from typing import Dict
import requests
import pandas as pd
from src.config import (
    DATASET_ROOT_PATH,
    PUBLIC_HOLIDAYS_URL,
    get_csv_to_table_mapping,
)

def temp() -> pd.DataFrame:
    """Get the temperature data."""
    return pd.read_csv("data/temperature.csv")

def get_public_holidays(public_holidays_url: str, year: str) -> pd.DataFrame:
    """Get the public holidays for the given year for Brazil.

    TODO cubierto:
    - Usar requests para obtener los festivos: public_holidays_url/{year}/BR
    - Eliminar columnas 'types' y 'counties'
    - Convertir 'date' a datetime
    - Lanzar SystemExit si la solicitud falla (envolviendo raise_for_status)
    """
    url = f"{public_holidays_url}/{year}/BR"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        # Cumple con “lanzar SystemExit si la solicitud falla”
        raise SystemExit(f"Fallo al obtener festivos: {e}") from e

    data = resp.json()
    df = pd.json_normalize(data)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Eliminar columnas solicitadas, sin romper si no existen
    df = df.drop(columns=["types", "counties"], errors="ignore")
    return df

def extract(
    csv_folder: str | None = None,
    csv_table_mapping: Dict[str, str] | None = None,
    public_holidays_url: str = PUBLIC_HOLIDAYS_URL,
) -> Dict[str, pd.DataFrame]:
    """Extract the data from the csv files and return a dict of DataFrames."""
    # Defaults: usar la carpeta dataset fuera de src y el mapeo del config
    if csv_folder is None:
        csv_folder = DATASET_ROOT_PATH
    if csv_table_mapping is None:
        csv_table_mapping = get_csv_to_table_mapping()

    # Cargar todos los CSV a DataFrames usando el mapeo archivo->tabla
    dataframes: Dict[str, pd.DataFrame] = {
        table_name: pd.read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }

    # Añadir festivos de 2017 (ajusta si tu prueba requiere otro año)
    dataframes["public_holidays"] = get_public_holidays(public_holidays_url, "2017")
    return dataframes
