import os
import subprocess
from pathlib import Path
from typing import List, Optional, Union
import environmental_insights
import calendar
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Determine the package root for default downloads
PACKAGE_ROOT = Path(environmental_insights.__file__).parent

# Base URLs for datasets
BASE_URLS = {
    "ML-HAPPE": "https://dap.ceda.ac.uk/badc/deposited2025/ML-HAPPE/",
    "SynthHAPPE": "https://dap.ceda.ac.uk/badc/deposited2025/SynthHAPPE/",
    "SynthHAPPE_v2": "https://dap.ceda.ac.uk/badc/deposited2025/SynthHAPPE_v2/",
}

# Valid options
DATASETS = list(BASE_URLS.keys())
ML_HAPPE_TYPES = ["Input", "Output", "Models", "Training_Data"]
SYNTH_TYPES = ["Input", "Output"]
MODEL_LEVELS = ["0.05", "0.5", "0.95", "mean"]
POLLUTANTS = ["no", "no2", "nox", "o3", "pm10", "pm2p5", "so2"]
MODEL_CATEGORIES = [
    "All",
    "Emissions_Models",
    "Forecasting_Models",
    "Forecasting_Transport_and_Emissions_Models",
    "Geographic_Models",
    "Global_Models",
    "Metrological_Models",
    "Remote_Sensing_Models",
    "Temporal_Models",
    "Transport_Infrastructure_Models",
    "Transport_Use_Models",
    "Climate_Projections_Models",
    "Transport_Infrastructure_Policy_Models",
]


def download_file(
    url: str,
    output_dir: Optional[Union[str, Path]] = None,
    token: Optional[str] = None,
    extra_wget_args: Optional[List[str]] = None
) -> None:
    """
    Download a single URL using wget into output_dir (defaults to package root).
    """
    # Determine download directory
    out_dir = Path(output_dir) if output_dir else PACKAGE_ROOT
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build wget command
    cmd = [
        "wget",
        "-e", "robots=off",
        "--no-parent",
        "-P", str(out_dir)
    ]
    if extra_wget_args:
        cmd.extend(extra_wget_args)
    if token:
        cmd.extend(["--header", f"Authorization: Bearer {token}"])
    cmd.append(url)

    # Execute wget
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"wget failed (code {result.returncode}) for URL: {url}\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
    print(f"Downloaded: {url} -> {out_dir}")


def download_time_point_ml(
    dataset: str,
    data_type: str,
    timestamp: str,
    token: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None
) -> None:
    """
    Download a single .nc time point for ML-HAPPE Input/Output.
    """
    # Append .nc if missing
    ts = timestamp if timestamp.endswith('.nc') else f"{timestamp}.nc"
    url = f"{BASE_URLS[dataset]}{data_type}/{ts}"
    download_file(url, output_dir, token)


def download_time_point_synth(
    data_type: str,
    month: Union[int, str],
    day: str,
    hour: Union[int, str],
    token: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None
) -> None:
    """
    Download a single .nc file for SynthHAPPE with synthetic filename format:
    Month_<n>-Day_<DayName>-Hour_<h>.nc
    Month can be numeric or month name.
    """
    # Normalize month to number
    if isinstance(month, str):
        try:
            # Try numeric string
            m = int(month)
        except ValueError:
            # Month name to number
            names = {name.lower(): num for num, name in enumerate(calendar.month_name) if name}
            m = names.get(month.lower())
            if m is None:
                raise ValueError(f"Invalid month: {month}")
    else:
        m = month
    if not 1 <= m <= 12:
        raise ValueError(f"Month must be 1-12 or name; got {month}")
    # Format day and hour
    day_norm = day.capitalize()
    try:
        h = int(hour)
    except ValueError:
        raise ValueError(f"Hour must be an integer; got {hour}")

    filename = f"Month_{m}-Day_{day_norm}-Hour_{h}.nc"
    url = f"{BASE_URLS['SynthHAPPE']}{data_type}/{filename}"
    download_file(url, output_dir, token)


