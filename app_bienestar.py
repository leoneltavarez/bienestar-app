import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración básica
st.set_page_config(page_title="Dashboard Bienestar", layout="wide")
st.title("📊 Control Mensual de Bienestar")

# 2. Carga de datos
try:
    # Ruta para GitHub
    df = pd.read_excel("bienestar_data.xlsx")
    
    # 3. Slicer de Mes en la barra lateral
    st.sidebar.header("Configuración")
    
    # Usamos la columna 'Mes' que sí existe en tu Excel
    lista_meses = df['Mes'].unique()
    meses_seleccionados = st.sidebar.multiselect(
        "Selecciona el Mes:",
        options=lista_meses,
        default=lista_meses
    )
    
    # Filtrado de datos según el Slicer
    df_filtrado = df[df['Mes'].isin(meses_seleccionados)]

    # 4. Visualización de Gráficos
    if not df_filtrado.empty:
        # Gráfico de Barras usando 'Categoría' y 'Valor' (las columnas reales)
        fig = px.bar(
            df_filtrado, 
            x="Categoría", 
            y="Valor", 
            color="Mes",
            title="Niveles de Bienestar por Categoría",
            barmode="group",
            text_auto=True # Muestra el número sobre la barra
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. Tabla de datos filtrados
        st.subheader("Detalle de Registros")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("Por favor, selecciona al menos un mes en el menú lateral.")

except Exception as e:
    st.error(f"Error al cargar el sistema: {e}")

st.info("Desarrollado por Diógenes Leonel Tavarez")