"""
E-commerce Analytics Dashboard
Dashboard interactivo para análisis de datos de Olist (2016-2018)

Este dashboard responde al problema de negocio de análisis de ingresos y entregas
para el marketplace brasileño Olist durante el período completo 2016-2018.
"""

# ===================================================================================
# IMPORTACIONES - Librerías necesarias para el dashboard
# ===================================================================================
import streamlit as st          # Framework principal para crear la aplicación web
import pandas as pd            # Manipulación y análisis de datos
import plotly.express as px    # Gráficos rápidos e interactivos
import plotly.graph_objects as go  # Gráficos personalizados y avanzados
from plotly.subplots import make_subplots  # Para crear múltiples gráficos en una figura
import json                    # Para leer archivos JSON con los datos
import sqlite3                 # Conector de base de datos SQLite (opcional)
from pathlib import Path       # Manejo de rutas de archivos

# ===================================================================================
# CONFIGURACIÓN INICIAL DE LA APLICACIÓN
# ===================================================================================
# IMPORTANTE: st.set_page_config() DEBE ser lo primero en ejecutarse
st.set_page_config(
    page_title="Olist E-commerce Analytics",  # Título en la pestaña del navegador
    page_icon="📊",                          # Icono en la pestaña del navegador
    layout="wide",                           # Usar todo el ancho de la pantalla
    initial_sidebar_state="expanded"         # Mostrar la barra lateral expandida
)

# ===================================================================================
# TÍTULO Y DESCRIPCIÓN PRINCIPAL
# ===================================================================================
st.title("🛒 Olist E-commerce Analytics Dashboard")
st.markdown("""
**Análisis de rendimiento empresarial 2016-2018**  
Explora las métricas clave de ingresos y entregas del marketplace brasileño Olist durante todo el período de datos disponible
""")

# ===================================================================================
# CONFIGURACIÓN DE LA BARRA LATERAL (SIDEBAR)
# ===================================================================================
st.sidebar.title("🎛️ Panel de Control")
st.sidebar.markdown("---")  # Línea separadora

# ===================================================================================
# FUNCIONES DE CARGA DE DATOS CON CACHÉ
# ===================================================================================
# El decorador @st.cache_data hace que Streamlit guarde en memoria los resultados
# Esto evita recargar los datos cada vez que el usuario interactúa

