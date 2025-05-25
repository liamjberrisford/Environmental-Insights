<a id="environmental_insights"></a>

# `environmental_insights`

<a id="environmental_insights.air_pollution_functions"></a>

# `environmental_insights.air_pollution_functions`

<a id="environmental_insights.air_pollution_functions.air_pollution_concentrations_to_UK_daily_air_quality_index"></a>

#### `air_pollution_concentrations_to_UK_daily_air_quality_index`

```python
def air_pollution_concentrations_to_UK_daily_air_quality_index(
        predicitions, pollutant, air_pollutant_column_name)
```

Add onto an existing dataframe the Daily Air Quality Index (https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info)
for the air pollutant concentration data described.

Parameters:
predicitions (dataframe): A dataframe of the air pollution concentrations that are to be added onto
pollutant (string): The string of the air pollutant concentration thresholds to be used to create the air quality indexes.
air_pollutant_column_name (string): The string of the column name for the air pollution concentration to calculate the air quality index on.

Returns:
dataframe: A dataframe with the additional columns for the air quality index based on the outlined air pollution concentration data.

<a id="environmental_insights.air_pollution_functions.visualise_air_pollution_daily_air_quality_index"></a>

#### `visualise_air_pollution_daily_air_quality_index`

```python
def visualise_air_pollution_daily_air_quality_index(air_pollution_GDF,
                                                    aqi_to_plot, filename)
```

Visualise air_pollution_GDF with the UK Daily Air Quality Index (https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info)
using the individual index bounds and standard color codes.

Parameters:
air_pollution_GDF (dataframe): A dataframe of the air pollution concentrations that are to be added onto
aqi_to_plot (string): Name of the column within air_pollution_GDF that has the indexes that are to be plotted.
filename (string): Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.visualise_air_pollution_daily_air_quality_bands"></a>

#### `visualise_air_pollution_daily_air_quality_bands`

```python
def visualise_air_pollution_daily_air_quality_bands(air_pollution_GDF,
                                                    aqi_to_plot, filename)
```

Visualise air_pollution_GDF with the UK Daily Air Quality Index (https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info)
using the bands and standard color codes.

Parameters:
air_pollution_GDF (dataframe): A dataframe of the air pollution concentrations that are to be added onto
aqi_to_plot (string): Name of the column within air_pollution_GDF that has the bands that are to be plotted.
filename (string): Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.change_in_concentrations_visulisation"></a>

#### `change_in_concentrations_visulisation`

```python
def change_in_concentrations_visulisation(first_dataframe, second_dataframe,
                                          air_pollutant, filename)
```

Visualisation the change in concentrations for two datasets of air pollution concentrations based on actual concentrations.

Parameters:
Parameters:
first_dataframe (DataFrame): The first concentration dataset.
second_dataframe (DataFrame): The second concentration dataset.
air_pollutant (string):  Common column name in both dataframes that will be used to calculate the difference in concentrations.
filename (string): Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.change_in_aqi_visulisation"></a>

#### `change_in_aqi_visulisation`

```python
def change_in_aqi_visulisation(first_dataframe, second_dataframe,
                               air_pollutant, filename)
```

Visualisation the change in concentrations for two datasets of air pollution concentrations based on air quality indexes.

Parameters:
Parameters:
first_dataframe (DataFrame): The first concentration dataset.
second_dataframe (DataFrame): The second concentration dataset.
air_pollutant (string):  Common column name in both dataframes that will be used to calculate the difference in concentrations.
filename (string): Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.change_in_concentration_line"></a>

#### `change_in_concentration_line`

```python
def change_in_concentration_line(air_pollutant, baseline_list, change_list,
                                 days, hours_covered, filename)
```

Visualisation the change in concentrations for two datasets of air pollution concentrations in a line graph.

Parameters:
Parameters:
air_pollutant (string): The name of the air pollutant to plot,
baseline_list (list): List of the air pollution concentrations for the baseline scenario.
change_list (list): List of the air pollution concentrations for the future scenario.
days (list): The days the lists covers.
hours_covered (list): The house the list covers.
filename (string): Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.data"></a>

# `environmental_insights.data`

<a id="environmental_insights.data.read_nc"></a>

#### `read_nc`

```python
def read_nc(filepath: str) -> xr.Dataset
```

Read a NetCDF (.nc) file into an xarray.Dataset.

Parameters
----------
filepath : str
    Path to the NetCDF file.

Returns
-------
xr.Dataset

<a id="environmental_insights.data.netcdf_to_dataframe"></a>

