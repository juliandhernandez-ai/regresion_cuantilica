import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Curva de Engel (1857) - Laboratorio Interactivo", layout="wide")
st.title("📈 Curva de Engel Cuantílica (Datos Reales de 1857)")
st.markdown("""
**Laboratorio interactivo** basado en la Figura 3 de Koenker y Hallock (2001). 
Base de datos histórica de Engel (1857): 235 hogares belgas.
""")

# ==========================================
# 2. CARGA DE DATOS
# ==========================================
@st.cache_data
def cargar_datos_engel():
    data = sm.datasets.engel.load_pandas().data
    return data.rename(columns={'income': 'Ingreso', 'foodexp': 'Gasto'})

df = cargar_datos_engel()

# ==========================================
# 3. FUNCIONES AUXILIARES
# ==========================================
def aplicar_estilo_limpio(fig, titulo, x_titulo, y_titulo):
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=22, color='black', family="Arial"),
                   x=0.5, xanchor='center'),
        xaxis=dict(
            title=dict(text=x_titulo, font=dict(size=18, color='black', family="Arial")),
            tickfont=dict(size=14, color='black'),
            showgrid=False, zeroline=False,
            showline=True, linecolor='black', linewidth=1
        ),
        yaxis=dict(
            title=dict(text=y_titulo, font=dict(size=18, color='black', family="Arial")),
            tickfont=dict(size=14, color='black'),
            showgrid=False, zeroline=False,
            showline=True, linecolor='black', linewidth=1
        ),
        plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=13, color='black')),
        margin=dict(l=80, r=60, t=100, b=80)
    )
    return fig

