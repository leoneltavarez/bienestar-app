import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Prevencionista del Bienestar", layout="wide")

# Título Principal
st.title("📊 Dashboard: Prevencionista del Bienestar")
st.markdown("---")

# --- CARGA DE DATOS (Cambio clave para GitHub/Streamlit Cloud) ---
try:
    # Eliminamos la ruta de C:\ para que funcione en la web
    nombre_archivo = "bienestar_data.xlsx"
    df = pd.read_excel(nombre_archivo)
    
    # --- FILTROS ---
    st.sidebar.header("Filtros de Control")
    # Asumiendo que tienes una columna llamada 'Categoría' o similar
    if 'Categoría' in df.columns:
        categoria = st.sidebar.multiselect("Selecciona Categoría:", 
                                           options=df["Categoría"].unique(),
                                           default=df["Categoría"].unique())
        df_selection = df.query("Categoría == @categoria")
    else:
        df_selection = df

    # --- MÉTRICAS PRINCIPALES ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df_selection))
    with col2:
        # Ejemplo: Promedio de Índice Glucémico si existe la columna 'IG'
        if 'IG' in df.columns:
            st.metric("Promedio IG", round(df_selection["IG"].mean(), 2))
    with col3:
        st.success("Estado: Activo")

    # --- GRÁFICOS ---
    st.markdown("### Análisis Visual")
    c1, c2 = st.columns(2)

    with c1:
        if 'Alimento' in df.columns and 'IG' in df.columns:
            fig_bar = px.bar(df_selection, x="Alimento", y="IG", title="Índice Glucémico por Alimento")
            st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.write("#### Tabla de Datos Seleccionados")
        st.dataframe(df_selection, use_container_width=True)

except FileNotFoundError:
    st.error(f"❌ No se encontró el archivo '{nombre_archivo}'. Asegúrate de que esté subido a GitHub junto con este código.")
except Exception as e:
    st.error(f"⚠️ Ocurrió un error: {e}")

st.info("Desarrollado por Diógenes Leonel Tavarez - Industrial Engineer")