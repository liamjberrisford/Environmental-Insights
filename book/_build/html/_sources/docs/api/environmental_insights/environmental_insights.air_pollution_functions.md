<a id="environmental_insights.air_pollution_functions"></a>

# environmental\_insights.air\_pollution\_functions

<a id="environmental_insights.air_pollution_functions.air_pollution_concentrations_to_UK_daily_air_quality_index"></a>

#### air\_pollution\_concentrations\_to\_UK\_daily\_air\_quality\_index

```python
def air_pollution_concentrations_to_UK_daily_air_quality_index(
        predicitions, pollutant, air_pollutant_column_name)
```

Add onto an existing dataframe the Daily Air Quality Index (https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info)
for the air pollutant concentration data described.

**Arguments**:

- `predicitions` _dataframe_ - A dataframe of the air pollution concentrations that are to be added onto
- `pollutant` _string_ - The string of the air pollutant concentration thresholds to be used to create the air quality indexes.
- `air_pollutant_column_name` _string_ - The string of the column name for the air pollution concentration to calculate the air quality index on.
  

**Returns**:

- `dataframe` - A dataframe with the additional columns for the air quality index based on the outlined air pollution concentration data.

<a id="environmental_insights.air_pollution_functions.visualise_air_pollution_daily_air_quality_index"></a>

#### visualise\_air\_pollution\_daily\_air\_quality\_index

```python
def visualise_air_pollution_daily_air_quality_index(air_pollution_GDF,
                                                    aqi_to_plot, filename)
```

Visualise air_pollution_GDF with the UK Daily Air Quality Index (https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info)
using the individual index bounds and standard color codes.

**Arguments**:

- `air_pollution_GDF` _dataframe_ - A dataframe of the air pollution concentrations that are to be added onto
- `aqi_to_plot` _string_ - Name of the column within air_pollution_GDF that has the indexes that are to be plotted.
- `filename` _string_ - Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.visualise_air_pollution_daily_air_quality_bands"></a>

#### visualise\_air\_pollution\_daily\_air\_quality\_bands

```python
def visualise_air_pollution_daily_air_quality_bands(air_pollution_GDF,
                                                    aqi_to_plot, filename)
```

Visualise air_pollution_GDF with the UK Daily Air Quality Index (https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info)
using the bands and standard color codes.

**Arguments**:

- `air_pollution_GDF` _dataframe_ - A dataframe of the air pollution concentrations that are to be added onto
- `aqi_to_plot` _string_ - Name of the column within air_pollution_GDF that has the bands that are to be plotted.
- `filename` _string_ - Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.change_in_concentrations_visulisation"></a>

#### change\_in\_concentrations\_visulisation

```python
def change_in_concentrations_visulisation(first_dataframe, second_dataframe,
                                          air_pollutant, filename)
```

Visualisation the change in concentrations for two datasets of air pollution concentrations based on actual concentrations.

**Arguments**:

- `first_dataframe` _DataFrame_ - The first concentration dataset.
- `second_dataframe` _DataFrame_ - The second concentration dataset.
- `air_pollutant` _string_ - Common column name in both dataframes that will be used to calculate the difference in concentrations.
- `filename` _string_ - Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.change_in_aqi_visulisation"></a>

#### change\_in\_aqi\_visulisation

```python
def change_in_aqi_visulisation(first_dataframe, second_dataframe,
                               air_pollutant, filename)
```

Visualisation the change in concentrations for two datasets of air pollution concentrations based on air quality indexes.

**Arguments**:

- `first_dataframe` _DataFrame_ - The first concentration dataset.
- `second_dataframe` _DataFrame_ - The second concentration dataset.
- `air_pollutant` _string_ - Common column name in both dataframes that will be used to calculate the difference in concentrations.
- `filename` _string_ - Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

<a id="environmental_insights.air_pollution_functions.change_in_concentration_line"></a>

#### change\_in\_concentration\_line

```python
def change_in_concentration_line(air_pollutant, baseline_list, change_list,
                                 days, hours_covered, filename)
```

Visualisation the change in concentrations for two datasets of air pollution concentrations in a line graph.

**Arguments**:

- `air_pollutant` _string_ - The name of the air pollutant to plot,
- `baseline_list` _list_ - List of the air pollution concentrations for the baseline scenario.
- `change_list` _list_ - List of the air pollution concentrations for the future scenario.
- `days` _list_ - The days the lists covers.
- `hours_covered` _list_ - The house the list covers.
- `filename` _string_ - Filename for the visualisation that is outputted in the environmental_insights_visulisations directory

