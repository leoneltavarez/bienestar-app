import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración profesional
st.set_page_config(page_title="Prevencionista del Bienestar", layout="wide")

# 1. RUTA DEL ARCHIVO (Asegúrate de que el nombre coincida aquí)
ruta_excel = r"C:\PROYECTOS_INGENIERIA\bienestar_data.xlsx"

try:
    df = pd.read_excel(ruta_excel, sheet_name="Data")
    
    st.title("🌿 Dashboard: Prevencionista del Bienestar")
    st.markdown("---")

    # 2. SLICER (Filtro lateral)
    st.sidebar.header("Filtros")
    mes_sel = st.sidebar.selectbox("Selecciona el Mes:", df['Mes'].unique())
    df_filtrado = df[df['Mes'] == mes_sel]

    # 3. INTERFAZ DE COLUMNAS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Cumplimiento en {mes_sel}")
        # Gráfico de Barras
        fig_bar = px.bar(df_filtrado, x='Categoría', y='Valor', 
                         color='Categoría', text_auto=True,
                         color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Gráfico de Araña (Balance)")
        # Gráfico de Araña (Radar)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=df_filtrado['Valor'],
            theta=df_filtrado['Categoría'],
            fill='toself',
            name=mes_sel,
            line_color='teal'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        st.plotly_chart(fig_radar, use_container_width=True)

except Exception as e:
    st.error(f"Error técnico: No se encuentra el archivo 'bienestar_data.xlsx' en la ruta especificada.")
    st.info("Asegúrate de que el archivo esté en C:\\PROYECTOS_INGENIERIA\\ y se llame exactamente así.")