#### `netcdf_to_dataframe`

```python
def netcdf_to_dataframe(ds: xr.Dataset) -> pd.DataFrame
```

Convert an xarray.Dataset to a pandas DataFrame,
dropping any rows that have no valid data in *any* variable.

Parameters
----------
ds : xr.Dataset
    The dataset to convert.

Returns
-------
pd.DataFrame

<a id="environmental_insights.data.air_pollution_concentration_typical_day_real_time_united_kingdom"></a>

#### `air_pollution_concentration_typical_day_real_time_united_kingdom`

```python
def air_pollution_concentration_typical_day_real_time_united_kingdom(
        month: int, day_of_week: str, hour: int, data_type: str = "Input")
```

Retrieve the typical-day dataset (either Input or Output) for the UK for a given time.

Parameters:
-----------
month : int
    Month of interest, 1 (January) through 12 (December).
day_of_week : str
    Day of week of interest, e.g., "Monday", "Tuesday", etc.
hour : int
    Hour of interest, 0 (midnight) through 23.
data_type : str, optional
    Whether to fetch the "Input" or the "Output" version of the SynthHAPPE dataset.
    Defaults to "Input".

Returns:
--------
pandas.DataFrame
    The typical-day air pollution dataset for the UK at the specified time,
    as a flattened DataFrame.

<a id="environmental_insights.data.air_pollution_concentration_nearest_point_typical_day_united_kingdom"></a>

#### `air_pollution_concentration_nearest_point_typical_day_united_kingdom`

```python
def air_pollution_concentration_nearest_point_typical_day_united_kingdom(
        month: int,
        day_of_week: str,
        hour: int,
        latitude: float,
        longitude: float,
        uk_grids,
        data_type: str = "Input")
```

Retrieve a single air pollution concentration data point (Input or Output)
for the UK model at the closest grid point to a given lat/long.

Parameters:
-----------
month : int
    Month of interest, 1 (January) through 12 (December).
day_of_week : str
    Day of week of interest, e.g. "Monday", "Tuesday", etc.
hour : int
    Hour of interest, 0 (midnight) through 23.
latitude : float
    Latitude of the point to estimate.
longitude : float
    Longitude of the point to estimate.
uk_grids : GeoDataFrame
    Model grid points for the UK.
data_type : str, optional
    "Input" or "Output" dataset to fetch. Defaults to "Input".

Returns:
--------
pandas.DataFrame
    One-row DataFrame with the nearest grid’s pollutant values
    at the specified time.

<a id="environmental_insights.data.air_pollution_concentration_complete_set_real_time_united_kingdom"></a>

#### `air_pollution_concentration_complete_set_real_time_united_kingdom`

```python
def air_pollution_concentration_complete_set_real_time_united_kingdom(
        time: str, data_type: str = "Input")
```

Retrieve the complete predicted dataset (Input or Output) for a given timestamp in the UK ML-HAPPE dataset.

Parameters:
-----------
time : str
    Timestamp of the form "YYYY-MM-DD HHmmss".
data_type : str, optional
    Whether to fetch the "Input" or "Output" version of the ML-HAPPE dataset.
    Defaults to "Input".

Returns:
--------
pandas.DataFrame
    The full air pollution dataset for the UK at the specified timestamp,
    as a flattened DataFrame.

<a id="environmental_insights.data.air_pollution_concentration_nearest_point_real_time_united_kingdom"></a>

#### `air_pollution_concentration_nearest_point_real_time_united_kingdom`

```python
def air_pollution_concentration_nearest_point_real_time_united_kingdom(
        latitude: float,
        longitude: float,
        time: str,
        uk_grids,
        data_type: str = "Input")
```

Retrieve a single air pollution concentration data point (Input or Output)
for the UK ML-HAPPE model at the closest grid point to a given lat/long and timestamp.

Parameters:
-----------
latitude : float
    Latitude of the point to estimate.
longitude : float
    Longitude of the point to estimate.
time : str
    Timestamp of the form "YYYY-MM-DD HHmmss".
uk_grids : GeoDataFrame
    Model grid points for the UK.
data_type : str, optional
    "Input" or "Output" dataset to fetch. Defaults to "Input".

Returns:
--------
pandas.DataFrame
    One‐row DataFrame with the nearest grid’s pollutant values
    at the specified time.

<a id="environmental_insights.data.air_pollution_concentration_complete_set_real_time_global"></a>

#### `air_pollution_concentration_complete_set_real_time_global`

