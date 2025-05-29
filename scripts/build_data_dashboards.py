#!/usr/bin/env python3
"""
build_no2_input_data_kepler.py

Loads UK model grid and two NO₂ prediction datasets (typical-day and complete real-time),
prepares & simplifies the geometries, then visualizes each layer in its own KeplerGl map and
saves each map to separate HTML files in the ../_static/ directory (creating it if needed).
"""

import os
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
VAR_NAME_NEAT = "Nitrogen Dioxide Prediction Mean"
# ======================

# Adjust pandas display settings for a "pretty" console output
pd.set_option('display.width', 120)
pd.set_option('display.max_columns', None)

# Kepler Gl base config (shared)
import copy
base_config = {
    'version': 'v1',
    'config': {
        'visState': {
            'filters': [],
            'layers': [{
                'id': 'gyunm4n',
                'type': 'geojson',
                'config': {
                    'dataId': None,
                    'label': None,
                    'color': [77, 193, 156],
                    'highlightColor': [252, 242, 26, 255],
                    'columns': {'geojson': 'geometry'},
                    'isVisible': True,
                    'visConfig': {
                        'opacity': 0.2,
                        'strokeOpacity': 0.8,
                        'thickness': 0.5,
                        'strokeColor': [119, 110, 87],
                        'colorRange': {
                            'name': 'Global Warming',
                            'type': 'sequential',
                            'category': 'Uber',
                            'colors': [
                                '#5A1846', '#900C3F', '#C70039',
                                '#E3611C', '#F1920E', '#FFC300'
                            ]
                        },
                        'strokeColorRange': {
                            'name': 'Global Warming',
                            'type': 'sequential',
                            'category': 'Uber',
                            'colors': [
                                '#5A1846', '#900C3F', '#C70039',
                                '#E3611C', '#F1920E', '#FFC300'
                            ]
                        },
                        'radius': 10,
                        'sizeRange': [0, 10],
                        'radiusRange': [0, 50],
                        'heightRange': [0, 500],
                        'elevationScale': 5,
                        'enableElevationZoomFactor': True,
                        'stroked': False,
                        'filled': True,
                        'enable3d': False,
                        'wireframe': False
                    },
                    'hidden': False,
                    'textLabel': [{
                        'field': None,
                        'color': [255, 255, 255],
                        'size': 18,
                        'offset': [0, 0],
                        'anchor': 'start',
                        'alignment': 'center'
                    }]
                },
                'visualChannels': {
                    'colorField': {'name': VAR_NAME_NEAT, 'type': 'real'},
                    'colorScale': 'quantile',
                    'strokeColorField': None,
                    'strokeColorScale': 'quantile',
                    'sizeField': None,
                    'sizeScale': 'linear',
                    'heightField': None,
                    'heightScale': 'linear',
                    'radiusField': None,
                    'radiusScale': 'linear'
                }
            }],
            'interactionConfig': {
                'tooltip': {
                    'fieldsToShow': {},
                    'compareMode': False,
                    'compareType': 'absolute',
                    'enabled': True
                },
                'brush': {'size': 0.5, 'enabled': False},
                'geocoder': {'enabled': False},
                'coordinate': {'enabled': False}
            },
            'layerBlending': 'normal',
            'splitMaps': [],
            'animationConfig': {'currentTime': None, 'speed': 1}
        },
        'mapState': {
            'bearing': 0,
            'dragRotate': False,
            'latitude': 52.69738599316781,
            'longitude': -0.29600986227730636,
            'pitch': 0,
            'zoom': 5,
            'isSplit': False
        }
    }
}

def load_uk_grid():
    gdf = ei_data.get_uk_grids()
    return gdf[["UK_Model_Grid_ID", "geometry"]]

def prepare_and_merge(df: pd.DataFrame,
                      grid_gdf: gpd.GeoDataFrame,
                      simplify_tol: float = 0.0005,
                      quantize_digits: int = 4) -> gpd.GeoDataFrame:
    df2 = df[["UK_Model_Grid_ID", VAR_NAME]].dropna(subset=[VAR_NAME]).copy()
    df2[VAR_NAME] = df2[VAR_NAME].astype(np.float16)
    merged = grid_gdf.merge(df2, on="UK_Model_Grid_ID", how="inner")
    if merged.crs != "EPSG:4326":
        merged = merged.to_crs(epsg=4326)
    merged["geometry"] = merged.geometry.simplify(
        tolerance=simplify_tol, preserve_topology=True
    )
    def _quantize(geom):
        return transform(
            lambda x, y: (round(x, quantize_digits), round(y, quantize_digits)),
            geom
        )
    merged["geometry"] = merged.geometry.apply(_quantize)
    merged = merged.rename(columns={VAR_NAME: VAR_NAME_NEAT})
    return merged[["geometry", VAR_NAME_NEAT]]

def save_map(gdf: gpd.GeoDataFrame, title: str, filename: str):
    """
    Create a KeplerGl map for `gdf`, save to `filename`, and print confirmation.
    Ensures the output directory exists.
    """
    # Prepare output path and directory
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../book/_static'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    # Prepare config copy
    conf = copy.deepcopy(base_config)
    conf['config']['visState']['layers'][0]['config']['dataId'] = title
    conf['config']['visState']['layers'][0]['config']['label'] = title
    conf['config']['visState']['interactionConfig']['tooltip']['fieldsToShow'] = {
        title: [{'name': VAR_NAME_NEAT, 'format': None}]
    }

    # Create and save map
    kmap = KeplerGl(config=conf)
    kmap.add_data(data=gdf, name=title)
    kmap.save_to_html(file_name=out_path)
    print(f"{title} map saved to {out_path}")


def main():
    grid_gdf    = load_uk_grid()
    typ_df       = ei_data.air_pollution_concentration_typical_day_real_time_united_kingdom(
                    MONTH, DAY_OF_WEEK, HOUR, data_type="Output"
                  )
    typ_prepared = prepare_and_merge(typ_df, grid_gdf)

    rt_df        = ei_data.air_pollution_concentration_complete_set_real_time_united_kingdom(
                    REALTIME_TIME, data_type="Output"
                  )
    rt_prepared  = prepare_and_merge(rt_df, grid_gdf)

    save_map(typ_prepared, title="Typical Day NO₂ Prediction", filename="synthhappe_no2.html")
    save_map(rt_prepared,  title="Real-Time NO₂ Prediction",  filename="mlhappe_no2.html")

if __name__ == "__main__":
    main()