def caja_interpretacion(texto):
    """Caja azul con letra blanca para interpretaciones."""
    st.markdown(f"""
    <div style="background-color:#1E40AF; color:white; padding:18px; 
                border-radius:10px; margin-top:15px; font-size:15px;
                border-left:6px solid #60A5FA;">
        💡 <b>Interpretación:</b> {texto}
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. PESTAÑAS
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Datos", "📈 Distribuciones", "📦 Boxplot",
    "🔍 Heterogeneidad", "📊 Curvas de Engel", "🎯 Outlier Interactivo"
])

# ==========================================
# PESTAÑA 1: DATOS
# ==========================================
with tab1:
    st.subheader("📋 Base de Datos de Engel (1857)")
    st.markdown("Datos originales de 235 hogares belgas de la clase trabajadora.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Vista previa (primeras 15 filas):**")
        st.dataframe(df.head(15), use_container_width=True, height=400)
    with col2:
        st.markdown("**Resumen:**")
        st.metric("Total de hogares", len(df))
        st.metric("Ingreso promedio", f"{df['Ingreso'].mean():.0f} francos")
        st.metric("Gasto promedio", f"{df['Gasto'].mean():.0f} francos")
    
    st.subheader("Estadísticas Descriptivas")
    st.dataframe(df.describe().T, use_container_width=True)
    
    caja_interpretacion("""
    El ingreso promedio (≈1050) es mayor que el gasto promedio en alimentos (≈625). 
    Esto refleja que los hogares belgas de 1857 destinaban cerca del 60% de su ingreso 
    a alimentación, consistente con la Ley de Engel.
    """)

# ==========================================
# PESTAÑA 2: DISTRIBUCIONES
# ==========================================
with tab2:
    st.subheader("📈 Distribuciones de las Variables")
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        mostrar_hist_gasto = st.checkbox("Mostrar histograma de Gasto", value=False)
        mostrar_kde_gasto = st.checkbox("Mostrar densidad (KDE) de Gasto", value=False)
    with col_ctrl2:
        mostrar_hist_ingreso = st.checkbox("Mostrar histograma de Ingreso", value=False)
        mostrar_kde_ingreso = st.checkbox("Mostrar densidad (KDE) de Ingreso", value=False)
    
    def crear_hist_densidad(variable, color_hist, color_kde, titulo, x_titulo):
        fig = go.Figure()
        mostrar_hist = mostrar_hist_gasto if variable == 'Gasto' else mostrar_hist_ingreso
        mostrar_kde = mostrar_kde_gasto if variable == 'Gasto' else mostrar_kde_ingreso
        
        if mostrar_hist:
            fig.add_trace(go.Histogram(
                x=df[variable], name=f'Histograma {variable}',
                histnorm='probability density',
                marker_color=color_hist, opacity=0.6, nbinsx=30
            ))
        if mostrar_kde:
            kde = stats.gaussian_kde(df[variable])
            x_vals = np.linspace(df[variable].min(), df[variable].max(), 200)
            fig.add_trace(go.Scatter(
                x=x_vals, y=kde(x_vals), mode='lines',
                name=f'Densidad {variable}',
                line=dict(color=color_kde, width=3)
            ))
        fig = aplicar_estilo_limpio(fig, titulo, x_titulo, "Densidad")
        return fig
    
    col1, col2 = st.columns(2)
    with col1:
        if mostrar_hist_gasto or mostrar_kde_gasto:
            st.plotly_chart(crear_hist_densidad('Gasto', 'steelblue', 'darkblue',
                                                "Distribución del Gasto en Alimentos",
                                                "Gasto (Francos belgas)"),
                            use_container_width=True)
        else:
            st.info("👆 Activa el histograma o la densidad del Gasto.")
    with col2:
        if mostrar_hist_ingreso or mostrar_kde_ingreso:
            st.plotly_chart(crear_hist_densidad('Ingreso', 'seagreen', 'darkgreen',
                                                "Distribución del Ingreso del Hogar",
                                                "Ingreso (Francos belgas)"),
                            use_container_width=True)
        else:
            st.info("👆 Activa el histograma o la densidad del Ingreso.")
    
    if mostrar_hist_gasto or mostrar_kde_gasto or mostrar_hist_ingreso or mostrar_kde_ingreso:
        caja_interpretacion("""
        Ambas variables tienen <b>asimetría positiva</b> (cola larga a la derecha). 
        La mayoría de hogares se concentra en ingresos bajos (500–1500) y gastos bajos (300–800), 
        pero hay pocos hogares con valores muy altos. Esto justifica el uso de cuantiles: 
        la media no representa al hogar típico.
        """)

# ==========================================
# PESTAÑA 3: BOXPLOT
# ==========================================
with tab3:
    st.subheader("📦 Boxplot Comparativo")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        mostrar_box_gasto = st.checkbox("Mostrar boxplot de Gasto", value=False)
    with col_c2:
        mostrar_box_ingreso = st.checkbox("Mostrar boxplot de Ingreso", value=False)
    with col_c3:
        mostrar_media = st.checkbox("Mostrar media (punto)", value=False)
    
    if mostrar_box_gasto or mostrar_box_ingreso:
        fig = go.Figure()
        if mostrar_box_gasto:
            fig.add_trace(go.Box(
                y=df['Gasto'], name='Gasto',
                marker_color='steelblue',
                boxmean='sd' if mostrar_media else False
            ))
        if mostrar_box_ingreso:
            fig.add_trace(go.Box(
                y=df['Ingreso'], name='Ingreso',
                marker_color='seagreen',
                boxmean='sd' if mostrar_media else False
            ))
        fig = aplicar_estilo_limpio(fig, "Boxplot Comparativo: Gasto vs Ingreso",
                                    "Variable", "Francos belgas")
        st.plotly_chart(fig, use_container_width=True)
        
        caja_interpretacion("""
        La caja del <b>Ingreso</b> es más ancha y tiene más valores atípicos. 
        La mediana del ingreso (~850) supera a la del gasto (~580). 
        El <b>Gasto</b> tiene menor dispersión y menos outliers, porque la alimentación es 
        una necesidad acotada. La presencia de outliers justifica métodos robustos como la cuantílica.
        """)
    else:
        st.info("👆 Activa al menos un boxplot para visualizarlo.")

# ==========================================
# PESTAÑA 4: HETEROGENEIDAD
# ==========================================
with tab4:
    st.subheader("🔍 Evidencia de Heterogeneidad en el Efecto del Ingreso")
    
    cuantiles_all = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]
    modelos_all = {q: smf.quantreg('Gasto ~ Ingreso', data=df).fit(q=q) for q in cuantiles_all}
    modelo_mco_all = smf.ols('Gasto ~ Ingreso', data=df).fit()
    
    mostrar_metricas = st.checkbox("Mostrar métricas comparativas (0.05 vs 0.95 vs MCO)", value=False)
    mostrar_barras = st.checkbox("Mostrar gráfico de barras de pendientes", value=False)
    mostrar_tabla = st.checkbox("Mostrar tabla completa de coeficientes", value=False)
    
    p05 = modelos_all[0.05].params['Ingreso']
    p95 = modelos_all[0.95].params['Ingreso']
    p_mco = modelo_mco_all.params['Ingreso']
    diff = p95 - p05
    ratio = p95 / p05 if p05 != 0 else np.nan
    
    if mostrar_metricas:
        col1, col2, col3 = st.columns(3)
        col1.metric("Pendiente Cuantil 0.05", f"{p05:.4f}")
        col2.metric("Pendiente MCO", f"{p_mco:.4f}")
        col3.metric("Pendiente Cuantil 0.95", f"{p95:.4f}", delta=f"{diff:.4f}")
        
        caja_interpretacion(f"""
        La pendiente del cuantil <b>0.95</b> ({p95:.4f}) es <b>{ratio:.2f} veces mayor</b> 
        que la del cuantil <b>0.05</b> ({p05:.4f}). Esto significa que el ingreso impacta 
        mucho más fuerte en los hogares que ya gastan mucho. El MCO ({p_mco:.4f}) da un 
        solo número promedio que oculta esta heterogeneidad.
        """)
    
    if mostrar_barras:
        pendientes_df = pd.DataFrame([
            {"Cuantil": str(q), "Pendiente": modelos_all[q].params['Ingreso']}
            for q in cuantiles_all
        ])
        pendientes_df = pd.concat([
            pd.DataFrame([{"Cuantil": "MCO", "Pendiente": p_mco}]),
            pendientes_df
        ], ignore_index=True)
        
        # Mapa de colores: MCO en gris, cuantiles con colores distintos
        mapa_colores = {
            "MCO": "#808080",
            "0.05": "#66C2A5", "0.1": "#FC8D62", "0.25": "#8DA0CB",
            "0.5": "#E78AC3", "0.75": "#A6D854", "0.9": "#FFD92F", "0.95": "#E5C494"
        }
        
        fig = px.bar(pendientes_df, x="Cuantil", y="Pendiente",
                     color="Cuantil", text_auto='.4f',
                     color_discrete_map=mapa_colores)
        fig = aplicar_estilo_limpio(fig, "Pendiente del Ingreso por Cuantil (vs MCO)",
                                    "Modelo / Cuantil", "Pendiente estimada")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        caja_interpretacion("""
        Las barras muestran una tendencia <b>creciente</b>: a mayor cuantil, mayor pendiente. 
        La barra <b>gris (MCO)</b> queda en un punto intermedio que no representa ni a los 
        hogares pobres ni a los ricos.
        """)
    
    if mostrar_tabla:
        coef_data = [{
            "Cuantil": q,
            "Intercepto": round(modelos_all[q].params['Intercept'], 2),
            "Pendiente": round(modelos_all[q].params['Ingreso'], 4)
        } for q in cuantiles_all]
        st.dataframe(pd.DataFrame(coef_data), hide_index=True, use_container_width=True)

# ==========================================
# PESTAÑA 5: CURVAS DE ENGEL
# ==========================================
with tab5:
    st.subheader("📊 Curvas de Engel - Construcción Paso a Paso")
    st.markdown("Activa cada elemento para construir el gráfico desde cero.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**1. Nube de puntos:**")
        mostrar_puntos = st.checkbox("Mostrar nube de puntos", value=False, key="ptos")
        st.markdown("**2. Línea MCO (promedio):**")
        mostrar_mco_linea = st.checkbox("Mostrar línea MCO", value=False, key="mco")
    with col_b:
        st.markdown("**3. Cuantiles (selecciona cuáles mostrar):**")
        cuantiles_sel = st.multiselect(
            "Cuantiles activos:",
            options=[0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95],
            default=[]
        )
    
    modelos_sel = {q: smf.quantreg('Gasto ~ Ingreso', data=df).fit(q=q) for q in cuantiles_sel}
    modelo_mco_sel = smf.ols('Gasto ~ Ingreso', data=df).fit()
    
    fig = go.Figure()
    x_range = np.linspace(df['Ingreso'].min(), df['Ingreso'].max(), 100)
    
    if mostrar_puntos:
        fig.add_trace(go.Scatter(
            x=df['Ingreso'], y=df['Gasto'],
            mode='markers', name='Datos',
            marker=dict(color='black', opacity=0.6, size=7)
        ))
    
    if mostrar_mco_linea:
        y_mco = modelo_mco_sel.params['Intercept'] + modelo_mco_sel.params['Ingreso'] * x_range
        fig.add_trace(go.Scatter(
            x=x_range, y=y_mco, mode='lines', name='MCO (Promedio)',
            line=dict(color='red', dash='dash', width=2.5)
        ))
    
    colores = px.colors.qualitative.Dark24
    for i, (q, modelo) in enumerate(modelos_sel.items()):
        y_qr = modelo.params['Intercept'] + modelo.params['Ingreso'] * x_range
        grosor = 3.5 if q == 0.5 else 1.8
        fig.add_trace(go.Scatter(
            x=x_range, y=y_qr, mode='lines', name=f'Cuantil {q}',
            line=dict(color=colores[i % len(colores)], width=grosor)
        ))
    
    fig = aplicar_estilo_limpio(
        fig, "Curvas de Engel para Alimentos (1857)",
        "Ingreso del Hogar (Francos belgas)",
        "Gasto en Alimentos (Francos belgas)"
    )
    fig.update_xaxes(range=[0, 5500])
    fig.update_yaxes(range=[0, 2200])
    
    if len(fig.data) > 0:
        st.plotly_chart(fig, use_container_width=True)
        
        try:
            img_bytes = fig.to_image(format="pdf", width=1200, height=800, scale=2)
            st.download_button(
                label="📥 Descargar gráfico actual en PDF",
                data=img_bytes,
                file_name="curva_engel.pdf",
                mime="application/pdf"
            )
        except Exception:
            st.warning("Para descargar PDF, instala: `pip install -U kaleido`")
        
        caja_interpretacion("""
        Las líneas se <b>abren en abanico</b> hacia la derecha (heterocedasticidad). 
        Las líneas superiores están más juntas (cola corta) y las inferiores más separadas 
        (cola larga): la distribución está <b>sesgada a la izquierda</b>. 
        La línea MCO (roja discontinua) solo captura el promedio.
        """)
    else:
        st.info("👆 Activa al menos un elemento para ver el gráfico.")
    
    # ---- TABLA DE ECUACIONES ----
       
    st.markdown("---")
    st.markdown("### 📐 Ecuaciones Estimadas del Modelo")
    st.markdown("Notación general: $Q_\\tau(Y \\mid X) = \\beta_0(\\tau) + \\beta_1(\\tau) \\cdot X$")
    
    # Construir filas de la tabla en Markdown con LaTeX
    filas_md = []
    
    # Fila MCO
    b0 = modelo_mco_sel.params['Intercept']
    b1 = modelo_mco_sel.params['Ingreso']
    filas_md.append(
        f"| **MCO (media)** | $E[Y \\mid X] = {b0:.2f} + {b1:.4f} \\cdot X$ |"
    )
    
    # Filas cuantílicas (solo las seleccionadas)
    for q in sorted(modelos_sel.keys()):
        m = modelos_sel[q]
        b0_q = m.params['Intercept']
        b1_q = m.params['Ingreso']
        filas_md.append(
            f"| **Cuantil** $\\tau = {q}$ | $Q_{{{q}}}(Y \\mid X) = {b0_q:.2f} + {b1_q:.4f} \\cdot X$ |"
        )
    
    tabla_md = "| Modelo | Ecuación |\n|---|---|\n" + "\n".join(filas_md)
    st.markdown(tabla_md)
# ==========================================
# PESTAÑA 6: OUTLIER INTERACTIVO
# ==========================================
with tab6:
    st.subheader("🎯 ¿Cómo afecta un valor atípico a la recta MCO?")
    st.markdown("""
    Mueve los **sliders** para cambiar la posición de un punto atípico. Observa cómo la 
    **línea roja (MCO)** se "tuerce" mientras la **línea negra gruesa (mediana cuantílica)** resiste.
    """)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        x_outlier = st.slider("Posición X del outlier (Ingreso)", 
                              min_value=500, max_value=5000, value=4500, step=100)
    with col_s2:
        y_outlier = st.slider("Posición Y del outlier (Gasto)", 
                              min_value=100, max_value=3000, value=300, step=50)
    
    col_chk1, col_chk2, col_chk3 = st.columns(3)
    with col_chk1:
        mostrar_mediana_out = st.checkbox("Mostrar mediana cuantílica (robusta)", value=False)
    with col_chk2:
        mostrar_ols_sin = st.checkbox("Mostrar MCO sin el outlier (referencia)", value=False)
    with col_chk3:
        mostrar_puntos_orig = st.checkbox("Mostrar nube de puntos original", value=False)
    
    df_out = pd.concat([
        df,
        pd.DataFrame([{'Ingreso': x_outlier, 'Gasto': y_outlier}])
    ], ignore_index=True)
    
    mco_con = smf.ols('Gasto ~ Ingreso', data=df_out).fit()
    mco_sin = smf.ols('Gasto ~ Ingreso', data=df).fit()
    med_con = smf.quantreg('Gasto ~ Ingreso', data=df_out).fit(q=0.5)
    
    fig2 = go.Figure()
    
    if mostrar_puntos_orig:
        fig2.add_trace(go.Scatter(
            x=df['Ingreso'], y=df['Gasto'], mode='markers',
            name='Datos originales',
            marker=dict(color='gray', opacity=0.5, size=6)
        ))
    
    fig2.add_trace(go.Scatter(
        x=[x_outlier], y=[y_outlier], mode='markers',
        name='Outlier',
        marker=dict(color='red', size=15, symbol='star',
                    line=dict(color='black', width=1))
    ))
    
    x_range2 = np.linspace(0, 5500, 100)
    
    y_mco_con = mco_con.params['Intercept'] + mco_con.params['Ingreso'] * x_range2
    fig2.add_trace(go.Scatter(
        x=x_range2, y=y_mco_con, mode='lines',
        name='MCO con outlier',
        line=dict(color='red', width=3)
    ))
    
    if mostrar_ols_sin:
        y_mco_sin = mco_sin.params['Intercept'] + mco_sin.params['Ingreso'] * x_range2
        fig2.add_trace(go.Scatter(
            x=x_range2, y=y_mco_sin, mode='lines',
            name='MCO sin outlier',
            line=dict(color='orange', dash='dash', width=2)
        ))
    
    if mostrar_mediana_out:
        y_med = med_con.params['Intercept'] + med_con.params['Ingreso'] * x_range2
        fig2.add_trace(go.Scatter(
            x=x_range2, y=y_med, mode='lines',
            name='Mediana (cuantil 0.5)',
            line=dict(color='black', width=3.5)
        ))
    
    fig2 = aplicar_estilo_limpio(
        fig2, "Efecto del Outlier sobre MCO vs Cuantílica",
        "Ingreso del Hogar (Francos belgas)",
        "Gasto en Alimentos (Francos belgas)"
    )
    fig2.update_xaxes(range=[0, 5500])
    fig2.update_yaxes(range=[0, 3200])
    st.plotly_chart(fig2, use_container_width=True)
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Pendiente MCO (con outlier)", f"{mco_con.params['Ingreso']:.4f}")
    col_b.metric("Pendiente MCO (sin outlier)", f"{mco_sin.params['Ingreso']:.4f}",
                 delta=f"{mco_con.params['Ingreso'] - mco_sin.params['Ingreso']:+.4f}")
    col_c.metric("Pendiente Mediana", f"{med_con.params['Ingreso']:.4f}",
                 delta=f"{med_con.params['Ingreso'] - mco_sin.params['Ingreso']:+.4f}")
    
    # ---- ECUACIONES DINÁMICAS ----
    st.markdown("---")
    st.markdown("### 📐 Ecuaciones de las Rectas (actualizadas en tiempo real)")
    
    # MCO con outlier
    b0_mco = mco_con.params['Intercept']
    b1_mco = mco_con.params['Ingreso']
    # Mediana
    b0_med = med_con.params['Intercept']
    b1_med = med_con.params['Ingreso']
    # MCO sin outlier
    b0_sin = mco_sin.params['Intercept']
    b1_sin = mco_sin.params['Ingreso']
    
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.markdown("**🔴 MCO (media) con outlier:**")
        st.latex(rf"\hat{{Y}} = {b0_mco:.2f} + {b1_mco:.4f} \cdot X")
    with col_e2:
        st.markdown("**🟠 MCO (media) sin outlier:**")
        st.latex(rf"\hat{{Y}} = {b0_sin:.2f} + {b1_sin:.4f} \cdot X")
    with col_e3:
        st.markdown("**⚫ Mediana (cuantil τ = 0.5):**")
        st.latex(rf"\hat{{Q}}_{{0.5}}(Y \mid X) = {b0_med:.2f} + {b1_med:.4f} \cdot X")