```python
def air_pollution_concentration_complete_set_real_time_global(time)
```

Retrieve the complete calculated dataset for a given timestamp in the global dataset.

Parameters:
time (string): A string denoting the timestamp desired, of the form DD-MM-YYYY HHmmss.

Returns:
DataFrame: A DataFrame of the dataset for the global model for a given timestamp.

<a id="environmental_insights.data.get_amenities_as_geodataframe"></a>

#### `get_amenities_as_geodataframe`

```python
def get_amenities_as_geodataframe(amenity_type, min_lat, min_lon, max_lat,
                                  max_lon)
```

Fetch amenities of a given type within a bounding box and return as a GeoDataFrame.

Parameters:
amenity_type (string): Type of amenity, e.g., "hospital".
min_lat (float): Minimum latitude.
min_lon (float): Minimum longitude.
max_lat (float): Maximum latitude.
max_lon (float): Maximum longitude.

Returns:
GeoDataFrame: A GeoDataFrame containing the amenities with their names and coordinates.

<a id="environmental_insights.data.get_highways_as_geodataframe"></a>

#### `get_highways_as_geodataframe`

```python
def get_highways_as_geodataframe(highway_type, min_lat, min_lon, max_lat,
                                 max_lon)
```

Fetch highways of a specified type within a bounding box from OSM and return as a GeoDataFrame.

Parameters:
highway_type (string): Type of highway, e.g., "motorway", "residential".
min_lat (float): Minimum latitude.
min_lon (float): Minimum longitude.
max_lat (float): Maximum latitude.
max_lon (float): Maximum longitude.

Returns:
GeoDataFrame: A GeoDataFrame containing the highways with their names and coordinates.

<a id="environmental_insights.data.ckd_nearest_LineString"></a>

#### `ckd_nearest_LineString`

```python
def ckd_nearest_LineString(gdf_A, gdf_B, gdf_B_cols)
```

Calculate the nearest points between two GeoDataFrames containing LineString geometries.

This function uses cKDTree to efficiently find the nearest points between two sets
of LineStrings. For each point in `gdf_A`, the function finds the closest point
in `gdf_B` and returns the distances along with selected columns from `gdf_B`.

Parameters:
gdf_A (GeoDataFrame): A GeoDataFrame containing LineString geometries.
gdf_B (GeoDataFrame): A GeoDataFrame containing LineString geometries which will be
                     used to find the closest points to `gdf_A`.
gdf_B_cols (list or tuple): A list or tuple containing column names from `gdf_B`
                           which will be included in the resulting DataFrame.

Returns:
GeoDataFrame: A GeoDataFrame with each row containing a geometry from `gdf_A`,
              corresponding closest geometry details from `gdf_B` (as specified by `gdf_B_cols`),
              and the distance to the closest point in `gdf_B`.

Note:
The resulting GeoDataFrame maintains the order of `gdf_A` and attaches the nearest
details from `gdf_B`.
This code was adapted from the code available here: https://gis.stackexchange.com/questions/222315/finding-nearest-point-in-other-geodataframe-using-geopandas

<a id="environmental_insights.data.get_even_spaced_points"></a>

#### `get_even_spaced_points`

```python
def get_even_spaced_points(points, number_of_points)
```

Generate a list of evenly spaced points between two given points.

This function calculates the distance (or difference) between two input points
and divides this distance into `number_of_points` equal segments. The resulting
points, including the start and end points, are returned in a list.

Parameters:
points (list or tuple of float): A list or tuple containing two points
                                (start and end) between which the evenly spaced points
                                are to be calculated.
number_of_points (int): The total number of points to generate,
                      including the start and end points.

Returns:
list: A list of evenly spaced points between the provided start and end points.

Example:
>>> get_even_spaced_points([1, 10], 5)
[1.0, 3.25, 5.5, 7.75, 10.0]

Note:
The function assumes that the points list is sorted in ascending order.

<a id="environmental_insights.data.calculate_new_metrics_distance_total"></a>

#### `calculate_new_metrics_distance_total`

```python
def calculate_new_metrics_distance_total(current_infrastructure, highway_type,
                                         start_point, end_point,
                                         land_grids_centroids, land_grids)
```

Simulate the addition of a proposed highway to current infrastructure and calculate new metrics.

This function creates a new proposed highway segment based on given start and end points.
The proposed highway is then added to the current infrastructure dataset. After adding the
new highway, the function calculates distance metrics and total length of the specific highway type.

