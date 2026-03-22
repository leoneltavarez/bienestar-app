import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(page_title="Control Bienestar", layout="wide")
st.title("📊 Control Mensual de Bienestar")

# 2. Carga de datos
try:
    # Leemos el archivo que ya tienes en GitHub
    df = pd.read_excel("bienestar_data.xlsx")
    
    # 3. Lógica del Slicer (Barra Lateral)
    st.sidebar.header("Configuración")
    
    # Extraemos los meses únicos (Enero, Febrero)
    lista_meses = df['Mes'].unique()
    meses_seleccionados = st.sidebar.multiselect(
        "Selecciona el Mes:",
        options=lista_meses,
        default=lista_meses
    )
    
    # --- LA CONEXIÓN CLAVE ---
    # Filtramos los datos ANTES de graficar
    df_filtrado = df[df['Mes'].isin(meses_seleccionados)]

    # 4. Creación del Gráfico
    if not df_filtrado.empty:
        # Usamos 'Categoría' para el eje X y 'Valor' para el eje Y
        fig = px.bar(
            df_filtrado, 
            x="Categoría", 
            y="Valor", 
            color="Mes",
            title="Resultados por Categoría y Mes",
            barmode="group",
            text_auto=True,
            color_discrete_map={"Enero": "#ef553b", "Febrero": "#636efa"} # Colores fijos
        )
        
        # Ajuste visual del gráfico
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. Tabla de datos debajo
        st.subheader("Registros Seleccionados")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("⚠️ Selecciona al menos un mes en el menú de la izquierda para ver los datos.")

except Exception as e:
    st.error(f"Hubo un problema con los nombres de las columnas: {e}")

st.info("Desarrollado por Diógenes Leonel Tavarez - Industrial Engineer")