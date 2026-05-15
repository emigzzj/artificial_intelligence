import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CEMEX | Talent Score Hub",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CEMEX BRAND COLORS ────────────────────────────────────────────────────────
CEMEX_BLUE   = "#0000b3"
CEMEX_RED    = "#f22331"
CEMEX_SKY    = "#398ef4"
CEMEX_GREEN  = "#53cc80"
CEMEX_PURPLE = "#9a4cf5"
CEMEX_ORANGE = "#ffb000"
CEMEX_GRAY   = "#3d3d3d"
CEMEX_LIGHT  = "#f0f4ff"

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] {{
      font-family: 'Barlow', sans-serif;
      background-color: #f5f7ff;
  }}

  /* ── HEADER ── */
  .cemex-header {{
      background: linear-gradient(135deg, {CEMEX_BLUE} 0%, #0008d4 60%, {CEMEX_SKY} 100%);
      border-radius: 16px;
      padding: 2rem 2.5rem;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      gap: 2rem;
      box-shadow: 0 8px 32px rgba(0,0,179,0.25);
      position: relative;
      overflow: hidden;
  }}
  .cemex-header::before {{
      content: '';
      position: absolute;
      top: -40px; right: -40px;
      width: 200px; height: 200px;
      background: rgba(255,255,255,0.07);
      border-radius: 50%;
  }}
  .cemex-header::after {{
      content: '';
      position: absolute;
      bottom: -60px; right: 80px;
      width: 300px; height: 120px;
      background: rgba(242,35,49,0.15);
      border-radius: 50%;
  }}
  .header-title {{
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 2.6rem;
      font-weight: 800;
      color: white;
      line-height: 1;
      letter-spacing: -0.5px;
  }}
  .header-sub {{
      font-size: 1rem;
      color: rgba(255,255,255,0.75);
      margin-top: 0.4rem;
      font-weight: 300;
  }}
  .header-badge {{
      background: {CEMEX_RED};
      color: white;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-top: 0.5rem;
      display: inline-block;
  }}

  /* ── METRIC CARDS ── */
  .metric-row {{
      display: flex;
      gap: 1rem;
      margin-bottom: 1.5rem;
  }}
  .metric-card {{
      flex: 1;
      background: white;
      border-radius: 14px;
      padding: 1.25rem 1.5rem;
      box-shadow: 0 2px 12px rgba(0,0,0,0.07);
      border-left: 5px solid {CEMEX_BLUE};
      transition: transform 0.2s;
  }}
  .metric-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,179,0.12); }}
  .metric-card.red  {{ border-left-color: {CEMEX_RED}; }}
  .metric-card.green{{ border-left-color: {CEMEX_GREEN}; }}
  .metric-card.orange{{ border-left-color: {CEMEX_ORANGE}; }}
  .metric-label {{ font-size: 0.78rem; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.8px; }}
  .metric-value {{ font-family: 'Barlow Condensed', sans-serif; font-size: 2.2rem; font-weight: 800; color: {CEMEX_BLUE}; line-height: 1.1; }}
  .metric-card.red  .metric-value {{ color: {CEMEX_RED}; }}
  .metric-card.green .metric-value {{ color: #2a9f5a; }}
  .metric-card.orange .metric-value {{ color: #cc8800; }}
  .metric-delta {{ font-size: 0.82rem; color: #aaa; margin-top: 0.1rem; }}

  /* ── SECTION TITLES ── */
  .section-title {{
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 1.5rem;
      font-weight: 700;
      color: {CEMEX_BLUE};
      border-bottom: 3px solid {CEMEX_RED};
      padding-bottom: 0.4rem;
      margin-bottom: 1.2rem;
      display: inline-block;
  }}

  /* ── SCORE BADGE ── */
  .score-pill {{
      display: inline-block;
      padding: 0.2rem 0.7rem;
      border-radius: 20px;
      font-weight: 700;
      font-size: 0.95rem;
      color: white;
  }}
  .score-high  {{ background: #2a9f5a; }}
  .score-mid   {{ background: {CEMEX_ORANGE}; color: {CEMEX_GRAY}; }}
  .score-low   {{ background: {CEMEX_RED}; }}

  /* ── SIDEBAR ── */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, {CEMEX_BLUE} 0%, #0005aa 100%);
  }}
  [data-testid="stSidebar"] * {{ color: white !important; }}
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stSlider label,
  [data-testid="stSidebar"] .stCheckbox label {{
      color: rgba(255,255,255,0.85) !important;
      font-weight: 500;
      font-size: 0.88rem;
  }}
  [data-testid="stSidebar"] .stButton button {{
      background: {CEMEX_RED} !important;
      color: white !important;
      border: none !important;
      border-radius: 8px !important;
      font-weight: 700 !important;
      font-size: 1rem !important;
      width: 100%;
      padding: 0.65rem !important;
      margin-top: 0.5rem;
      letter-spacing: 0.5px;
  }}
  [data-testid="stSidebar"] .stButton button:hover {{
      background: #c8000e !important;
      transform: translateY(-1px);
  }}
  .sidebar-section {{
      background: rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 0.9rem 1rem;
      margin-bottom: 0.8rem;
  }}
  .sidebar-section-title {{
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: rgba(255,255,255,0.55) !important;
      margin-bottom: 0.5rem;
  }}
  .sidebar-logo {{
      text-align: center;
      padding: 1rem 0 0.5rem;
  }}

  /* ── TABLE ── */
  .rank-table {{ width: 100%; border-collapse: collapse; }}
  .rank-table th {{
      background: {CEMEX_BLUE};
      color: white;
      padding: 0.75rem 1rem;
      text-align: left;
      font-size: 0.82rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
  }}
  .rank-table td {{
      padding: 0.65rem 1rem;
      border-bottom: 1px solid #eef0f8;
      font-size: 0.9rem;
      color: {CEMEX_GRAY};
  }}
  .rank-table tr:nth-child(even) td {{ background: #f8f9ff; }}
  .rank-table tr:hover td {{ background: #eef2ff; }}
  .rank-num {{
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 1.3rem;
      font-weight: 800;
      color: {CEMEX_BLUE};
  }}
  .rank-num.gold   {{ color: #d4a000; }}
  .rank-num.silver {{ color: #888; }}
  .rank-num.bronze {{ color: #a0522d; }}

  /* ── FILTER CHIP ── */
  .filter-active {{
      background: {CEMEX_BLUE};
      color: white;
      padding: 0.2rem 0.6rem;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 600;
      display: inline-block;
      margin: 0.1rem;
  }}

  /* ── TABS ── */
  .stTabs [data-baseweb="tab-list"] {{ gap: 2px; }}
  .stTabs [data-baseweb="tab"] {{
      background: white !important;
      border-radius: 8px 8px 0 0 !important;
      color: {CEMEX_GRAY} !important;
      font-weight: 600 !important;
      font-size: 0.9rem !important;
  }}
  .stTabs [aria-selected="true"] {{
      background: {CEMEX_BLUE} !important;
      color: white !important;
  }}

  /* ── FOOTER ── */
  .footer {{
      text-align: center;
      color: #aaa;
      font-size: 0.78rem;
      padding: 1.5rem 0 0.5rem;
      border-top: 1px solid #e5e8f5;
      margin-top: 2rem;
  }}

  div[data-testid="stVerticalBlock"] {{ gap: 0.5rem; }}
  .stDownloadButton button {{
      background: {CEMEX_GREEN} !important;
      color: white !important;
      border: none !important;
      border-radius: 8px !important;
      font-weight: 700 !important;
  }}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────────────────────
NIVEL_INGLES_MAP = {0: "A1", 1: "A2", 2: "B1", 3: "B2", 4: "C"}
NIVEL_INGLES_REV = {v: k for k, v in NIVEL_INGLES_MAP.items()}


@st.cache_data
def load_data():
    df = pd.read_excel("df_cluster__1_.xlsx")
    return df


def calculate_hybrid_score(row, requirements):
    base_score = 50 if row["Cluster_Id"] == 1 else 25
    points_met = 0
    active_reqs = 0

    if requirements["nivel_ingles"] is not None:
        active_reqs += 1
        if row["NIVEL_DE_INGLES"] >= requirements["nivel_ingles"]:
            points_met += 1

    if requirements["vicepresidencia"] is not None:
        active_reqs += 1
        if str(row["VICEPRESIDENCIA"]).lower() == requirements["vicepresidencia"].lower():
            points_met += 1

    if requirements["banda"] is not None:
        active_reqs += 1
        if row["BANDA"] == requirements["banda"]:
            points_met += 1

    if requirements["ubicacion"] is not None:
        active_reqs += 1
        person_match = str(row["UBICACION"]).lower() == requirements["ubicacion"].lower()
        if person_match:
            points_met += 1
        elif requirements.get("job_allows_relocation") == 1 and row["REUBICACION"] == 1:
            points_met += 1

    if requirements["anioscemex"] is not None and requirements["anioscemex"] > 0:
        active_reqs += 1
        if row["ANIOSCEMEX"] >= requirements["anioscemex"]:
            points_met += 1

    if requirements["cursos_liderazgo_total"] is not None and requirements["cursos_liderazgo_total"] > 0:
        active_reqs += 1
        if row["CURSOS_LIDERAZGO_TOTAL"] >= requirements["cursos_liderazgo_total"]:
            points_met += 1

    if requirements["programa_talento"] is not None:
        active_reqs += 1
        if row["PROGRAMA_TALENTO"] == requirements["programa_talento"]:
            points_met += 1

    req_score = (points_met / active_reqs * 50) if active_reqs > 0 else 0
    return round(base_score + req_score, 1)


def score_color(score):
    if score >= 75:
        return "score-high"
    elif score >= 50:
        return "score-mid"
    return "score-low"


def rank_color(rank):
    if rank == 1: return "gold"
    if rank == 2: return "silver"
    if rank == 3: return "bronze"
    return ""


def to_excel_bytes(df_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_export.to_excel(writer, index=False, sheet_name="Ranking CEMEX")
    return output.getvalue()


# ── LOAD DATA ─────────────────────────────────────────────────────────────────
try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo `df_cluster__1_.xlsx`. Colócalo en la misma carpeta que `app.py`.")
    st.stop()

vp_options    = sorted(df["VICEPRESIDENCIA"].dropna().unique().tolist())
loc_options   = sorted(df["UBICACION"].dropna().unique().tolist())
max_anios     = float(df["ANIOSCEMEX"].max())
max_cursos    = int(df["CURSOS_LIDERAZGO_TOTAL"].max())

# ── HEADER ────────────────────────────────────────────────────────────────────
# CEMEX logo SVG inline (red stripes + blue text)
logo_svg = """
<svg width="120" height="40" viewBox="0 0 120 40" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="8"  width="7" height="24" rx="1" fill="#f22331" transform="rotate(-15 6 20)"/>
  <rect x="11" y="8" width="7" height="24" rx="1" fill="#f22331" transform="rotate(-15 17 20)"/>
  <text x="32" y="28" font-family="Arial Black, sans-serif" font-size="22" font-weight="900" fill="white" letter-spacing="-0.5">CEMEX</text>
</svg>
"""

st.markdown(f"""
<div class="cemex-header">
  <div>{logo_svg}</div>
  <div>
    <div class="header-title">Talent Score Hub</div>
    <div class="header-sub">Plataforma de identificación y ranking de talento interno</div>
    <div class="header-badge">🏗️ Score Híbrido v2.0</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">' + logo_svg + "</div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Requisitos del Puesto")
    st.markdown("---")

    # ── Inglés
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">🌐 Idioma</div>', unsafe_allow_html=True)
    ingles_display = st.selectbox("Nivel de inglés mínimo",
                                  options=["No aplica"] + list(NIVEL_INGLES_MAP.values()),
                                  index=0)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Vicepresidencia
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">🏢 Organización</div>', unsafe_allow_html=True)
    vp_sel = st.selectbox("Vicepresidencia", options=["Cualquiera"] + vp_options, index=0)
    banda_sel = st.selectbox("Banda", options=["No aplica", "Banda 0", "Banda 1"], index=0)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Ubicación
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">📍 Ubicación</div>', unsafe_allow_html=True)
    loc_sel = st.selectbox("Ubicación requerida", options=["Cualquiera"] + loc_options, index=0)
    permite_reub = False
    if loc_sel != "Cualquiera":
        permite_reub = st.checkbox("¿El puesto permite reubicación?", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Experiencia
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">📅 Experiencia</div>', unsafe_allow_html=True)
    anios_min = st.slider("Años mínimos en CEMEX", 0.0, max_anios, 0.0, step=0.5)
    cursos_min = st.slider("Cursos de liderazgo mínimos", 0, max_cursos, 0)
    req_talento = st.selectbox("Programa de talento", options=["No aplica", "Requerido (Sí)", "No requerido (No)"], index=0)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Filtros adicionales
    st.markdown("### 🔍 Filtros de Vista")
    show_cluster = st.multiselect("Cluster Id", options=[0, 1], default=[0, 1])
    top_n = st.slider("Mostrar Top N candidatos", 5, 50, 10)

    st.markdown("---")
    calcular = st.button("🚀 Calcular Ranking", use_container_width=True)

# ── BUILD REQUIREMENTS DICT ────────────────────────────────────────────────────
requirements = {
    "nivel_ingles":          NIVEL_INGLES_REV.get(ingles_display) if ingles_display != "No aplica" else None,
    "vicepresidencia":       vp_sel if vp_sel != "Cualquiera" else None,
    "banda":                 0 if banda_sel == "Banda 0" else (1 if banda_sel == "Banda 1" else None),
    "ubicacion":             loc_sel if loc_sel != "Cualquiera" else None,
    "job_allows_relocation": 1 if permite_reub else 0,
    "anioscemex":            anios_min if anios_min > 0 else None,
    "cursos_liderazgo_total": cursos_min if cursos_min > 0 else None,
    "programa_talento":      (1 if req_talento == "Requerido (Sí)" else 0) if req_talento != "No aplica" else None,
}

# ── MAIN: AUTO-CALCULATE ON LOAD OR BUTTON ────────────────────────────────────
if calcular or True:   # Always show results, refresh on button
    df_result = df.copy()
    df_result["Hybrid_Score"] = df_result.apply(
        lambda r: calculate_hybrid_score(r, requirements), axis=1
    )
    # Apply cluster filter
    df_filtered = df_result[df_result["Cluster_Id"].isin(show_cluster)]
    df_sorted   = df_filtered.sort_values("Hybrid_Score", ascending=False).reset_index(drop=True)

    top_df = df_sorted.head(top_n).copy()
    top_df.index = top_df.index + 1  # rank from 1

    # ── SUMMARY METRICS ────────────────────────────────────────────────────────
    avg_score   = df_sorted["Hybrid_Score"].mean()
    max_score   = df_sorted["Hybrid_Score"].max()
    cluster1_ct = df_sorted[df_sorted["Cluster_Id"] == 1].shape[0]
    reub_ct     = df_sorted[df_sorted["REUBICACION"] == 1].shape[0]

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-label">Candidatos Totales</div>
        <div class="metric-value">{len(df_sorted):,}</div>
        <div class="metric-delta">en el pool filtrado</div>
      </div>
      <div class="metric-card green">
        <div class="metric-label">Score Promedio</div>
        <div class="metric-value">{avg_score:.1f}</div>
        <div class="metric-delta">de 100 puntos</div>
      </div>
      <div class="metric-card red">
        <div class="metric-label">Score Máximo</div>
        <div class="metric-value">{max_score:.1f}</div>
        <div class="metric-delta">candidato líder</div>
      </div>
      <div class="metric-card orange">
        <div class="metric-label">Cluster Élite (1)</div>
        <div class="metric-value">{cluster1_ct:,}</div>
        <div class="metric-delta">de {len(df_sorted):,} candidatos</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ACTIVE FILTERS DISPLAY ─────────────────────────────────────────────────
    active_filters = []
    if requirements["nivel_ingles"] is not None:
        active_filters.append(f"Inglés ≥ {NIVEL_INGLES_MAP[requirements['nivel_ingles']]}")
    if requirements["vicepresidencia"]:
        active_filters.append(f"VP: {requirements['vicepresidencia']}")
    if requirements["banda"] is not None:
        active_filters.append(f"Banda {requirements['banda']}")
    if requirements["ubicacion"]:
        active_filters.append(f"Ubicación: {requirements['ubicacion']}")
    if requirements["anioscemex"]:
        active_filters.append(f"Años CEMEX ≥ {requirements['anioscemex']}")
    if requirements["cursos_liderazgo_total"]:
        active_filters.append(f"Cursos Liderazgo ≥ {requirements['cursos_liderazgo_total']}")
    if requirements["programa_talento"] is not None:
        active_filters.append(f"Talento: {'Sí' if requirements['programa_talento']==1 else 'No'}")

    if active_filters:
        chips = " ".join([f'<span class="filter-active">✓ {f}</span>' for f in active_filters])
        st.markdown(f"**Filtros activos:** {chips}", unsafe_allow_html=True)
    else:
        st.info("ℹ️ Sin requisitos específicos — mostrando score base por Cluster. Usa el panel izquierdo para personalizar.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["🏆 Ranking Top Candidatos", "📊 Visualizaciones", "📋 Tabla Completa"])

    # ─────────────────────────────── TAB 1: RANKING ───────────────────────────
    with tab1:
        col_title, col_export = st.columns([3, 1])
        with col_title:
            st.markdown(f'<div class="section-title">Top {top_n} — Mejores Perfiles</div>', unsafe_allow_html=True)
        with col_export:
            export_cols = ["ID", "Cluster_Id", "NIVEL_DE_INGLES", "VICEPRESIDENCIA",
                           "BANDA", "UBICACION", "REUBICACION", "ANIOSCEMEX",
                           "CURSOS_LIDERAZGO_TOTAL", "PROGRAMA_TALENTO", "Hybrid_Score"]
            export_df = top_df.reset_index()[export_cols]
            st.download_button(
                label="⬇️ Exportar Excel",
                data=to_excel_bytes(export_df),
                file_name="ranking_cemex_talent.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        # Build ranking table HTML
        rows_html = ""
        for rank, row_data in top_df.iterrows():
            rc  = rank_color(rank)
            sc  = score_color(row_data["Hybrid_Score"])
            eng = NIVEL_INGLES_MAP.get(int(row_data["NIVEL_DE_INGLES"]), "—")
            clust_icon = "⭐" if row_data["Cluster_Id"] == 1 else ""
            reub_icon  = "✅" if row_data["REUBICACION"] == 1 else "❌"
            tal_icon   = "✅" if row_data["PROGRAMA_TALENTO"] == 1 else "❌"
            rows_html += f"""
            <tr>
              <td><span class="rank-num {rc}">#{rank}</span></td>
              <td style="font-size:0.75rem;color:#999;max-width:140px;overflow:hidden;text-overflow:ellipsis">{row_data['ID'][:18]}…</td>
              <td>{clust_icon} Cluster {int(row_data['Cluster_Id'])}</td>
              <td>{eng}</td>
              <td style="font-size:0.82rem">{str(row_data['VICEPRESIDENCIA'])[:30]}</td>
              <td>Banda {int(row_data['BANDA'])}</td>
              <td style="font-size:0.78rem">{str(row_data['UBICACION'])[:28]}</td>
              <td>{reub_icon}</td>
              <td>{row_data['ANIOSCEMEX']:.1f} años</td>
              <td>{int(row_data['CURSOS_LIDERAZGO_TOTAL'])}</td>
              <td>{tal_icon}</td>
              <td><span class="score-pill {sc}">{row_data['Hybrid_Score']:.1f}</span></td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto;border-radius:12px;box-shadow:0 2px 16px rgba(0,0,0,0.08);">
        <table class="rank-table">
          <thead><tr>
            <th>#</th><th>ID</th><th>Cluster</th><th>Inglés</th>
            <th>Vicepresidencia</th><th>Banda</th><th>Ubicación</th>
            <th>Reub.</th><th>Años CEMEX</th><th>Cursos Líd.</th><th>Talento</th>
            <th>Score ▼</th>
          </tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────── TAB 2: CHARTS ────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Visualizaciones del Ranking</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Distribution histogram
            fig_hist = px.histogram(
                df_sorted, x="Hybrid_Score", nbins=20,
                title="Distribución de Score Híbrido",
                color_discrete_sequence=[CEMEX_BLUE],
                labels={"Hybrid_Score": "Score", "count": "Candidatos"},
            )
            fig_hist.add_vline(x=avg_score, line_dash="dash", line_color=CEMEX_RED,
                               annotation_text=f"Promedio: {avg_score:.1f}",
                               annotation_position="top right")
            fig_hist.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_family="Barlow, sans-serif",
                title_font_color=CEMEX_BLUE, title_font_size=14,
                margin=dict(t=45, b=30, l=10, r=10),
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col2:
            # Score by Cluster pie
            cluster_avg = df_sorted.groupby("Cluster_Id")["Hybrid_Score"].mean().reset_index()
            cluster_avg["label"] = cluster_avg["Cluster_Id"].map({0: "Cluster 0", 1: "Cluster 1 ⭐"})
            fig_pie = px.pie(cluster_avg, values="Hybrid_Score", names="label",
                             title="Score Promedio por Cluster",
                             color_discrete_sequence=[CEMEX_SKY, CEMEX_BLUE])
            fig_pie.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_family="Barlow, sans-serif",
                title_font_color=CEMEX_BLUE, title_font_size=14,
                margin=dict(t=45, b=10, l=10, r=10),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            # Top candidatos bar (horizontal)
            top15 = df_sorted.head(15).copy()
            top15["short_id"] = top15["ID"].str[:12] + "…"
            fig_bar = px.bar(
                top15, x="Hybrid_Score", y="short_id",
                orientation="h",
                title=f"Top 15 Candidatos — Score",
                color="Hybrid_Score",
                color_continuous_scale=[[0, CEMEX_SKY], [0.5, CEMEX_BLUE], [1, CEMEX_RED]],
                labels={"Hybrid_Score": "Score", "short_id": ""},
            )
            fig_bar.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_family="Barlow, sans-serif",
                yaxis=dict(autorange="reversed"),
                coloraxis_showscale=False,
                title_font_color=CEMEX_BLUE, title_font_size=14,
                margin=dict(t=45, b=30, l=10, r=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col4:
            # Score by VP box
            vp_data = df_sorted.groupby("VICEPRESIDENCIA")["Hybrid_Score"].mean().sort_values(ascending=False).reset_index()
            vp_data["short_vp"] = vp_data["VICEPRESIDENCIA"].str[:22]
            fig_vp = px.bar(
                vp_data, x="short_vp", y="Hybrid_Score",
                title="Score Promedio por Vicepresidencia",
                color="Hybrid_Score",
                color_continuous_scale=[[0, CEMEX_SKY], [1, CEMEX_BLUE]],
                labels={"Hybrid_Score": "Score Promedio", "short_vp": ""},
            )
            fig_vp.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_family="Barlow, sans-serif",
                xaxis_tickangle=-40,
                coloraxis_showscale=False,
                title_font_color=CEMEX_BLUE, title_font_size=14,
                margin=dict(t=45, b=80, l=10, r=10),
            )
            st.plotly_chart(fig_vp, use_container_width=True)

        # Scatter: años CEMEX vs Score
        fig_scatter = px.scatter(
            df_sorted, x="ANIOSCEMEX", y="Hybrid_Score",
            color="Cluster_Id", size_max=8,
            color_discrete_map={0: CEMEX_SKY, 1: CEMEX_RED},
            title="Antigüedad en CEMEX vs Score Híbrido",
            labels={"ANIOSCEMEX": "Años en CEMEX", "Hybrid_Score": "Score Híbrido",
                    "Cluster_Id": "Cluster"},
            opacity=0.65,
        )
        fig_scatter.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="Barlow, sans-serif",
            title_font_color=CEMEX_BLUE, title_font_size=14,
            margin=dict(t=45, b=30, l=10, r=10),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ─────────────────────────────── TAB 3: FULL TABLE ────────────────────────
    with tab3:
        col_title3, col_exp3 = st.columns([3, 1])
        with col_title3:
            st.markdown('<div class="section-title">📋 Tabla Completa Filtrada</div>', unsafe_allow_html=True)
        with col_exp3:
            export_all = df_sorted[["ID","Cluster_Id","NIVEL_DE_INGLES","VICEPRESIDENCIA",
                                    "BANDA","UBICACION","REUBICACION","ANIOSCEMEX",
                                    "CURSOS_LIDERAZGO_TOTAL","PROGRAMA_TALENTO","Hybrid_Score"]].copy()
            export_all["NIVEL_DE_INGLES"] = export_all["NIVEL_DE_INGLES"].map(NIVEL_INGLES_MAP)
            st.download_button(
                label="⬇️ Exportar Todo",
                data=to_excel_bytes(export_all),
                file_name="candidatos_cemex_completo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        # Search box
        search = st.text_input("🔎 Buscar por ID, VP o Ubicación…", "")
        display_df = df_sorted[["ID","Cluster_Id","NIVEL_DE_INGLES","VICEPRESIDENCIA",
                                 "BANDA","UBICACION","REUBICACION","ANIOSCEMEX",
                                 "CURSOS_LIDERAZGO_TOTAL","PROGRAMA_TALENTO","Hybrid_Score"]].copy()
        display_df["NIVEL_DE_INGLES"] = display_df["NIVEL_DE_INGLES"].map(NIVEL_INGLES_MAP)
        display_df.columns = ["ID","Cluster","Inglés","Vicepresidencia","Banda",
                               "Ubicación","Reubicación","Años CEMEX","Cursos Líd.","Talento","Score"]

        if search:
            mask = display_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)
            display_df = display_df[mask]

        st.dataframe(
            display_df.reset_index(drop=True),
            use_container_width=True,
            height=480,
            column_config={
                "Score": st.column_config.ProgressColumn(
                    "Score", min_value=0, max_value=100, format="%.1f"
                ),
            }
        )
        st.caption(f"Mostrando {len(display_df):,} candidatos")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  🏗️ CEMEX Talent Score Hub &nbsp;|&nbsp; Modelo de Score Híbrido v2.0 &nbsp;|&nbsp;
  Desarrollado para Recursos Humanos CEMEX &nbsp;|&nbsp; Confidencial
</div>
""", unsafe_allow_html=True)
