#!/usr/bin/env python3
"""
build_station_dashboard.py

Loads all UK monitoring stations (one DataFrame),
then creates a single Kepler.gl HTML containing one point‐layer per pollutant.
Each layer:
  • Uses `type: "point"`
  • Draws a semi‐transparent circle (50 m radius) at each station’s lat/lon
  • Renders the station name in white text (via `textLabel`)
  • Colors/fills each pollutant’s points with a unique RGB color

Saves to: _static/stations_combined.html
"""

import os
import pandas as pd
import geopandas as gpd
from environmental_insights import data as ei_data
from keplergl import KeplerGl
from copy import deepcopy

# === USER CONFIGURATION ===
AVAILABLE_POLLUTANTS = ["no2", "nox", "no", "o3", "pm10", "pm2p5", "so2"]
TARGET_CRS = "EPSG:4326"

# One RGB color per pollutant (fill color for the circle):
COLOR_PALETTE = {
    "no2":   [228,  26,  28],   # red
    "nox":   [ 55, 126, 184],   # blue
    "no":    [ 77, 175,  74],   # green
    "o3":    [152,  78, 163],   # purple
    "pm10":  [255, 127,   0],   # orange
    "pm2p5": [255, 255,  51],   # yellow
    "so2":   [166,  86,  40]    # brown
}

# Where to save the final HTML
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(THIS_DIR, "..", "book", "_static"))
os.makedirs(STATIC_DIR, exist_ok=True)


# -----------------------------------------------------------------------------
# STEP 1: Pull every station into a DataFrame (with columns: station, pollutant, latitude, longitude)
# -----------------------------------------------------------------------------
records = []

for pol in AVAILABLE_POLLUTANTS:
    station_list = ei_data.get_uk_monitoring_stations(pol)
    for station_name in station_list:
        station_gdf = ei_data.get_uk_monitoring_station(pollutant=pol, station=station_name)
        if station_gdf is None or station_gdf.empty:
            continue

        # If CRS is missing, assume EPSG:3995 (Easting/Northing), then reproject → 4326
        if station_gdf.crs is None:
            station_gdf.set_crs(epsg=3995, inplace=True)
        station_gdf = station_gdf.to_crs(TARGET_CRS)

        pt = station_gdf.geometry.iloc[0]
        # Replace underscores with spaces, Title‐case each station name:
        name_formatted = station_name.replace("_", " ").title()

        records.append({
            "station":   name_formatted,  # e.g. "London N Kensington"
            "pollutant": pol.upper(),     # e.g. "SO2"
            "latitude":  pt.y,
            "longitude": pt.x
        })

stations_df = pd.DataFrame(records)
# Now: stations_df.columns == ["station", "pollutant", "latitude", "longitude"] (all floats/strings)


# -----------------------------------------------------------------------------
# STEP 2: Build a Kepler JSON‐config with one “point” layer per pollutant.
#            Each layer has a `textLabel` entry that points to the “station” field.
# -----------------------------------------------------------------------------
# Base template for a “point” layer (we will deep‐copy this for each pollutant).
BASE_POINT_LAYER = {
    "id": "",            # to be filled in below
    "type": "point",
    "config": {
        "dataId": "",    # to be filled in below
        "color": [18, 147, 154],  # placeholder; overwritten per pollutant in build_layers()
        "columns": {
            "lat": "latitude",
            "lng": "longitude",
            "altitude": None
        },
        "isVisible": True,
        "visConfig": {
            "radius": 10,
            "fixedRadius": False,
            "opacity": 0.5,            # semi‐transparent
            "outline": False,
            "thickness": 0.5,
            "strokeColor": [0, 0, 0],
            "colorRange": {
                # We won’t use Kepler’s automatic colorRanging because we set fill color manually.
                "name": "Global Warming",
                "type": "diverging",
                "category": "Uber",
                "colors": [
                    "#5A1846", "#900C3F", "#C70039",
                    "#E3611C", "#F1920E", "#FFC300"
                ]
            },
            "strokeColorRange": {
                "name": "ColorBrewer Accent",
                "type": "qualitative",
                "category": "ColorBrewer",
                "colors": [
                    "#8DD3C7", "#FFFFB3", "#BEBADA",
                    "#FB8072", "#80B1D3", "#FDB462",
                    "#B3DE69", "#FCCDE5", "#D9D9D9",
                    "#BC80BD", "#CCEBC5", "#FFED6F"
                ]
            },
            "radiusRange": [1, 10],
            "filled": True,
            # ─── THIS IS THE CRITICAL PIECE ───
            # textLabel must specify “field” as {name:type}, not just a string.
            "textLabel": [
                {
                    "field": {
                        "name": "station",  # must match your DataFrame column
                        "type": "string"
                    },
                    "size": 12,            # font size
                    "color": [255, 255, 255],  # white text
                    "anchor": "start",     # place text to the right of the point
                    "alignment": "center"
                }
            ]
        },
        "hidden": False,
        "textLabel": []            # (deprecated here; Kepler FLATTENS `visConfig.textLabel`)
    },
    "visualChannels": {
        "colorField": None,
        "colorScale": "linear",
        "strokeColorField": None,
        "strokeColorScale": "linear",
        "sizeField": None,
        "sizeScale": "linear",
        "heightField": None,
        "heightScale": "linear",
        "radiusField": None,
        "radiusScale": "linear"
    }
}


