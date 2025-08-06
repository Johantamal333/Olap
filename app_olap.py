import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la app
st.title("Análisis OLAP - Ventas por Producto, Región y Año")

# Cargar los datos desde un archivo CSV
archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
if archivo is not None:
    df = pd.read_csv(archivo)

    # Convertir columna Fecha a tipo datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    # Eliminar filas con fechas inválidas
    df = df.dropna(subset=['Fecha'])

    # Crear columna Año
    df['Año'] = df['Fecha'].dt.year

    # Filtros interactivos
    años = st.sidebar.multiselect("Selecciona Año(s)", options=sorted(df['Año'].unique()), default=sorted(df['Año'].unique()))
    productos = st.sidebar.multiselect("Selecciona Producto(s)", options=df['Producto'].unique(), default=df['Producto'].unique())
    regiones = st.sidebar.multiselect("Selecciona Región(es)", options=df['Región'].unique(), default=df['Región'].unique())

    # Filtrar datos
    df_filtrado = df[
        (df['Año'].isin(años)) &
        (df['Producto'].isin(productos)) &
        (df['Región'].isin(regiones))
    ]

    # Mostrar tabla dinámica
    st.subheader("Resumen de Ventas")
    tabla = pd.pivot_table(
        df_filtrado,
        values='Ventas',
        index=['Año', 'Producto'],
        columns='Región',
        aggfunc='sum',
        fill_value=0
    )
    st.dataframe(tabla)

    # Gráfica de barras
    st.subheader("Gráfica de Ventas por Producto y Año")
    grafica = df_filtrado.groupby(['Año', 'Producto'])['Ventas'].sum().reset_index()
    fig = px.bar(grafica, x='Producto', y='Ventas', color='Año', barmode='group')
    st.plotly_chart(fig)
