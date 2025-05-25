<a id="tests.integration.test_end_to_end_workflow"></a>

# tests.integration.test\_end\_to\_end\_workflow

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests"></a>

## IntegrationWorkflowTests Objects

```python
class IntegrationWorkflowTests(unittest.TestCase)
```

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_input_output_nonempty"></a>

#### test\_input\_output\_nonempty

```python
def test_input_output_nonempty()
```

Input and output datasets should be non-empty after download and load.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_model_predictions"></a>

#### test\_model\_predictions

```python
def test_model_predictions()
```

Model predictions should include the 'Model Prediction' column and contain data.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_aqi_conversion"></a>

#### test\_aqi\_conversion

```python
def test_aqi_conversion()
```

AQI conversion should add the correct AQI column and return data.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_nearest_point"></a>

#### test\_nearest\_point

```python
def test_nearest_point()
```

Retrieving the nearest point data should return a single point with distance measurement.

<a id="tests.integration.test_end_to_end_workflow.IntegrationWorkflowTests.test_visualisations_are_saved"></a>

#### test\_visualisations\_are\_saved

```python
def test_visualisations_are_saved()
```

Visualisation functions should complete without error and save PNG files.