Parameters:
current_infrastructure (GeoDataFrame): The current infrastructure dataset with existing highways.
highway_type (str): Type of the highway for which metrics are calculated (e.g., "motorway").
start_point (tuple of float): Coordinates (x, y) for the starting point of the proposed highway.
end_point (tuple of float): Coordinates (x, y) for the ending point of the proposed highway.
land_grids_centroids (GeoDataFrame): GeoDataFrame of the grids for predictions to be made on, with the geometry being a set of points representing the centroid of such grids.
land_grids (GeoDataFrame): GeoDataFrame of the grids for predictions to be made on, with the geometry being a set of polygons representing the grids themselves.

Returns:
tuple:
  - GeoDataFrame: Contains metrics such as road infrastructure distance and total road length for each grid.
  - GeoDataFrame: A merged dataset of current infrastructure and the proposed highway.

Note:
- The function assumes the use of EPSG:4326 and EPSG:3395 for coordinate reference systems.
- It also assumes the existence of helper functions like `get_even_spaced_points` and a global variable `land_grids_centroids`.

<a id="environmental_insights.data.replace_feature_vector_column"></a>

#### `replace_feature_vector_column`

```python
def replace_feature_vector_column(feature_vector, new_feature_vector,
                                  feature_vector_name)
```

Replace the feature vector column name with the new feature vector column name, replacing the data within the dataframe with new environmental conditions.

Parameters:
feature_vector (DataFrame): DataFrame of the original data.
new_feature_vector (DataFrame): DataFrame containing the new feature vector that is to be used to replace the data in feature_vector.
feature_vector_name (string): Name of the feature vector to be changed.

Returns:
DataFrame: A DataFrame of the original data that was added with the feature vector now replaced by the new data.

<a id="environmental_insights.data.get_uk_grids"></a>

#### `get_uk_grids`

```python
def get_uk_grids()
```

Get the spatial grids that represent the locations at which air pollution estimations are made for the UK Model.

Returns:
GeoDataFrame: A GeoDataFrame of the polygons for each of the grids in the UK Model alongside their centroid and unique ID.

<a id="environmental_insights.data.get_global_grids"></a>

#### `get_global_grids`

```python
def get_global_grids()
```

Get the spatial grids that represent the locations at which air pollution estimations are made for the Global Model.

Returns:
GeoDataFrame: A GeoDataFrame of the polygons for each of the grids in the Global Model and unique ID.

<a id="environmental_insights.download"></a>

# `environmental_insights.download`

<a id="environmental_insights.download.download_file"></a>

#### `download_file`

```python
def download_file(url: str,
                  output_dir: Optional[Union[str, Path]] = None,
                  token: Optional[str] = None,
                  extra_wget_args: Optional[List[str]] = None) -> None
```

Download a single URL using wget into output_dir (defaults to package root).

<a id="environmental_insights.download.download_time_point_ml"></a>

#### `download_time_point_ml`

```python
def download_time_point_ml(
        dataset: str,
        data_type: str,
        timestamp: str,
        token: Optional[str] = None,
        output_dir: Optional[Union[str, Path]] = None) -> None
```

Download a single .nc time point for ML-HAPPE Input/Output.

<a id="environmental_insights.download.download_time_point_synth"></a>

#### `download_time_point_synth`

```python
def download_time_point_synth(
        data_type: str,
        month: Union[int, str],
        day: str,
        hour: Union[int, str],
        token: Optional[str] = None,
        output_dir: Optional[Union[str, Path]] = None) -> None
```

Download a single .nc file for SynthHAPPE with synthetic filename format:
Month_<n>-Day_<DayName>-Hour_<h>.nc
Month can be numeric or month name.

<a id="environmental_insights.download.download_models"></a>

#### `download_models`

```python
def download_models(model_level: str,
                    pollutant: str,
                    model_category: str,
                    token: Optional[str] = None,
                    output_dir: Optional[Union[str, Path]] = None) -> None
```

Download ML-HAPPE model files for each category, or all if 'All' is specified.

<a id="environmental_insights.download.download_training_data"></a>

#### `download_training_data`

```python
def download_training_data(
        pollutant: str,
        station: str,
        token: Optional[str] = None,
        output_dir: Optional[Union[str, Path]] = None) -> None
```

Download ML-HAPPE training data .nc for a station.

<a id="environmental_insights.download.download"></a>

#### `download`