def download_models(
    model_level: str,
    pollutant: str,
    model_category: str,
    token: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None
) -> None:
    """
    Download the LightGBM booster and params files for a given model.
    - For ML-HAPPE models: path is ML-HAPPE/Models/{level}/{pollutant}/All_Stations/{pollutant}_{category}
    - For SynthHAPPE_v2 models: path is SynthHAPPE_v2/Models/{category}
    """
    # normalize output_dir
    out = Path(output_dir or Path.cwd())
    if model_category not in MODEL_CATEGORIES:
        raise ValueError(f"Unknown model_category: {model_category!r}")

    # pick namespace & build subdir(s)
    if model_category in ("Climate_Projections_Models", "Transport_Infrastructure_Policy_Models"):
        base = BASE_URLS["SynthHAPPE_v2"]
        subdirs = [f"Models/{model_category}"]
    else:
        base = BASE_URLS["ML-HAPPE"]
        cats = MODEL_CATEGORIES[1:] if model_category == "All" else [model_category]
        subdirs = [
            f"Models/{model_level}/{pollutant}/All_Stations/{pollutant}_{cat}"
            for cat in cats
        ]

    # download each file in each subdir
    for sd in subdirs:
        for fname in ("model_booster.txt", "model_params.json"):
            url = f"{base}{sd}/{fname}"
            print(f"→ Downloading {url}")
            download_file(url, out / model_category, token)

    print("Download complete.")





def download_training_data(
    pollutant: str,
    station: str,
    token: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None
) -> None:
    """
    Download ML-HAPPE training data .nc for a station.
    """
    if pollutant not in POLLUTANTS:
        raise ValueError(f"Invalid pollutant: {pollutant}")
    fn = station if station.endswith('.nc') else f"{station}.nc"
    url = f"{BASE_URLS['ML-HAPPE']}Training_Data/{pollutant}/{fn}"
    download_file(url, output_dir, token)

def get_training_station_names(
    pollutant: str
) -> list[str]:
    """
    Return a sorted list of all station names (without “.nc”) available
    under ML-HAPPE/Training_Data/{pollutant}/.
    """
    if pollutant not in POLLUTANTS:
        raise ValueError(f"Invalid pollutant: {pollutant}")
    url = f"{BASE_URLS['ML-HAPPE']}Training_Data/{pollutant}/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    stations = {
        Path(link.get("href")).stem
        for link in soup.find_all("a", href=True)
        if link["href"].endswith(".nc")
    }
    return sorted(stations)


def download(
    dataset: str,
    data_type: str,
    timestamp: Optional[str] = None,
    month: Optional[Union[int, str]] = None,
    day: Optional[str] = None,
    hour: Optional[Union[int, str]] = None,
    model_level: Optional[str] = None,
    pollutant: Optional[str] = None,
    station: Optional[str] = None,
    token: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None
) -> None:
    """
    Unified download interface for ML-HAPPE and SynthHAPPE.
    """
    if dataset not in DATASETS:
        raise ValueError(f"Dataset must be one of {DATASETS}")

    # SynthHAPPE branch
    if dataset == 'SynthHAPPE':
        if data_type not in SYNTH_TYPES:
            raise ValueError(f"Type for SynthHAPPE must be one of {SYNTH_TYPES}")
        if month is None or day is None or hour is None:
            raise ValueError("`month`, `day`, and `hour` are required for SynthHAPPE downloads")
        download_time_point_synth(data_type, month, day, hour, token, output_dir)
        return

    # ML-HAPPE branch
    if data_type in ('Input', 'Output'):
        if not timestamp:
            raise ValueError("`timestamp` is required for ML-HAPPE Input/Output downloads")
        download_time_point_ml(dataset, data_type, timestamp, token, output_dir)
    elif data_type == 'Models':
        if not model_level or not pollutant:
            raise ValueError("`model_level` and `pollutant` are required for Models downloads")
        download_models(model_level, pollutant, token, output_dir)
    elif data_type == 'Training_Data':
        if not pollutant:
            raise ValueError("`pollutant` is required for Training_Data")
        if station:
            # ------ SINGLE-STATION DOWNLOAD: ------
            download_training_data(
                pollutant=pollutant,
                station=station,
                token=token,
                output_dir=output_dir
            )
        else:
            # ------ LIST AVAILABLE STATIONS: ------
            return get_training_station_names(pollutant, token)
    else:
        raise ValueError(f"Type for ML-HAPPE must be one of {ML_HAPPE_TYPES}")
