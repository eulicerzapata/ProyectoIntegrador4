# � Dashboard de Analytics - Olist E-commerce

## 🎯 Descripción del Dashboard

Este dashboard interactivo proporciona análisis completo del rendimiento del marketplace brasileño Olist durante los años 2016-2018, enfocándose en dos áreas clave: **Ingresos** y **Entregas**.

## � Cómo Ejecutar el Dashboard

### Prerequisitos
- Python 3.9+
- Entorno virtual activado

### Instalación de Dependencias
```bash
pip install streamlit plotly pandas
```

### Ejecutar Dashboard
```bash
streamlit run dashboard.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📈 Estructura del Dashboard

### 1. 📈 Resumen Ejecutivo
- **Métricas principales**: KPIs de ingresos, crecimiento, y performance
- **Evolución temporal**: Gráfico de líneas con ingresos mensuales 2017-2018
- **Insights clave**: Tendencias principales y oportunidades de negocio

### 2. � Análisis de Ingresos
- **Top 10 categorías**: Gráfico de barras horizontal con categorías más rentables
- **Categorías menos exitosas**: Identificación de áreas que requieren atención
- **Detalles por categoría**: Tablas comparativas con métricas detalladas

### 3. 🚚 Performance de Entregas
- **Tiempo real vs estimado**: Comparación mensual de tiempos de entrega
- **Métricas de performance**: Promedios y precisión de estimaciones
- **Análisis por año**: Evolución de la eficiencia de entregas

### 4. 🗺️ Distribución Geográfica
- **Ingresos por estado**: Gráfico de barras de los top 15 estados
- **Concentración de mercado**: Análisis de dependencia geográfica
- **Top performers**: Estados con mayor contribución a ingresos

## 📊 Los 5 Gráficos Principales

1. **Evolución de Ingresos Mensuales** (Líneas temporales)
   - Comparación 2017 vs 2018
   - Identificación de tendencias estacionales

2. **Top 10 Categorías por Ingresos** (Barras horizontales)
   - Categorías más rentables
   - Volumen de pedidos vs ingresos

3. **Ingresos por Estado** (Barras verticales)
   - Distribución geográfica del negocio
   - Top 15 estados contribuyentes

4. **Tiempo Real vs Estimado de Entrega** (Líneas comparativas)
   - Performance mensual de entregas
   - Precisión de estimaciones por año

5. **Panel de KPIs Ejecutivos** (Métricas)
   - Ingresos totales y crecimiento
   - Top performers por categoría y estado
   - Métricas de entregas

## 🔍 Insights del Problema de Negocio

### Área de Ingresos
- **Crecimiento significativo** entre 2017 y 2018
- **Categorías estrella**: `bed_bath_table`, `health_beauty`, `computers_accessories`
- **Estacionalidad**: Picos en Mayo-Agosto, caída en Q4
- **Concentración geográfica**: SP, RJ, MG dominan el mercado

### Área de Entregas
- **Mejora en tiempos**: Reducción de tiempos promedio en 2018
- **Precisión variable**: Estimaciones más precisas en algunos meses
- **Oportunidad de optimización**: Estandarizar procesos de entrega

## 📋 Preguntas de Negocio Respondidas

1. **¿Cuánto ingresaron por año?**
   - 2017: ~$6.7M, 2018: ~$9.7M (45% crecimiento)

2. **¿Cuáles fueron las categorías más populares?**
   - Top 3: Cama/baño/mesa, Salud/belleza, Computadoras/accesorios

3. **¿Cuáles fueron los ingresos por estado?**
   - SP: $5.8M (40%), RJ: $2.1M (14%), MG: $1.8M (12%)

4. **¿Qué tan bien entrega la compañía?**
   - Tiempo promedio 2017: 12.8 días, 2018: 11.7 días
   - Mejora del 8.6% en eficiencia

5. **¿Diferencia entre fecha estimada y real?**
   - 2017: Estimaciones muy conservadoras (sobrestiman por ~12 días)
   - 2018: Estimaciones más precisas pero aún conservadoras

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework web interactivo
- **Plotly**: Gráficos interactivos y responsive
- **Pandas**: Manipulación y análisis de datos
- **SQLite**: Base de datos para consultas
- **Python**: Lenguaje principal de desarrollo

## 📁 Estructura de Archivos

```
├── dashboard.py              # Aplicación principal de Streamlit (COMENTADA)
├── tests/query_results/      # Datos JSON pre-procesados
│   ├── revenue_by_month_year.json
│   ├── top_10_revenue_categories.json
│   ├── revenue_per_state.json
│   └── real_vs_estimated_delivered_time.json
├── src/                      # Código fuente del ETL
└── requirements.txt          # Dependencias (incluye streamlit)
```

## 🎨 Características del Dashboard

- **Interfaz intuitiva**: Navegación por pestañas en sidebar
- **Gráficos interactivos**: Hover, zoom, pan automáticos
- **Responsive design**: Se adapta a diferentes tamaños de pantalla
- **Métricas en tiempo real**: KPIs calculados automáticamente
- **Insights automáticos**: Interpretación de datos integrada
- **Código comentado**: dashboard.py incluye explicaciones detalladas

## �️ Cómo Funciona el Código

### Configuración Inicial
```python
# IMPORTANTE: st.set_page_config() DEBE ser lo primero
st.set_page_config(
    page_title="Olist E-commerce Analytics",
    page_icon="📊",
    layout="wide"  # Usar todo el ancho de pantalla
)
```

### Sistema de Caché
```python
@st.cache_data  # Evita recargar datos en cada interacción
def load_query_result(filename):
    # Cargar datos JSON una sola vez
```

### Navegación
```python
# Sidebar con selectbox para navegación
selected_page = st.sidebar.selectbox("Selecciona sección:", menu_options)

# Router simple con if/elif
if selected_page == "📈 Resumen Ejecutivo":
    show_executive_summary()
```

### Gráficos
```python
# plotly.express para gráficos rápidos
fig = px.bar(df, x='Revenue', y='Category')

# plotly.graph_objects para control avanzado
fig = go.Figure()
fig.add_trace(go.Scatter(...))
```

### Layout
```python
# Columnas para organizar contenido horizontalmente
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("KPI", "valor", "delta")
```

## 📞 Soporte

### Verificaciones Antes de Ejecutar
1. ✅ Python 3.9+ instalado
2. ✅ Dependencias instaladas: `pip install streamlit plotly pandas`
3. ✅ Archivos JSON en `tests/query_results/`
4. ✅ Puerto 8501 disponible

### Problemas Comunes
- **"Page config must be called first"**: Mover `st.set_page_config()` al inicio
- **Datos no cargan**: Verificar que archivos JSON existen
- **Performance lenta**: Asegurar que `@st.cache_data` está en funciones de carga

### Comandos Útiles
```bash
# Ejecutar en puerto específico
streamlit run dashboard.py --server.port 8502

# Ejecutar sin abrir navegador
streamlit run dashboard.py --server.headless true

# Limpiar caché si es necesario
# Usar Ctrl+C en terminal, luego volver a ejecutar
```

---
*Dashboard desarrollado para análisis de datos de Olist E-commerce (2016-2018)*
*Código fuente completamente comentado en `dashboard.py`*