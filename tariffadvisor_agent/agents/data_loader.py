import pandas as pd
import requests

def load_tariff_data(source="tariff.csv"):
    """
    Load tariff data from a local CSV or a remote API endpoint.
    """
    if source.endswith(".csv"):
        return _load_from_csv(source)
    elif source.startswith("http"):
        return _load_from_api(source)
    else:
        raise ValueError("Unsupported source type. Must be a .csv file or HTTP URL.")

def _load_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return _clean_tariff_columns(df)
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV: {e}")

def _load_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        return _clean_tariff_columns(df)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch data from API: {e}")

def _clean_tariff_columns(df):
    """
    Cleans % signs and converts tariff columns to float.
    """
    if "TariffsCharged2USA" in df.columns:
        df["TariffsCharged2USA"] = (
            df["TariffsCharged2USA"]
            .astype(str)
            .str.replace('%', '', regex=False)
            .astype(float)
        )
    if "USAReciprocalTariffs" in df.columns:
        df["USAReciprocalTariffs"] = (
            df["USAReciprocalTariffs"]
            .astype(str)
            .str.replace('%', '', regex=False)
            .astype(float)
        )
    return df
