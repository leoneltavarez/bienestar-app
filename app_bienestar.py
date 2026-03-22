import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Prevencionista del Bienestar", layout="wide")

# Título Principal con Emoji
st.title("📊 Dashboard: Prevencionista del Bienestar")
st.markdown("---")

# --- CARGA DE DATOS ---
try:
    # Ruta relativa para que funcione en la web
    df = pd.read_excel("bienestar_data.xlsx")
    
    # --- SIDEBAR / FILTROS (Slicer por Mes y Categoría) ---
    st.sidebar.header("Filtros de Control")
    
    # Slicer de Mes
    meses = df['Mes'].unique() if 'Mes' in df.columns else []
    mes_sel = st.sidebar.multiselect("Selecciona el Mes:", options=meses, default=meses)
    
    # Slicer de Categoría
    cats = df['Categoría'].unique() if 'Categoría' in df.columns else []
    cat_sel = st.sidebar.multiselect("Selecciona Categoría:", options=cats, default=cats)

    # Filtrado dinámico
    df_selection = df[df['Mes'].isin(mes_sel) & df['Categoría'].isin(cat_sel)]

    # --- MÉTRICAS PRINCIPALES ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registros", len(df_selection))
    if 'Valor' in df_selection.columns:
        col2.metric("Promedio Valor", round(df_selection['Valor'].mean(), 1))
    col3.success("Estado: Activo en la Nube")

    st.markdown("---")

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📈 Análisis de Barras")
        # Gráfico de Barras: Categoría vs Valor
        fig_bar = px.bar(df_selection, x="Categoría", y="Valor", color="Mes",
                         title="Desempeño por Categoría", barmode="group",
                         color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("🕸️ Gráfico de Araña (Radar)")
        # Gráfico de Araña
        categorias_radar = df_selection['Categoría'].unique()
        valores_radar = [df_selection[df_selection['Categoría'] == c]['Valor'].mean() for c in categorias_radar]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=valores_radar,
            theta=categorias_radar,
            fill='toself',
            name='Perfil de Bienestar',
            line_color='#FF4B4B'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- TABLA ---
    st.markdown("### 📋 Tabla de Datos Seleccionados")
    st.dataframe(df_selection, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar datos: {e}")

st.info("Desarrollado por Diógenes Leonel Tavarez - Industrial Engineer")