def build_layers(pollutants):
    """
    For each pollutant in `pollutants`, clone BASE_POINT_LAYER,
    then set:
      • layer['id']               = "stations_<POLLUTANT>_pt"
      • layer['config']['dataId'] = same as layer['id']
      • layer['config']['label']  = "<POLLUTANT> Stations"
      • layer['config']['color']  = COLOR_PALETTE[pol]
    """
    layers = []
    for pol in pollutants:
        pol_upper = pol.upper()
        layer_id = f"stations_{pol_upper}_pt"

        layer = deepcopy(BASE_POINT_LAYER)
        layer["id"] = layer_id
        layer["config"]["dataId"] = layer_id
        layer["config"]["label"] = f"{pol_upper} Stations"
        layer["config"]["color"] = COLOR_PALETTE.get(pol, [18, 147, 154])
        layers.append(layer)

    return layers


layers = build_layers(AVAILABLE_POLLUTANTS)


# -----------------------------------------------------------------------------
# STEP 3: Build a tooltip config:
#   so that hovering any point shows “station” and “pollutant.”
# -----------------------------------------------------------------------------
tooltip_fields = {}
for pol in AVAILABLE_POLLUTANTS:
    layer_id = f"stations_{pol.upper()}_pt"
    tooltip_fields[layer_id] = [
        {"name": "station",   "format": None},
        {"name": "pollutant", "format": None}
    ]

tooltip_config = {
    "fieldsToShow": tooltip_fields,
    "compareMode": False,
    "enabled": True
}


POINTS_CONFIG = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": layers,
            "interactionConfig": {
                "tooltip": tooltip_config,
                "brush": {"size": 0.5, "enabled": False},
                "geocoder": {"enabled": False},
                "coordinate": {"enabled": False}
            },
            "layerBlending": "normal",
            "splitMaps": [],
            "animationConfig": {"currentTime": None, "speed": 1}
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 54.0,   # center roughly on the UK
            "longitude": -2.0,
            "pitch": 0,
            "zoom": 5,
            "isSplit": False
        }
    }
}


def save_combined_map(stations_df: pd.DataFrame):
    """
    - Instantiate a Kepler map with one 'point' layer per pollutant.
    - Add data for each pollutant to its matching layer.
    - Save to _static/stations_combined.html.
    """
    out_path = os.path.join(STATIC_DIR, "stations_combined.html")
    kmap = KeplerGl(config=POINTS_CONFIG, height=600)

    for pol in AVAILABLE_POLLUTANTS:
        pol_upper = pol.upper()
        subset = stations_df[stations_df["pollutant"] == pol_upper].copy()
        if subset.empty:
            continue

        layer_id = f"stations_{pol_upper}_pt"
        kmap.add_data(data=subset, name=layer_id)

    kmap.save_to_html(file_name=out_path)
    print(f"Combined map saved to: {out_path}")


def main():
    save_combined_map(stations_df)


if __name__ == "__main__":
    main()
