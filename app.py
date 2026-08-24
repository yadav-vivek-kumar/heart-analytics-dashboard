"""
Google HEART & UX Analytics Suite - Main Streamlit Application
"""
import os
import sys
import streamlit as st
import pandas as pd

# Ensure current directory is in Python path for Streamlit Cloud container
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from data_loader import load_all_data, compute_heart_kpis, DEFAULT_EXCEL_PATH
    from components.kpi_cards import render_heart_kpi_cards
    from components.heatmap_studio import render_heatmap_studio
    from components.heart_dashboard import render_heart_dashboard
    from components.risk_analyzer import render_risk_analyzer
    from components.user_explorer import render_user_explorer
    from components.sheet_viewer import render_sheet_viewer
except ModuleNotFoundError:
    from data_loader import load_all_data, compute_heart_kpis, DEFAULT_EXCEL_PATH
    from kpi_cards import render_heart_kpi_cards
    from heatmap_studio import render_heatmap_studio
    from heart_dashboard import render_heart_dashboard
    from risk_analyzer import render_risk_analyzer
    from user_explorer import render_user_explorer
    from sheet_viewer import render_sheet_viewer

# -------------------------------------------------------------
# 1. Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="Google HEART & UX Analytics Studio",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. Inject Custom CSS
# -------------------------------------------------------------
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. Sidebar: Ingestion & Global Filters
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-tag">UX Intelligence Suite</div>
        <div class="sidebar-title">❤️ Google HEART Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📂 Data Source")
    use_custom_file = st.toggle("Upload Custom Excel File", value=False)
    
    file_source = None
    if use_custom_file:
        uploaded_file = st.file_uploader("Upload .xlsx file", type=["xlsx", "xls"])
        if uploaded_file is not None:
            file_source = uploaded_file
        else:
            st.info("Using default dataset until a file is uploaded.")
            file_source = DEFAULT_EXCEL_PATH
    else:
        file_source = DEFAULT_EXCEL_PATH
        st.caption(f"📁 Path: `{DEFAULT_EXCEL_PATH}`")
        
    st.markdown("---")
    st.markdown("### 🎯 Global Filters")
    
    # Load raw data
    try:
        sheets_data = load_all_data(file_source)
        df_ux_raw = sheets_data.get("ux_matrix", pd.DataFrame()).copy()
    except Exception as e:
        st.error(f"Error loading Excel data: {e}")
        st.stop()
        
    # Filter 1: NPS Category
    nps_opts = df_ux_raw["nps_category"].dropna().unique().tolist() if "nps_category" in df_ux_raw.columns else []
    selected_nps = st.multiselect("NPS Category:", options=nps_opts, default=nps_opts)
    
    # Filter 2: UX Risk Level
    risk_opts = df_ux_raw["Ux_Risk_level"].dropna().unique().tolist() if "Ux_Risk_level" in df_ux_raw.columns else []
    selected_risk = st.multiselect("UX Risk Level:", options=risk_opts, default=risk_opts)
    
    # Filter 3: Engagement Tier
    eng_opts = df_ux_raw["Eng_flag"].dropna().unique().tolist() if "Eng_flag" in df_ux_raw.columns else []
    selected_eng = st.multiselect("Engagement Tier:", options=eng_opts, default=eng_opts)
    
    # Filter 4: Adoption Status
    adopt_opts = df_ux_raw["Adoptation_Flag"].dropna().unique().tolist() if "Adoptation_Flag" in df_ux_raw.columns else []
    selected_adopt = st.multiselect("Adoption Status:", options=adopt_opts, default=adopt_opts)
    
    # Filter 5: Retention Status
    ret_opts = df_ux_raw["Retention_Flag"].dropna().unique().tolist() if "Retention_Flag" in df_ux_raw.columns else []
    selected_ret = st.multiselect("Day-7 Retention:", options=ret_opts, default=ret_opts)
    
    # Apply filters
    filtered_df = df_ux_raw.copy()
    if selected_nps:
        filtered_df = filtered_df[filtered_df["nps_category"].isin(selected_nps)]
    if selected_risk:
        filtered_df = filtered_df[filtered_df["Ux_Risk_level"].isin(selected_risk)]
    if selected_eng:
        filtered_df = filtered_df[filtered_df["Eng_flag"].isin(selected_eng)]
    if selected_adopt:
        filtered_df = filtered_df[filtered_df["Adoptation_Flag"].isin(selected_adopt)]
    if selected_ret:
        filtered_df = filtered_df[filtered_df["Retention_Flag"].isin(selected_ret)]
        
    st.markdown("---")
    st.markdown(f"**Cohort Filtered:** `{len(filtered_df)}` / `{len(df_ux_raw)}` users")
    
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# -------------------------------------------------------------
# 4. Main Header Banner
# -------------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <div class="hero-title">
        <span>❤️ Google HEART & UX Analytics Studio</span>
        <span class="badge badge-promoter" style="font-size:12px; margin-left:auto;">Live Dataset Ready</span>
    </div>
    <div class="hero-subtitle">
        Executive UX Intelligence, Multi-Metric Heatmaps, Behavioral Funnels & Usability Diagnostic Workbench for E-Learning
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. Executive KPI Cards
# -------------------------------------------------------------
if len(filtered_df) == 0:
    st.warning("No user records match the selected filters. Please adjust your sidebar criteria.")
    st.stop()

