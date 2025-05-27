#!/usr/bin/env python3
"""
build_no2_output_dashboards.py

Creates two kepler.gl dashboards that map the 'no2_Prediction_Mean'
from the OUTPUT datasets on UK model grid polygons, with hover highlighting
and semi-transparent fills, optimized to use minimal float precision:
  1) SynthHAPPE (typical-day) Output only
  2) ML-HAPPE   (real-time)    Output only

Each is saved to its own .html, centred over the UK with a color legend,
no permanent borders, but a colored border appears on hover, fills are semi-
transparent, and data precision is reduced for minimal payload size.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.ops import transform
from keplergl import KeplerGl

# your EI helper functions:
from environmental_insights import data as ei_data

# === CONFIGURE HERE ===
MONTH         = 1
DAY_OF_WEEK   = "Friday"
HOUR          = 9
REALTIME_TIME = "2018-01-01_090000"  # YYYY-MM-DD_HHMMSS

VAR_NAME      = "no2_Prediction_Mean"
VAR_NAME_NEAT = "Nitrogen Dioxide Predicition Mean" 
OUT_TYP_HTML  = "../book/_static/synthhappe_no2.html"
OUT_RT_HTML   = "../book/_static/mlhappe_no2.html"
# ======================


def load_uk_grid():
    """
    Load the UK model grid polygons, keeping only ID and geometry.
    Returns a GeoDataFrame with 'UK_Model_Grid_ID' and 'geometry'.
    """
    gdf = ei_data.get_uk_grids()
    return gdf[["UK_Model_Grid_ID", "geometry"]]


def prepare_and_merge(df, grid_gdf):
    """
    Merge OUTPUT data on UK_Model_Grid_ID, cast to float16, simplify geometry coords,
    reproject to WGS84, and return minimal GeoDataFrame.
    """
    # select ID and variable, drop NaNs
    df2 = df[["UK_Model_Grid_ID", VAR_NAME]].dropna(subset=[VAR_NAME]).copy()
    # cast variable to float16
    df2[VAR_NAME] = df2[VAR_NAME].astype(np.float16)

    # merge with grid polygons
    merged = grid_gdf.merge(df2, on="UK_Model_Grid_ID", how="inner")

    # ensure WGS84
    if merged.crs != "EPSG:4326":
        merged = merged.to_crs(epsg=4326)

    # round geometry coordinates to 2 decimals (~1m precision)
    def _round_geom(geom):
        return transform(lambda x, y: (round(x, 2), round(y, 2)), geom)
    merged["geometry"] = merged["geometry"].apply(_round_geom)
    merged = merged.rename(columns={VAR_NAME:VAR_NAME_NEAT})
    # keep only needed columns
    return merged[["geometry", VAR_NAME_NEAT]]


def build_no2_grid_dashboard(grid_gdf, df, out_html):
    """
    Render NO2 var on grid polygons with semitransparent fill,
    no default borders, yellow highlight on hover, minimal data size.
    """
    plot_gdf = prepare_and_merge(df, grid_gdf)


    
    print(f"[{out_html}] plotting {len(plot_gdf)} grid polygons of '{VAR_NAME_NEAT}'")

    uk_config = {
      "version": "v1",
      "config": {
        "mapState": {"latitude": 54.0, "longitude": -2.0, "zoom": 5, "pitch": 0, "bearing": 0},
        "visState": {
          "layers": [
            {
              "id": "no2_grid_layer",
              "type": "geojson",
              "config": {
                "autoHighlight": True,
                "dataId": VAR_NAME_NEAT,
                "label": VAR_NAME_NEAT,
                "columns": {"geojson": "geometry"},
                "isVisible": True,
                "visConfig": {
                  "opacity": 0.25,
                  "filled": True,
                  "stroked": True,
                  "thickness": 1,
                  "strokeColor": [0, 0, 0, 0],
                  "highlightColor": [255, 255, 0, 255],
                  "colorRange": {
                    "name": "Global Warming",
                    "type": "sequential",
                    "category": "Uber",
                    "colors": [
                      "#5A1846", "#900C3F", "#C70039",
                      "#E3611C", "#F1920E", "#FFC300"
                    ]
                  }
                }
              },
              "visualChannels": {"colorField": {"name": VAR_NAME_NEAT, "type": "real"}, "colorScale": "quantile"}
            }
          ],
          "interactionConfig": {
            "tooltip": {"fieldsToShow": {VAR_NAME_NEAT: [VAR_NAME_NEAT]}, "enabled": True},
            "brush": {"size": 0.5, "enabled": False},
            "geocoder": {"enabled": False},
            "coordinate": {"enabled": False}
          },
          "layerBlending": "normal",
          "splitMaps": [],
          "animationConfig": {"currentTime": None, "speed": 1}
        }
      }
    }

    m = KeplerGl(data={VAR_NAME_NEAT: plot_gdf}, config=uk_config)
    m.save_to_html(file_name=out_html)
    print(f"→ Wrote {out_html}")


def main():
    grid_gdf = load_uk_grid()

    # SynthHAPPE typical-day
    typ_out = ei_data.air_pollution_concentration_typical_day_real_time_united_kingdom(
        MONTH, DAY_OF_WEEK, HOUR, data_type="Output"
    )
    build_no2_grid_dashboard(grid_gdf, typ_out, OUT_TYP_HTML)

    # ML-HAPPE real-time
    rt_out = ei_data.air_pollution_concentration_complete_set_real_time_united_kingdom(
        REALTIME_TIME, data_type="Output"
    )
    build_no2_grid_dashboard(grid_gdf, rt_out, OUT_RT_HTML)

if __name__ == "__main__":
    main()
