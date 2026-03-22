import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración básica
st.set_page_config(page_title="Dashboard Bienestar", layout="wide")
st.title("📊 Control Mensual de Bienestar")

# 2. Carga de datos
try:
    # Ruta relativa para GitHub
    df = pd.read_excel("bienestar_data.xlsx")
    
    # 3. Slicer de Mes en la barra lateral
    st.sidebar.header("Configuración")
    if 'Mes' in df.columns:
        lista_meses = df['Mes'].unique()
        meses_seleccionados = st.sidebar.multiselect(
            "Selecciona el Mes:",
            options=lista_meses,
            default=lista_meses  # Por defecto muestra todos (Enero y Febrero)
        )
        
        # FILTRADO CRÍTICO: Aquí es donde se conectan los datos con el Slicer
        df_filtrado = df[df['Mes'].isin(meses_seleccionados)]
    else:
        df_filtrado = df
        st.error("No se encontró la columna 'Mes' en el Excel.")

    # 4. Visualización de Gráficos
    if not df_filtrado.empty:
        # Gráfico de Barras Simple
        # Nota: Asegúrate que las columnas 'Alimento' e 'IG' existan en tu Excel
        # Si tus columnas se llaman distinto, cambia los nombres abajo:
        fig = px.bar(
            df_filtrado, 
            x="Alimento", 
            y="IG", 
            color="Mes",
            title="Índice Glucémico por Mes Seleccionado",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. Tabla de datos filtrados
        st.subheader("Datos detallados")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("Selecciona al menos un mes en el menú de la izquierda.")

except Exception as e:
    st.error(f"Error al cargar el sistema: {e}")

st.info("Desarrollado por Diógenes Leonel Tavarez")