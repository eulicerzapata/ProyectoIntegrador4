from airflow import DAG
from airflow.decorators import task
from datetime import datetime


with DAG(
    dag_id='olist_ecommerce',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['ETL', 'CSV', 'sqlite'],
) as dag:

    @task
    def extract_task():
        import logging
        import sys
        # Asegura que la carpeta montada `src` esté en sys.path cuando la tarea se ejecute dentro del contenedor
        sys.path.insert(0, "/opt/airflow/src")
        sys.path.insert(0, "/opt/airflow")
        from src.extract import extract
        from src.load import get_engine, load_all
        from src.config import DATASET_ROOT_PATH, get_csv_to_table_mapping, PUBLIC_HOLIDAYS_URL

        logging.info("Iniciando paso de extracción")
        dfs = extract(DATASET_ROOT_PATH, get_csv_to_table_mapping(), PUBLIC_HOLIDAYS_URL)
        logging.info(f"Se extrajeron {len(dfs)} tablas: {list(dfs.keys())}")
        engine = get_engine()
        load_all(dfs, engine)
        logging.info("Paso de extracción completado y datos cargados en la BD")

    @task
    def transform_task():
        import logging
        import sys
        sys.path.insert(0, "/opt/airflow/src")
        sys.path.insert(0, "/opt/airflow")
        from src.transform import run_queries
        from src.load import get_engine, load_all

        logging.info("Iniciando paso de transformación")
        engine = get_engine()
        query_results = run_queries(engine)
        logging.info(f"Se ejecutaron {len(query_results)} consultas: {list(query_results.keys())}")
        prefixed = {f"qry_{k}": v for k, v in query_results.items()}
        load_all(prefixed, engine)
        logging.info("Paso de transformación completado y resultados de consultas almacenados")

    @task
    def load_task():
        import os
        import logging
        import sys
        sys.path.insert(0, "/opt/airflow/src")
        sys.path.insert(0, "/opt/airflow")
        import pandas as pd
        from src.load import get_engine

        outdir = "/opt/airflow/query_results"
        os.makedirs(outdir, exist_ok=True)
        logging.info(f"Exportando resultados de consultas a {outdir}")
        engine = get_engine()
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'qry_%'", engine)
        logging.info(f"Se encontraron {len(tables)} tablas de resultados: {tables['name'].tolist()}")
        for name in tables['name'].tolist():
            df = pd.read_sql(f"SELECT * FROM {name}", engine)
            outpath = os.path.join(outdir, f"{name}.json")
            df.to_json(outpath, orient='records', force_ascii=False)
            logging.info(f"Se escribieron {len(df)} filas en {outpath}")

    # Define order
    e = extract_task()
    t = transform_task()
    l = load_task()

    e >> t >> l
