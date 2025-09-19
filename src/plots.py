import matplotlib
import matplotlib.pyplot as plt

import plotly.express as px
import seaborn as sns

from pandas import DataFrame


def plot_revenue_by_month_year(df: DataFrame, year: int):
    """Plot revenue by month in a given year

    Args:
        df (DataFrame): Dataframe with revenue by month and year query result
        year (int): It could be 2016, 2017 or 2018
    """
    # Usar matplotlib directamente para evitar problemas con seaborn/pandas
    fig, ax1 = plt.subplots(figsize=(12, 6))

    months = df["month"].astype(str).tolist()
    values = df[f"Year{year}"].astype(float).tolist()

    # Línea de ingresos
    ax1.plot(months, values, marker="o", color="#1f77b4", label=f"Ingresos {year}")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Ingresos (R$)", color="#1f77b4")
    ax1.tick_params(axis="y", labelcolor="#1f77b4")

    # Barras en segundo eje (transparente)
    ax2 = ax1.twinx()
    bar_positions = range(len(months))
    ax2.bar(bar_positions, values, alpha=0.25, color="#ff7f0e", label=f"Ingresos {year} (bar)")
    ax2.set_ylabel("Ingresos (R$)", color="#ff7f0e")
    ax2.tick_params(axis="y", labelcolor="#ff7f0e")

    # Ajustar ticks x
    ax1.set_xticks(bar_positions)
    ax1.set_xticklabels(months, rotation=45)

    ax1.set_title(f"Ingresos por mes en {year}")
    ax1.grid(True, which="both", axis="y", linestyle="--", alpha=0.5)

    fig.tight_layout()
    plt.show()


def plot_real_vs_predicted_delivered_time(df: DataFrame, year: int):
    """Plot real vs predicted delivered time by month in a given year

    Args:
        df (DataFrame): Dataframe with real vs predicted delivered time by month and
                        year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    _, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}_real_time"], marker="o", sort=False, ax=ax1)
    ax1.twinx()
    g = sns.lineplot(
        data=df[f"Year{year}_estimated_time"], marker="o", sort=False, ax=ax1
    )
    g.set_xticks(range(len(df)))
    g.set_xticklabels(df.month.values)
    g.set(xlabel="month", ylabel="Average days delivery time", title="some title")
    ax1.set_title(f"Average days delivery time by month in {year}")
    ax1.legend(["Real time", "Estimated time"])

    plt.show()


def plot_global_amount_order_status(df: DataFrame):
    """Plot global amount of order status

    Args:
        df (DataFrame): Dataframe with global amount of order status query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["order_status"]]

    wedges, autotexts = ax.pie(df["Ammount"], textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Order Status",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Order Status Total")

    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.show()


def plot_revenue_per_state(df: DataFrame):
    """Plot revenue per state

    Args:
        df (DataFrame): Dataframe with revenue per state query result
    """
    fig = px.treemap(
        df, path=["customer_state"], values="Revenue", width=800, height=400
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_top_10_least_revenue_categories(df: DataFrame):
    """Plot top 10 least revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 least revenue categories query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Least Revenue Categories ammount")

    plt.show()


def plot_top_10_revenue_categories_ammount(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    # Plotting the top 10 revenue categories ammount
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Revenue Categories ammount")

    plt.show()


def plot_top_10_revenue_categories(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    fig = px.treemap(df, path=["Category"], values="Num_order", width=800, height=400)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_freight_value_weight_relationship(df: DataFrame):
    """Plot freight value weight relationship

    Args:
        df (DataFrame): Dataframe with freight value weight relationship query result
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    
    # Configurar el estilo
    matplotlib.rc_file_defaults()
    sns.set_style("whitegrid")
    
    # Crear la figura
    plt.figure(figsize=(12, 8))
    
    # Crear scatterplot con seaborn
    # Usando una muestra para mejor rendimiento visual
    sample_size = min(5000, len(df))  # Máximo 5000 puntos para mejor visualización
    df_sample = df.sample(n=sample_size, random_state=42)
    
    sns.scatterplot(data=df_sample, 
                   x='product_weight_g', 
                   y='freight_value', 
                   alpha=0.6, 
                   s=30)
    
    # Configurar títulos y etiquetas
    plt.title('Freight Value vs Product Weight Relationship', fontsize=16, fontweight='bold')
    plt.xlabel('Product Weight (grams)', fontsize=12)
    plt.ylabel('Freight Value (R$)', fontsize=12)
    
    # Agregar línea de tendencia
    try:
        z = np.polyfit(df_sample['product_weight_g'], df_sample['freight_value'], 1)
        p = np.poly1d(z)
        plt.plot(df_sample['product_weight_g'].sort_values(), 
                p(df_sample['product_weight_g'].sort_values()), 
                "r--", alpha=0.8, linewidth=2, label=f'Trend line')
        plt.legend()
    except:
        pass  # Si hay error en la línea de tendencia, continuar sin ella
    
    # Mejorar el layout
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_delivery_date_difference(df: DataFrame):
    """Plot delivery date difference

    Args:
        df (DataFrame): Dataframe with delivery date difference query result
    """
    sns.barplot(data=df, x="Delivery_Difference", y="State").set(
        title="Difference Between Delivery Estimate Date and Delivery Date"
    )


def plot_order_amount_per_day_with_holidays(df: DataFrame):
    """Plot order amount per day with holidays

    Args:
        df (DataFrame): Dataframe with order amount per day with holidays query result
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime
    
    # Convertir timestamp a fecha
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], unit='ms')
    
    # Crear la figura
    plt.figure(figsize=(15, 8))
    
    # Graficar la línea principal de pedidos por día
    plt.plot(df_copy['date'], df_copy['order_count'], 
             linewidth=1.5, color='steelblue', alpha=0.8)
    
    # Marcar los días festivos con líneas verticales rojas
    holidays = df_copy[df_copy['holiday'] == True]
    for _, holiday_row in holidays.iterrows():
        plt.axvline(x=holiday_row['date'], color='red', 
                   linestyle='--', alpha=0.7, linewidth=1)
    
    # Configurar el gráfico
    plt.title('Orders per Day and Holidays (2017)', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Orders', fontsize=12)
    
    # Formato del eje x
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=45)
    
    # Agregar leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='steelblue', linewidth=1.5, label='Daily Orders'),
        Line2D([0], [0], color='red', linestyle='--', linewidth=1, label='Holidays')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    # Mejorar el layout
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
