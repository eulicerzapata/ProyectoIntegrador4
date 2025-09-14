# -*- coding: utf-8 -*-
"""
Runner end-to-end para el pipeline:
- Verifica dependencias clave (NumPy/Pandas) y te da un mensaje claro si hay incompatibilidades.
- Ejecuta extract(...) leyendo la carpeta dataset/ (fuera de src) según src.config.
- Carga todo a SQLite usando src.load (crea índices y respeta el orden).
- Lista las tablas creadas al final.

Colócalo en la raíz del repo (donde están /src y /dataset).
Ejecuta con: python run_pipeline.py
"""

from __future__ import annotations
import sys
import os
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))  # asegurar import de paquete src.*

def _check_dependencies() -> None:
    """Valida compatibilidad básica de NumPy/Pandas (evita errores binarios)."""
    try:
        import numpy as _np  # noqa
        np_ver = _np.__version__
    except Exception as e:
        print("❌ No se pudo importar NumPy:", e)
        print("Sugerencia: pip install --no-cache-dir \"numpy<2\"")
        sys.exit(1)

    try:
        import pandas as _pd  # noqa
        pd_ver = _pd.__version__
    except Exception as e:
        print("❌ No se pudo importar pandas (suele ser incompatibilidad con NumPy).")
        print("Detalle:", e)
        print("Arreglo sugerido en tu venv:\n"
              "  pip uninstall -y numpy pandas matplotlib seaborn\n"
              "  pip cache purge\n"
              "  pip install --no-cache-dir numpy==1.26.4\n"
              "  pip install --no-cache-dir pandas==1.5.2 matplotlib==3.6.2 seaborn==0.11.2")
        sys.exit(1)

def main() -> int:
    _check_dependencies()

    # Imports del proyecto (ya con deps validadas)
    try:
        from src.config import (
            DATASET_ROOT_PATH,
            get_csv_to_table_mapping,
            PUBLIC_HOLIDAYS_URL,
            SQLITE_BD_ABSOLUTE_PATH,
        )
        from src.extract import extract
        from src.load import get_engine, load_all
    except Exception as e:
        print("❌ Error importando módulos del proyecto:", e)
        return 1

    print("▶ Iniciando pipeline ELT…")
    print(f"   Dataset dir : {DATASET_ROOT_PATH}")
    print(f"   DB (SQLite) : {SQLITE_BD_ABSOLUTE_PATH}")

    t0 = perf_counter()
    try:
        mapping = get_csv_to_table_mapping()
        dfs = extract(
            csv_folder=DATASET_ROOT_PATH,
            csv_table_mapping=mapping,
            public_holidays_url=PUBLIC_HOLIDAYS_URL,
        )
    except SystemExit as e:
        print("❌ Falló la obtención de festivos (SystemExit):", e)
        return 1
    except Exception as e:
        print("❌ Error en extracción:", e)
        return 1
    t1 = perf_counter()
    print(f"✓ Extracción lista ({len(dfs)} tablas) en {t1 - t0:0.2f}s")

    try:
        engine = get_engine(SQLITE_BD_ABSOLUTE_PATH)
        load_all(dfs, engine, if_exists="replace")
    except Exception as e:
        print("❌ Error en carga a SQLite:", e)
        return 1
    t2 = perf_counter()
    print(f"✓ Carga completada en {t2 - t1:0.2f}s")

    # Comprobación rápida de tablas creadas
    try:
        import sqlite3
        db_path = SQLITE_BD_ABSOLUTE_PATH
        exists = os.path.exists(db_path)
        print(f"   DB creada: {exists} -> {db_path}")
        if exists:
            con = sqlite3.connect(db_path)
            with con:
                tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
                print(f"   Tablas ({len(tables)}): {', '.join(tables) if tables else '(ninguna)'}")
    except Exception as e:
        print("⚠ No pude listar tablas, pero la carga terminó. Detalle:", e)

    print("✅ Pipeline finalizado.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
