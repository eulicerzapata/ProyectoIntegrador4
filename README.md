

 **Crear entorno virtual**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

 **Instalar dependencias**:
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

### Dashboard Interactivo 📊
```bash
# Ejecutar dashboard de Streamlit
python run_dashboard.py
# o directamente:
streamlit run dashboard.py
```
El dashboard se abrirá en `http://localhost:8501` con visualizaciones interactivas.
