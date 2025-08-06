import streamlit as st
import pandas as pd

# Cargar los datos
df = pd.read_csv('ventas.csv', parse_dates=['Fecha'])

# Título
st.title("Análisis Multidimensional con OLAP - Streamlit")

# Mostrar el DataFrame
if st.checkbox("Mostrar datos originales"):
    st.dataframe(df)

# Filtros tipo Slice y Dice
st.sidebar.header("Filtros")
productos = st.sidebar.multiselect("Selecciona Producto(s)", options=df['Producto'].unique(), default=df['Producto'].unique())
regiones = st.sidebar.multiselect("Selecciona Región(es)", options=df['Región'].unique(), default=df['Región'].unique())
años = st.sidebar.multiselect("Selecciona Año(s)", options=df['Año'].unique(), default=df['Año'].unique())

# Aplicar filtros
df_filtrado = df[(df['Producto'].isin(productos)) & (df['Región'].isin(regiones)) & (df['Año'].isin(años))]

# Mostrar tabla filtrada
st.subheader("Datos filtrados")
st.dataframe(df_filtrado)

# Roll-up: Ventas por Año y Producto
st.subheader("Roll-up: Ventas por Año y Producto")
rollup = df_filtrado.groupby(['Año', 'Producto'])['Ventas'].sum().reset_index()
st.dataframe(rollup)

# Drill-down: Año, Mes y Producto
st.subheader("Drill-down: Ventas por Año, Mes y Producto")
drill = df_filtrado.groupby(['Año', 'Mes', 'Producto'])['Ventas'].sum().reset_index()
st.dataframe(drill)

# Pivot
st.subheader("Pivot: Región vs Producto")
pivot = df_filtrado.pivot_table(values='Ventas', index='Región', columns='Producto', aggfunc='sum', fill_value=0)
st.dataframe(pivot)

# Visualización simple
st.subheader("Gráfico: Total de Ventas por Región")
grafico = df_filtrado.groupby('Región')['Ventas'].sum()
st.bar_chart(grafico)