kpis = compute_heart_kpis(filtered_df)
render_heart_kpi_cards(kpis)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. Main App Navigation Tabs
# -------------------------------------------------------------
tab_overview, tab_heatmaps, tab_risk, tab_simulator, tab_explorer, tab_sheets = st.tabs([
    "📊 HEART Dashboard",
    "🔥 Heatmap Studio",
    "⚠️ UX Risk & Early Warning",
    "🔮 What-If Simulator",
    "👥 User Segment Explorer",
    "📑 Workbook Sheets"
])

with tab_overview:
    render_heart_dashboard(filtered_df, kpis)
    
with tab_heatmaps:
    render_heatmap_studio(filtered_df)
    
with tab_risk:
    render_risk_analyzer(filtered_df, kpis)

with tab_simulator:
    st.markdown("""
    <div class="section-box">
        <h3 style="margin-top:0; color:#f8fafc; font-weight:800; font-size: 20px;">
            🔮 Interactive UX Optimization & What-If Simulator
        </h3>
        <p style="color:#94a3b8; font-size:13px; margin-bottom:0;">
            Simulate the business impact of onboarding velocity improvements and usability error reductions on NPS and Retention.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        st.markdown("#### ⚙️ Simulation Levers")
        ttfv_reduction = st.slider("Target TTFV Reduction (% Faster Onboarding):", min_value=0, max_value=60, value=30, step=5)
        error_reduction = st.slider("Target Usability Error Reduction (% Fewer Mistakes):", min_value=0, max_value=70, value=40, step=5)
        adoption_boost = st.slider("Target Core Action Adoption Boost (% Increase):", min_value=0, max_value=40, value=15, step=5)
        
    with sim_col2:
        st.markdown("#### 📈 Projected Metric Impact")
        
        # Calculate simulation estimates based on correlation weights
        current_nps = kpis.get("nps_score", 0)
        projected_nps = min(100.0, current_nps + (ttfv_reduction * 0.45) + (error_reduction * 0.35))
        
        current_ret = kpis.get("retention_rate", 0)
        projected_ret = min(100.0, current_ret + (ttfv_reduction * 0.25) + (adoption_boost * 0.30))
        
        current_sus = kpis.get("avg_sus", 0)
        projected_sus = min(100.0, current_sus + (error_reduction * 0.30) + (ttfv_reduction * 0.15))
        
        p1, p2, p3 = st.columns(3)
        p1.metric("Projected NPS", f"{projected_nps:+.1f}", delta=f"{projected_nps - current_nps:+.1f}")
        p2.metric("Projected Retention", f"{projected_ret:.1f}%", delta=f"{projected_ret - current_ret:+.1f}%")
        p3.metric("Projected SUS Score", f"{projected_sus:.1f}/100", delta=f"{projected_sus - current_sus:+.1f}")
        
        st.info(f"💡 By cutting TTFV by {ttfv_reduction}% and reducing task errors by {error_reduction}%, the application's NPS is projected to jump from **{current_nps:+.1f}** to **{projected_nps:+.1f}**, transforming passive users into active promoters.")

with tab_explorer:
    render_user_explorer(filtered_df)
    
with tab_sheets:
    render_sheet_viewer(sheets_data)
