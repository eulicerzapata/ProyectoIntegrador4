# Proyecto Integrador IV - E-Commerce Data Pipeline

> Pipeline ELT (Extract, Load, Transform) para análisis de datos de e-commerce brasileño (Olist)

## 📋 Descripción

Este proyecto implementa un pipeline completo de datos para analizar información de e-commerce de la plataforma brasileña Olist. El pipeline incluye extracción de datos de múltiples fuentes, carga en una base de datos SQLite, y transformaciones para generar insights de negocio con visualizaciones interactivas.

## 🚀 Características

- **Extract**: Lectura de archivos CSV y obtención de datos de feriados públicos vía API
- **Load**: Carga de datos en base de datos SQLite con índices optimizados
- **Transform**: Consultas SQL para análisis de ingresos, entregas y patrones de compra
- **Visualizaciones**: Gráficos interactivos con Plotly para insights de negocio

## 📁 Estructura del Proyecto

```
proyecto_integrador/
├── src/                          # Código fuente principal
│   ├── config.py                # Configuración y rutas
│   ├── extract.py               # Funciones de extracción
│   ├── load.py                  # Funciones de carga a BD
│   ├── transform.py             # Queries y transformaciones
│   └── plots.py                 # Visualizaciones
├── dataset/                     # Archivos CSV de datos
├── queries/                     # Consultas SQL
├── tests/                       # Tests unitarios
├── images/                      # Gráficos de referencia
├── Project.ipynb               # Notebook principal
├── run_pipeline.py             # Script para ejecutar pipeline completo
└── requirements.txt            # Dependencias Python
```

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/eulicerzapata/ProyectoIntegrador4.git
   cd ProyectoIntegrador4
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Datos

El proyecto utiliza los siguientes datasets de Olist:
- `olist_customers_dataset.csv` - Información de clientes
- `olist_orders_dataset.csv` - Datos de pedidos
- `olist_order_items_dataset.csv` - Items de pedidos
- `olist_order_payments_dataset.csv` - Pagos
- `olist_order_reviews_dataset.csv` - Reseñas
- `olist_products_dataset.csv` - Productos
- `olist_sellers_dataset.csv` - Vendedores
- `olist_geolocation_dataset.csv` - Datos de geolocalización
- `product_category_name_translation.csv` - Traducción de categorías

**⚠️ IMPORTANTE**: Los archivos de datos no están incluidos en este repositorio debido a su tamaño. 

**Para obtener los datasets:**
1. Descarga el dataset completo de Olist desde [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Crea una carpeta `dataset/` en la raíz del proyecto
3. Extrae todos los archivos CSV en la carpeta `dataset/`

**Estructura requerida:**
```
dataset/
├── olist_customers_dataset.csv
├── olist_geolocation_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_orders_dataset.csv
├── olist_products_dataset.csv
├── olist_sellers_dataset.csv
└── product_category_name_translation.csv
```

## 🏃‍♂️ Uso

### Opción 1: Notebook Jupyter (Recomendado)
1. Abrir `Project.ipynb` en VS Code o Jupyter
2. Ejecutar las celdas secuencialmente

### Opción 2: Pipeline completo
```bash
python run_pipeline.py
```

### Opción 3: Componentes individuales
```python
# Ejecutar transformaciones
from src.transform import run_queries
from src.load import get_engine
from src.config import SQLITE_BD_ABSOLUTE_PATH

engine = get_engine(SQLITE_BD_ABSOLUTE_PATH)
results = run_queries(engine)
```

### Opción 4: Dashboard Interactivo 📊
```bash
# Ejecutar dashboard de Streamlit
python run_dashboard.py
# o directamente:
streamlit run dashboard.py
```
El dashboard se abrirá en `http://localhost:8501` con visualizaciones interactivas.

## 📈 Análisis Disponibles

### Ingresos
- Ingresos por mes y año
- Top 10 categorías más rentables
- Top 10 categorías menos rentables  
- Ingresos por estado

### Entregas
- Diferencias en fechas de entrega
- Tiempo real vs estimado de entrega
- Estados de pedidos globales
- Pedidos por día y feriados públicos
- Relación entre valor de flete y peso

### Dashboard Interactivo 🆕
- **Resumen ejecutivo**: KPIs principales y evolución temporal
- **Análisis de ingresos**: Categorías top y bottom performers
- **Performance de entregas**: Métricas de tiempo y precisión
- **Distribución geográfica**: Concentración por estados
- **5 visualizaciones principales** que responden al problema de negocio

## 🧪 Tests

Ejecutar tests unitarios:
```bash
python -m pytest tests/
```

## 📋 Requisitos

- Python 3.9+
- SQLite
- Librerías: pandas, plotly, sqlalchemy, requests, streamlit

## 🎯 Características del Dashboard

### 5 Visualizaciones Principales
1. **Evolución de Ingresos**: Líneas temporales mensuales 2017-2018
2. **Top Categorías**: Barras horizontales de categorías más rentables  
3. **Distribución Geográfica**: Ingresos por estado (top 15)
4. **Performance de Entregas**: Tiempo real vs estimado por mes
5. **KPIs Ejecutivos**: Panel de métricas principales

### Navegación Intuitiva
- **Resumen Ejecutivo**: Vista general con insights clave
- **Análisis de Ingresos**: Deep dive en categorías y tendencias
- **Performance de Entregas**: Métricas de cumplimiento y eficiencia  
- **Distribución Geográfica**: Concentración y oportunidades por región

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto es de uso académico.

## 👥 Autor

- **Eulicer Zapata** - [eulicerzapata](https://github.com/eulicerzapata)