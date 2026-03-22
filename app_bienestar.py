import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración
st.set_page_config(page_title="Prevencionista del Bienestar", layout="wide")

st.title("📊 Dashboard: Prevencionista del Bienestar")
st.markdown("---")

try:
    # Carga de datos
    df = pd.read_excel("bienestar_data.xlsx")
    
    # --- FILTROS EN EL SIDEBAR ---
    st.sidebar.header("Filtros de Control")
    
    # Filtro de Mes
    meses = df['Mes'].unique() if 'Mes' in df.columns else []
    mes_sel = st.sidebar.multiselect("Selecciona el Mes:", options=meses, default=meses)
    
    # Filtro de Categoría (Opcional, si lo tienes)
    cats = df['Categoría'].unique() if 'Categoría' in df.columns else []
    cat_sel = st.sidebar.multiselect("Selecciona Categoría:", options=cats, default=cats)

    # --- LA CONEXIÓN CRÍTICA (Filtrado de datos) ---
    # Aquí creamos el sub-conjunto de datos basado en lo que elegiste en el slicer
    df_selection = df[df['Mes'].isin(mes_sel)]
    if cat_sel:
        df_selection = df_selection[df_selection['Categoría'].isin(cat_sel)]

    # --- MÉTRICAS ---
    col1, col2 = st.columns(2)
    col1.metric("Datos en Pantalla", len(df_selection))
    col2.info("Usa el menú de la izquierda para filtrar por mes.")

    # --- GRÁFICOS (Ahora usando df_selection) ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📈 Análisis por Alimento")
        # IMPORTANTE: Aquí usamos df_selection para que el gráfico responda al filtro
        if not df_selection.empty:
            fig_bar = px.bar(df_selection, x="Alimento", y="IG", color="Mes",
                             title="Índice Glucémico Seleccionado",
                             barmode="group")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No hay datos para los meses seleccionados.")

    with c2:
        st.subheader("🕸️ Perfil de Bienestar")
        if not df_selection.empty and 'Categoría' in df_selection.columns:
            # Agrupamos los datos filtrados para el radar
            radar_data = df_selection.groupby('Categoría')['Valor'].mean().reset_index()
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_data['Valor'],
                theta=radar_data['Categoría'],
                fill='toself',
                line_color='#00CC96'
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
            st.plotly_chart(fig_radar, use_container_width=True)

    # Tabla de datos (también filtrada)
    st.markdown("### 📋 Vista Previa de la Selección")
    st.dataframe(df_selection, use_container_width=True)

except Exception as e:
    st.error(f"Error en la lógica de filtrado: {e}")

st.info("Desarrollado por Diógenes Leonel Tavarez - Industrial Engineer")