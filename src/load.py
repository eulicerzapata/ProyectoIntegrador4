# src/load.py
from typing import Dict
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine
from src.config import SQLITE_BD_ABSOLUTE_PATH  # usa la ruta del config

# Ruta por defecto del DW (SQLite) desde config
DEFAULT_DB_PATH = SQLITE_BD_ABSOLUTE_PATH

def get_engine(db_path: str = DEFAULT_DB_PATH) -> Engine:
    """Crea/retorna un Engine de SQLAlchemy para SQLite."""
    return create_engine(f"sqlite:///{db_path}")

# Columnas datetime por tabla (según Olist + festivos)
_DATETIME_COLUMNS = {
    "olist_orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "olist_order_items": ["shipping_limit_date"],
    "olist_order_reviews": ["review_creation_date", "review_answer_timestamp"],
    "public_holidays": ["date"],
}

def _ensure_datetime_serializable(name: str, df: DataFrame) -> DataFrame:
    """Convierte a datetime las columnas conocidas para evitar problemas en SQLite."""
    out = df.copy()
    for col in _DATETIME_COLUMNS.get(name, []):
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
    return out

def load_dataframe(
    name: str,
    df: DataFrame,
    engine: Engine,
    if_exists: str = "replace",
    index: bool = False,
) -> None:
    """Carga un DataFrame a SQLite usando su nombre de tabla."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df debe ser DataFrame, recibido: {type(df)}")

    df = _ensure_datetime_serializable(name, df)

    # Normaliza objetos a string para evitar tipos mixtos en SQLite
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("string")

    df.to_sql(name=name, con=engine, if_exists=if_exists, index=index)

def _create_basic_indexes(engine: Engine) -> None:
    """Índices útiles para acelerar joins y filtros comunes."""
    stmts = [
        # Orders & relacionados
        "CREATE INDEX IF NOT EXISTS idx_olist_orders_order_id ON olist_orders(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_olist_orders_customer_id ON olist_orders(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_olist_orders_purchase_ts ON olist_orders(order_purchase_timestamp)",

        "CREATE INDEX IF NOT EXISTS idx_olist_order_items_order_id ON olist_order_items(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_olist_order_items_product_id ON olist_order_items(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_olist_order_items_seller_id ON olist_order_items(seller_id)",

        "CREATE INDEX IF NOT EXISTS idx_olist_order_payments_order_id ON olist_order_payments(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_olist_order_reviews_order_id ON olist_order_reviews(order_id)",

        # Dimensiones
        "CREATE INDEX IF NOT EXISTS idx_olist_customers_customer_id ON olist_customers(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_olist_products_product_id ON olist_products(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_olist_sellers_seller_id ON olist_sellers(seller_id)",

        # Festivos
        "CREATE INDEX IF NOT EXISTS idx_public_holidays_date ON public_holidays(date)",
    ]
    with engine.begin() as conn:
        for s in stmts:
            conn.execute(text(s))

def load_all(tables: Dict[str, DataFrame], engine: Engine, if_exists: str = "replace") -> None:
    """Carga todas las tablas y crea índices."""
    # Orden sugerido: dimensiones -> hechos -> extras
    preferred_order = [
        "product_category_name_translation",
        "olist_customers",
        "olist_geolocation",
        "olist_products",
        "olist_sellers",
        "olist_orders",
        "olist_order_items",
        "olist_order_payments",
        "olist_order_reviews",
        "public_holidays",
    ]
    for name in preferred_order:
        if name in tables:
            load_dataframe(name, tables[name], engine, if_exists=if_exists, index=False)

    # Carga cualquier otra tabla no contemplada explícitamente
    for name, df in tables.items():
        if name not in preferred_order:
            load_dataframe(name, df, engine, if_exists=if_exists, index=False)

    _create_basic_indexes(engine)

# === Función simple que cumple el TODO original de tu test ===
def load(data_frames: Dict[str, DataFrame], database: Engine):
    """
    Por cada DataFrame en el diccionario, usa pandas.DataFrame.to_sql()
    para cargar el DataFrame como una tabla cuyo nombre es la clave.
    (Cumple exactamente el TODO del enunciado.)
    """
    for table_name, df in data_frames.items():
        df = _ensure_datetime_serializable(table_name, df)
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype("string")
        df.to_sql(name=table_name, con=database, if_exists="replace", index=False)

if __name__ == "__main__":
    # Ejecución e2e: extract -> load_all
    from src.extract import extract
    from src.config import DATASET_ROOT_PATH, get_csv_to_table_mapping, PUBLIC_HOLIDAYS_URL

    dfs = extract(DATASET_ROOT_PATH, get_csv_to_table_mapping(), PUBLIC_HOLIDAYS_URL)
    eng = get_engine(DEFAULT_DB_PATH)
    load_all(dfs, eng)
    print("Carga completada en:", DEFAULT_DB_PATH)