```python
def download(dataset: str,
             data_type: str,
             timestamp: Optional[str] = None,
             month: Optional[Union[int, str]] = None,
             day: Optional[str] = None,
             hour: Optional[Union[int, str]] = None,
             model_level: Optional[str] = None,
             pollutant: Optional[str] = None,
             station: Optional[str] = None,
             token: Optional[str] = None,
             output_dir: Optional[Union[str, Path]] = None) -> None
```

Unified download interface for ML-HAPPE and SynthHAPPE.

<a id="environmental_insights.models"></a>

# `environmental_insights.models`

<a id="environmental_insights.models.ensure_download"></a>

#### `ensure_download`

```python
def ensure_download(dataset: str,
                    data_type: str,
                    *,
                    timestamp: Optional[str] = None,
                    month: Optional[Union[int, str]] = None,
                    day: Optional[str] = None,
                    hour: Optional[Union[int, str]] = None,
                    model_level: Optional[str] = None,
                    pollutant: Optional[str] = None,
                    station: Optional[str] = None,
                    token: Optional[str] = None,
                    output_dir: Optional[Union[str, Path]] = None) -> None
```

Ensure the requested file(s) exist locally by invoking the unified downloader.

<a id="environmental_insights.models.load_model_united_kingdom"></a>

#### `load_model_united_kingdom`

```python
def load_model_united_kingdom(
        model_level: str,
        pollutant: str,
        model_category: str,
        token: Optional[str] = None) -> lgb.LGBMRegressor
```

Load a pretrained UK air pollution LGBM model for a specific category,
downloading only the required booster + params.

Parameters:
- model_level: one of ['0.05','0.5','0.95','mean']
- pollutant: one of ['no','no2','nox','o3','pm10','pm2p5','so2']
- model_category: one of MODEL_CATEGORIES or 'All'

<a id="environmental_insights.models.load_model_global"></a>

#### `load_model_global`

```python
def load_model_global(model_level: str,
                      pollutant: str,
                      model_category: str,
                      token: Optional[str] = None) -> lgb.LGBMRegressor
```

Load a pretrained Global air pollution LGBM model for a specific category,
downloading only the required booster + params.

<a id="environmental_insights.models.make_concentration_predictions_united_kingdom"></a>

#### `make_concentration_predictions_united_kingdom`

```python
def make_concentration_predictions_united_kingdom(
        estimating_model: lgb.LGBMRegressor, observation_data: pd.DataFrame,
        feature_names: List[str]) -> pd.DataFrame
```

Predict concentrations using a trained LGBM model.

<a id="environmental_insights.variables"></a>

# `environmental_insights.variables`

<a id="tests"></a>

# `tests`

<a id="tests..ipynb_checkpoints.tests_air_pollution_functions-checkpoint"></a>

# `tests..ipynb_checkpoints.tests_air_pollution_functions-checkpoint`

<a id="tests..ipynb_checkpoints.tests_data-checkpoint"></a>

# `tests..ipynb_checkpoints.tests_data-checkpoint`

<a id="tests..ipynb_checkpoints.tests_models-checkpoint"></a>

# `tests..ipynb_checkpoints.tests_models-checkpoint`

<a id="tests.integration.test_end_to_end_workflow"></a>

# `tests.integration.test_end_to_end_workflow`

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests"></a>

## `IntegrationWorkflowTests` Objects

```python
class IntegrationWorkflowTests(unittest.TestCase)
```

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_input_output_nonempty"></a>

#### `test_input_output_nonempty`

```python
def test_input_output_nonempty()
```

Input and output datasets should be non-empty after download and load.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_model_predictions"></a>

#### `test_model_predictions`

```python
def test_model_predictions()
```

Model predictions should include the 'Model Prediction' column and contain data.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_aqi_conversion"></a>

#### `test_aqi_conversion`

```python
def test_aqi_conversion()
```

AQI conversion should add the correct AQI column and return data.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_nearest_point"></a>

#### `test_nearest_point`

```python
def test_nearest_point()
```

Retrieving the nearest point data should return a single point with distance measurement.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_visualisations_are_saved"></a>

#### `test_visualisations_are_saved`

```python
def test_visualisations_are_saved()
```

Visualisation functions should complete without error and save PNG files.

<a id="tests.unit.test_air_pollution_functions"></a>

# `tests.unit.test_air_pollution_functions`

<a id="tests.unit.test_air_pollution_functions._"></a>

#### `_`

Access C-API

<a id="tests.unit.test_data"></a>

# `tests.unit.test_data`

<a id="tests.unit.test_models"></a>

# `tests.unit.test_models`

