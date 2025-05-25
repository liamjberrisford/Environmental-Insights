<a id="environmental_insights.models"></a>

# environmental\_insights.models

<a id="environmental_insights.models.ensure_download"></a>

#### ensure\_download

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

#### load\_model\_united\_kingdom

```python
def load_model_united_kingdom(
        model_level: str,
        pollutant: str,
        model_category: str,
        token: Optional[str] = None) -> lgb.LGBMRegressor
```

Load a pretrained UK air pollution LGBM model for a specific category,
downloading only the required booster + params.

**Arguments**:

  - model_level: one of ['0.05','0.5','0.95','mean']
  - pollutant: one of ['no','no2','nox','o3','pm10','pm2p5','so2']
  - model_category: one of MODEL_CATEGORIES or 'All'

<a id="environmental_insights.models.load_model_global"></a>

#### load\_model\_global

```python
def load_model_global(model_level: str,
                      pollutant: str,
                      model_category: str,
                      token: Optional[str] = None) -> lgb.LGBMRegressor
```

Load a pretrained Global air pollution LGBM model for a specific category,
downloading only the required booster + params.

<a id="environmental_insights.models.make_concentration_predictions_united_kingdom"></a>

#### make\_concentration\_predictions\_united\_kingdom

```python
def make_concentration_predictions_united_kingdom(
        estimating_model: lgb.LGBMRegressor, observation_data: pd.DataFrame,
        feature_names: List[str]) -> pd.DataFrame
```

Predict concentrations using a trained LGBM model.

