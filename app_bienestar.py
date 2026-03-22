import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Prevencionista del Bienestar", layout="wide")

# Título con estilo profesional
st.title("📊 Dashboard: Prevencionista del Bienestar")
st.markdown("---")

# 2. Configuración de la URL de Google Sheets (ID extraído de tu link)
SHEET_ID = "1fUxhdjjSZAbHV-4fUWfKuPTR1fd8esRBFr8R_RWeUDU"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

try:
    # 3. Carga de datos en tiempo real
    df = pd.read_csv(URL)
    
    # 4. Slicer de Mes en la barra lateral
    st.sidebar.header("Filtros de Control")
    if 'Mes' in df.columns:
        lista_meses = df['Mes'].unique()
        meses_seleccionados = st.sidebar.multiselect(
            "Selecciona el Mes:",
            options=lista_meses,
            default=lista_meses
        )
        
        # Filtrado de los datos
        df_filtrado = df[df['Mes'].isin(meses_seleccionados)]
    else:
        df_filtrado = df
        st.sidebar.error("Columna 'Mes' no encontrada.")

    # 5. Visualización de Resultados
    if not df_filtrado.empty:
        # Gráfico de Barras: Categoría vs Valor
        fig = px.bar(
            df_filtrado, 
            x="Categoría", 
            y="Valor", 
            color="Mes",
            title="Niveles de Bienestar por Categoría",
            barmode="group",
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        fig.update_layout(yaxis_range=[0, 100]) # Escala de 0 a 100
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla detallada
        st.subheader("📋 Detalle de Datos (Desde Google Sheets)")
        st.dataframe(df_filtrado, use_container_width=True)
        
    else:
        st.warning("Selecciona al menos un mes para visualizar los indicadores.")

except Exception as e:
    st.error(f"Error de conexión con Google Sheets: {e}")
    st.info("Verifica que el archivo esté compartido como 'Cualquier persona con el enlace'.")

st.markdown("---")
st.info("Desarrollado por Diógenes Leonel Tavarez - Industrial Engineer & Consultor")