@st.cache_data
def load_query_result(filename):
    """
    Carga resultados de consultas desde archivos JSON
    
    Args:
        filename (str): Nombre del archivo sin extensión .json
    
    Returns:
        list: Lista de diccionarios con los datos del JSON
    """
    try:
        with open(f"tests/query_results/{filename}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"No se pudo cargar el archivo {filename}.json")
        return []

@st.cache_data
def load_revenue_by_month():
    """Carga y procesa datos de ingresos por mes y año"""
    data = load_query_result("revenue_by_month_year")
    df = pd.DataFrame(data)
    return df

@st.cache_data  
def load_top_categories():
    """Carga datos de top categorías por ingresos"""
    data = load_query_result("top_10_revenue_categories")
    df = pd.DataFrame(data)
    return df

@st.cache_data
def load_revenue_by_state():
    """Carga datos de ingresos por estado"""
    data = load_query_result("revenue_per_state")
    df = pd.DataFrame(data)
    return df

@st.cache_data
def load_delivery_comparison():
    """Carga datos de comparación de tiempos de entrega"""
    data = load_query_result("real_vs_estimated_delivered_time")
    df = pd.DataFrame(data)
    return df

# ===================================================================================
# FUNCIÓN PRINCIPAL DEL DASHBOARD - SISTEMA DE NAVEGACIÓN
# ===================================================================================
def main():
    """
    Función principal que controla la navegación del dashboard
    
    Streamlit ejecuta todo el código de arriba hacia abajo cada vez que hay interacción.
    Usamos selectbox para controlar qué sección mostrar.
    """
    # Crear menú de navegación en la barra lateral
    menu_options = [
        "📈 Resumen Ejecutivo",      # Vista general con KPIs principales
        "💰 Análisis de Ingresos",   # Deep dive en categorías y tendencias
        "🚚 Performance de Entregas", # Métricas de cumplimiento
        "🗺️ Distribución Geográfica" # Análisis por estados
    ]
    
    # selectbox crea un menú desplegable - el usuario elige una opción
    selected_page = st.sidebar.selectbox("Selecciona una sección:", menu_options)
    
    # Según la selección, mostrar la página correspondiente
    if selected_page == "📈 Resumen Ejecutivo":
        show_executive_summary()
    elif selected_page == "💰 Análisis de Ingresos":
        show_revenue_analysis()
    elif selected_page == "🚚 Performance de Entregas":
        show_delivery_analysis()
    elif selected_page == "🗺️ Distribución Geográfica":
        show_geographic_analysis()

# ===================================================================================
# PÁGINA 1: RESUMEN EJECUTIVO
# ===================================================================================
def show_executive_summary():
    """
    Página de resumen ejecutivo con métricas principales
    
    Muestra:
    1. KPIs principales en formato de métricas
    2. Gráfico de evolución temporal principal
    3. Insights clave para la dirección
    """
    st.header("📈 Resumen Ejecutivo")
    
    # Cargar todos los datos necesarios para esta página
    revenue_df = load_revenue_by_month()
    categories_df = load_top_categories()
    states_df = load_revenue_by_state()
    
    # ===================================================================================
    # CÁLCULO DE MÉTRICAS PRINCIPALES
    # ===================================================================================
    total_2016 = revenue_df['Year2016'].sum()
    total_2017 = revenue_df['Year2017'].sum()
    total_2018 = revenue_df['Year2018'].sum()
    # Calcular tasa de crecimiento año a año (verificamos división por cero)
    growth_rate_17 = ((total_2017 - total_2016) / total_2016 * 100) if total_2016 > 0 else 0
    growth_rate_18 = ((total_2018 - total_2017) / total_2017 * 100) if total_2017 > 0 else 0
    
    # ===================================================================================
    # DISEÑO CON COLUMNAS - MÉTRICAS PRINCIPALES
    # ===================================================================================
    # st.columns() permite dividir el espacio horizontal en secciones
    col1, col2, col3, col4 = st.columns(4)
    
    # Columna 1: Ingresos 2016 (año de lanzamiento)
    with col1:
        st.metric(
            label="📅 Ingresos 2016",                    # Etiqueta de la métrica
            value=f"${total_2016:,.0f}",                # Valor principal (formato con comas)
            delta="Año de lanzamiento"                  # Contexto del año
        )
    
    # Columna 2: Ingresos 2017 con crecimiento vs 2016
    with col2:
        st.metric(
            label="📈 Ingresos 2017",
            value=f"${total_2017:,.0f}",
            delta=f"{growth_rate_17:+.1f}% vs 2016" if total_2016 > 0 else "Primer año completo"
        )
    
    # Columna 3: Ingresos 2018 con crecimiento vs 2017
    with col3:
        st.metric(
            label="💰 Ingresos 2018",                    # Etiqueta de la métrica
            value=f"${total_2018:,.0f}",                # Valor principal (formato con comas)
            delta=f"{growth_rate_18:+.1f}% vs 2017"    # Delta (cambio) con signo y color automático
        )
    
    with col4:
        total_orders = categories_df['Num_order'].sum()
        st.metric(
            label="📦 Total Pedidos",
            value=f"{total_orders:,}",
            delta="Top 10 categorías"
        )
    
    st.markdown("---")
    
    # Gráfico principal: Evolución temporal de ingresos
    # ===================================================================================
    # GRÁFICO PRINCIPAL: EVOLUCIÓN TEMPORAL DE INGRESOS
    # ===================================================================================
    st.subheader("📊 Evolución de Ingresos Mensuales")
    
    # Crear figura usando plotly.graph_objects para más control
    fig = go.Figure()
    
    # Agregar línea para 2016
    fig.add_trace(go.Scatter(
        x=revenue_df['month'],           # Eje X: meses
        y=revenue_df['Year2016'],        # Eje Y: ingresos 2016
        mode='lines+markers',           # Mostrar líneas y puntos
        name='2016',                    # Nombre en la leyenda
        line=dict(color='#d62728', width=3),  # Color rojo
        marker=dict(size=8)             # Tamaño de los marcadores
    ))
    
    # Agregar línea para 2017
    fig.add_trace(go.Scatter(
        x=revenue_df['month'],           # Eje X: meses
        y=revenue_df['Year2017'],        # Eje Y: ingresos 2017
        mode='lines+markers',           # Mostrar líneas y puntos
        name='2017',                    # Nombre en la leyenda
        line=dict(color='#1f77b4', width=3),  # Color azul
        marker=dict(size=8)             # Tamaño de los marcadores
    ))
    
    # Agregar línea para 2018
    fig.add_trace(go.Scatter(
        x=revenue_df['month'],
        y=revenue_df['Year2018'],
        mode='lines+markers',
        name='2018',
        line=dict(color='#ff7f0e', width=3),  # Color naranja
        marker=dict(size=8)
    ))
    
    # Configurar el layout del gráfico
    fig.update_layout(
        title="Ingresos Mensuales 2016-2018",    # Título del gráfico actualizado
        xaxis_title="Mes",                       # Etiqueta eje X
        yaxis_title="Ingresos ($)",              # Etiqueta eje Y
        height=500,                              # Altura en píxeles
        hovermode='x unified'                    # Mostrar hover unificado por X
    )
    
    # Mostrar el gráfico en Streamlit (use_container_width=True hace que use todo el ancho)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights clave
    st.subheader("🔍 Insights Clave")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **💡 Tendencias de Ingresos:**
        - 2016: Año de lanzamiento (${total_2016:,.0f})
        - 2017: Crecimiento significativo ({growth_rate_17:+.1f}%)
        - 2018: Expansión acelerada ({growth_rate_18:+.1f}%)
        - Picos de ventas en Mayo-Agosto 2018
        """)
    
    with col2:
        st.success("""
        **🎯 Oportunidades:**
        - Mantener momentum de crecimiento 2016-2018
        - Optimizar estrategias para Q4
        - Fortalecer categorías top performers
        - Expandir en estados con alto potencial
        """)

# ===================================================================================
# PÁGINA 2: ANÁLISIS DE INGRESOS
# ===================================================================================
def show_revenue_analysis():
    """
    Página de análisis detallado de ingresos
    
    Incluye:
    1. Gráfico de barras de top categorías
    2. Gráfico de categorías con menor rendimiento
    3. Tablas comparativas con detalles
    """
    st.header("💰 Análisis de Ingresos")
    
    # Gráfico de top categorías
    st.subheader("🏆 Top 10 Categorías por Ingresos")
    
    categories_df = load_top_categories()
    
    # Usar plotly.express para gráfico de barras rápido
    fig = px.bar(
        categories_df,                           # DataFrame con los datos
        x='Revenue',                            # Columna para eje X
        y='Category',                           # Columna para eje Y
        orientation='h',                        # Horizontal (barras acostadas)
        title="Categorías con Mayores Ingresos", # Título
        labels={'Revenue': 'Ingresos ($)', 'Category': 'Categoría'},  # Etiquetas
        color='Revenue',                        # Colorear por valor de ingresos
        color_continuous_scale='viridis'        # Esquema de colores
    )
    
    # Configurar layout específico
    fig.update_layout(
        height=600,                             # Altura del gráfico
        yaxis={'categoryorder':'total ascending'} # Ordenar categorías por valor
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de categorías menos exitosas
    st.subheader("📉 Categorías con Menor Rendimiento")
    
    least_categories = load_query_result("top_10_least_revenue_categories")
    least_df = pd.DataFrame(least_categories)
    
    if not least_df.empty:
        fig2 = px.bar(
            least_df,
            x='Category',
            y='Revenue',
            title="10 Categorías con Menores Ingresos",
            labels={'Revenue': 'Ingresos ($)', 'Category': 'Categoría'},
            color='Revenue',
            color_continuous_scale='reds'
        )
        
        fig2.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tabla de detalles
    st.subheader("📋 Detalles por Categoría")
    
    # Combinar datos de top y least categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏆 Top Performers**")
        top_display = categories_df.head(5).copy()
        top_display['Revenue'] = top_display['Revenue'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(top_display, hide_index=True)
    
    with col2:
        st.markdown("**📉 Requieren Atención**")
        if not least_df.empty:
            least_display = least_df.sort_values('Revenue', ascending=True).head(5).copy()
            least_display['Revenue'] = least_display['Revenue'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(least_display, hide_index=True)

def show_delivery_analysis():
    """Página de análisis de performance de entregas"""
    st.header("🚚 Performance de Entregas")
    
    delivery_df = load_delivery_comparison()
    
    # Gráfico de comparación tiempos reales vs estimados
    st.subheader("⏱️ Tiempo Real vs Estimado de Entrega")
    
    # Filtrar datos válidos para 2016, 2017 y 2018
    months = delivery_df['month'].tolist()
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Año 2016', 'Año 2017', 'Año 2018'),
        vertical_spacing=0.08
    )
    
    # Datos 2016
    real_2016 = delivery_df['Year2016_real_time'].fillna(0)
    est_2016 = delivery_df['Year2016_estimated_time'].fillna(0)
    
    fig.add_trace(
        go.Scatter(x=months, y=real_2016, name='Real 2016', 
                  line=dict(color='darkred'), legendgroup="2016"),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=est_2016, name='Estimado 2016', 
                  line=dict(color='lightcoral', dash='dash'), legendgroup="2016"),
        row=1, col=1
    )
    
    # Datos 2017
    real_2017 = delivery_df['Year2017_real_time'].fillna(0)
    est_2017 = delivery_df['Year2017_estimated_time'].fillna(0)
    
    fig.add_trace(
        go.Scatter(x=months, y=real_2017, name='Real 2017', 
                  line=dict(color='blue'), legendgroup="2017"),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=est_2017, name='Estimado 2017', 
                  line=dict(color='lightblue', dash='dash'), legendgroup="2017"),
        row=2, col=1
    )
    
    # Datos 2018
    real_2018 = delivery_df['Year2018_real_time'].fillna(0)
    est_2018 = delivery_df['Year2018_estimated_time'].fillna(0)
    
    fig.add_trace(
        go.Scatter(x=months, y=real_2018, name='Real 2018', 
                  line=dict(color='orange'), legendgroup="2018"),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=est_2018, name='Estimado 2018', 
                  line=dict(color='moccasin', dash='dash'), legendgroup="2018"),
        row=3, col=1
    )
    
    fig.update_layout(height=900, title_text="Comparación de Tiempos de Entrega por Mes")
    fig.update_yaxes(title_text="Días", row=1, col=1)
    fig.update_yaxes(title_text="Días", row=2, col=1)
    fig.update_yaxes(title_text="Días", row=3, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas de performance
    st.subheader("📊 Métricas de Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcular métricas (solo con valores no nulos)
    avg_real_2016 = delivery_df['Year2016_real_time'].dropna().mean()
    avg_real_2017 = delivery_df['Year2017_real_time'].dropna().mean()
    avg_real_2018 = delivery_df['Year2018_real_time'].dropna().mean()
    avg_est_2016 = delivery_df['Year2016_estimated_time'].dropna().mean()
    avg_est_2017 = delivery_df['Year2017_estimated_time'].dropna().mean()
    
    with col1:
        if not pd.isna(avg_real_2016):
            st.metric(
                label="⏱️ Tiempo Promedio Real 2016",
                value=f"{avg_real_2016:.1f} días",
                delta=f"vs {avg_est_2016:.1f} días estimado"
            )
        else:
            st.metric(
                label="⏱️ Tiempo Promedio Real 2016",
                value="Sin datos",
                delta="Año de lanzamiento"
            )
    
    with col2:
        st.metric(
            label="⏱️ Tiempo Promedio Real 2017",
            value=f"{avg_real_2017:.1f} días",
            delta=f"vs {avg_est_2017:.1f} días estimado"
        )
    
    with col3:
        st.metric(
            label="⏱️ Tiempo Promedio Real 2018", 
            value=f"{avg_real_2018:.1f} días",
            delta=f"{((avg_real_2018-avg_real_2017)/avg_real_2017*100):+.1f}% vs 2017"
        )
    
    with col4:
        # Calcular precisión global de estimaciones (promedio de todos los años)
        accuracies = []
        
        # Agregar precisión 2016 si hay datos
        if not pd.isna(avg_real_2016) and not pd.isna(avg_est_2016) and avg_est_2016 > 0:
            accuracy_2016 = abs(avg_real_2016 - avg_est_2016) / avg_est_2016 * 100
            accuracies.append(100 - accuracy_2016)
        
        # Agregar precisión 2017
        if not pd.isna(avg_est_2017) and avg_est_2017 > 0:
            accuracy_2017 = abs(avg_real_2017 - avg_est_2017) / avg_est_2017 * 100
            accuracies.append(100 - accuracy_2017)
        
        # Agregar precisión 2018 si hay datos
        avg_est_2018 = delivery_df['Year2018_estimated_time'].dropna().mean()
        if not pd.isna(avg_real_2018) and not pd.isna(avg_est_2018) and avg_est_2018 > 0:
            accuracy_2018 = abs(avg_real_2018 - avg_est_2018) / avg_est_2018 * 100
            accuracies.append(100 - accuracy_2018)
        
        if accuracies:
            global_accuracy = sum(accuracies) / len(accuracies)
            st.metric(
                label="🎯 Precisión Global Entregas",
                value=f"{global_accuracy:.1f}%",
                delta=f"Promedio {len(accuracies)} años"
            )
        else:
            st.metric(
                label="🎯 Precisión Global Entregas",
                value="Calculando...",
                delta="En desarrollo"
            )

def show_geographic_analysis():
    """Página de análisis geográfico"""
    st.header("🗺️ Distribución Geográfica")
    
    states_df = load_revenue_by_state()
    
    # Gráfico de barras por estado
    st.subheader("💰 Ingresos por Estado")
    
    fig = px.bar(
        states_df.head(15),  # Top 15 estados
        x='customer_state',
        y='Revenue',
        title="Ingresos por Estado (Top 15)",
        labels={'Revenue': 'Ingresos ($)', 'customer_state': 'Estado'},
        color='Revenue',
        color_continuous_scale='blues'
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de concentración
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 5 Estados")
        top_states = states_df.head(5).copy()
        total_revenue = states_df['Revenue'].sum()
        top_states['Participación %'] = (top_states['Revenue'] / total_revenue * 100).round(1)
        top_states['Revenue'] = top_states['Revenue'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(top_states, hide_index=True)
    
    with col2:
        st.subheader("📊 Concentración de Mercado")
        
        # Calcular concentración
        top_3_pct = (states_df.head(3)['Revenue'].sum() / total_revenue * 100)
        top_5_pct = (states_df.head(5)['Revenue'].sum() / total_revenue * 100)
        
        st.metric("Top 3 Estados", f"{top_3_pct:.1f}%", "del total de ingresos")
        st.metric("Top 5 Estados", f"{top_5_pct:.1f}%", "del total de ingresos")
        
        # Insight sobre concentración
        if top_3_pct > 70:
            st.warning("⚠️ Alta concentración geográfica - Riesgo de dependencia")
        else:
            st.success("✅ Distribución geográfica balanceada")

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        📊 Olist E-commerce Analytics Dashboard | 
        Datos: 2016-2018 (Período Completo) | 
        Desarrollado con Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()