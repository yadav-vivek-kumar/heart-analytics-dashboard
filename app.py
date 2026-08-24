"""
Google HEART & UX Analytics Studio - Complete Self-Contained Master Application
Designed for instant 1-click deployment on Streamlit Community Cloud and GitHub.
"""
import os
import sys
import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
# 2. Embedded Glassmorphic Design System (CSS)
# -------------------------------------------------------------
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1400px;
}

.hero-header {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.hero-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #f472b6, #fb923c);
}

.hero-title {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #f8fafc;
    margin: 0 0 6px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.hero-subtitle {
    font-size: 13.5px;
    color: #94a3b8;
    margin: 0;
    font-weight: 400;
}

.kpi-card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px 18px;
    position: relative;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 15px -2px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px -4px rgba(0, 0, 0, 0.35);
    border-color: rgba(255, 255, 255, 0.2);
}

.kpi-card.accent-happiness { border-top: 3px solid #10b981; }
.kpi-card.accent-engagement { border-top: 3px solid #3b82f6; }
.kpi-card.accent-adoption { border-top: 3px solid #8b5cf6; }
.kpi-card.accent-retention { border-top: 3px solid #f59e0b; }
.kpi-card.accent-tasksuccess { border-top: 3px solid #06b6d4; }
.kpi-card.accent-risk { border-top: 3px solid #ef4444; }

.kpi-category {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94a3b8;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 6px;
}

.kpi-subtext {
    font-size: 11.5px;
    color: #94a3b8;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}
.badge-promoter { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

.section-box {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

.sidebar-brand {
    padding: 10px 0 16px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 18px;
}

.sidebar-title {
    font-size: 17px;
    font-weight: 800;
    color: #f1f5f9;
}

.sidebar-tag {
    font-size: 10.5px;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(30, 41, 59, 0.4);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
    color: #94a3b8;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: #38bdf8 !important;
    color: #0b1120 !important;
    font-weight: 700 !important;
}
"""
st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. Data Ingestion & Metric Engine
# -------------------------------------------------------------
SUS_QUESTIONS = {
    "SUS_Q1": "1. I think that I would like to use this system frequently.",
    "SUS_Q2": "2. I found the system unnecessarily complex.",
    "SUS_Q3": "3. I thought the system was easy to use.",
    "SUS_Q4": "4. I think that I would need the support of a technical person.",
    "SUS_Q5": "5. I found the various functions in this system were well integrated.",
    "SUS_Q6": "6. I thought there was too much inconsistency in this system.",
    "SUS_Q7": "7. I would imagine that most people would learn to use this system very quickly.",
    "SUS_Q8": "8. I found the system very cumbersome/awkward to use.",
    "SUS_Q9": "9. I felt very confident using the system.",
    "SUS_Q10": "10. I needed to learn a lot of things before I could get going with this system."
}

SUS_SHORT_NAMES = {
    "SUS_Q1": "Q1: Frequent Use",
    "SUS_Q2": "Q2: Unnecessarily Complex",
    "SUS_Q3": "Q3: Easy to Use",
    "SUS_Q4": "Q4: Tech Support Needed",
    "SUS_Q5": "Q5: Well Integrated",
    "SUS_Q6": "Q6: Inconsistent",
    "SUS_Q7": "Q7: Quick to Learn",
    "SUS_Q8": "Q8: Cumbersome/Awkward",
    "SUS_Q9": "Q9: Confident",
    "SUS_Q10": "Q10: Steep Learning"
}

def locate_excel_file():
    """Finds the HEART_ANALYSIS.xlsx file across cloud and local paths."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    search_paths = [
        os.path.join(base_dir, "HEART_ANALYSIS.xlsx"),
        os.path.join(base_dir, "data", "HEART_ANALYSIS.xlsx"),
        r"C:\DOCUMENTS\HEART_ANALYSIS.xlsx",
        "HEART_ANALYSIS.xlsx"
    ]
    for p in search_paths:
        if os.path.exists(p):
            return p
    return search_paths[0]

@st.cache_data(show_spinner=False)
def load_workbook_data(file_source=None):
    """Loads all workbook sheets with error handling and data cleaning."""
    path = file_source if file_source is not None else locate_excel_file()
    
    if not os.path.exists(path) and not hasattr(path, "read"):
        raise FileNotFoundError(f"Workbook not found at: {path}")
        
    xl = pd.ExcelFile(path)
    sheets = {sheet: xl.parse(sheet) for sheet in xl.sheet_names}
    
    if "ux_matrix" in sheets:
        df_ux = sheets["ux_matrix"].copy()
        if "nps_category" in df_ux.columns:
            df_ux["nps_category"] = df_ux["nps_category"].replace({
                "DECTATOR": "DETRACTOR",
                "PASS": "PASSIVE",
                "PROMOTER": "PROMOTER"
            })
        if "Adoptation_Flag" in df_ux.columns:
            df_ux["Adoptation_Flag"] = df_ux["Adoptation_Flag"].replace({
                "NOt Adopted": "Not Adopted",
                "NOt adopted": "Not Adopted"
            })
        if "Task_Complition_Flag" in df_ux.columns:
            df_ux["Task_Complition_Flag"] = df_ux["Task_Complition_Flag"].replace({
                "Fail": "Failed"
            })
        sheets["ux_matrix"] = df_ux
        
    return sheets

def compute_heart_metrics(df):
    """Computes all Google HEART framework and risk KPIs."""
    n_users = len(df)
    if n_users == 0:
        return {}
        
    # Happiness
    promoters = (df["NPS_Response"] >= 9).sum() if "NPS_Response" in df.columns else 0
    passives = ((df["NPS_Response"] >= 7) & (df["NPS_Response"] <= 8)).sum() if "NPS_Response" in df.columns else 0
    detractors = (df["NPS_Response"] <= 6).sum() if "NPS_Response" in df.columns else 0
    
    pct_prom = (promoters / n_users) * 100
    pct_pass = (passives / n_users) * 100
    pct_det = (detractors / n_users) * 100
    nps_score = pct_prom - pct_det
    
    avg_csat = df["CSAT_Response"].mean() if "CSAT_Response" in df.columns else 0.0
    avg_sus = df["sus_score"].mean() if "sus_score" in df.columns else 0.0
    
    # Engagement
    avg_sessions = df["Sessions"].mean() if "Sessions" in df.columns else 0.0
    pct_high_eng = ((df["Eng_flag"] == "HIGH").sum() / n_users * 100) if "Eng_flag" in df.columns else 0.0
    
    # Adoption
    core_actions = (df["Core_Action"] == 1).sum() if "Core_Action" in df.columns else 0
    adoption_rate = (core_actions / n_users) * 100
    avg_ttfv = df["TTFV_min"].mean() if "TTFV_min" in df.columns else 0.0
    
    # Retention
    retention_rate = ((df["Day7_Return"] == 1).sum() / n_users * 100) if "Day7_Return" in df.columns else 0.0
    
    # Task Success
    task_success_rate = ((df["Task_Completed"] == 1).sum() / n_users * 100) if "Task_Completed" in df.columns else 0.0
    total_attempts = df["Task_Attempts"].sum() if "Task_Attempts" in df.columns else 0
    total_errors = df["Errors"].sum() if "Errors" in df.columns else 0
    overall_error_rate = (total_errors / total_attempts * 100) if total_attempts > 0 else 0.0
    
    # Risk
    avg_risk_points = df["Ux_Risk_Points"].mean() if "Ux_Risk_Points" in df.columns else 0.0
    high_risk_users = (df["Ux_Risk_level"] == "High").sum() if "Ux_Risk_level" in df.columns else 0
    pct_high_risk = (high_risk_users / n_users) * 100

    return {
        "n_users": n_users,
        "nps_score": nps_score,
        "pct_promoters": pct_prom,
        "pct_passives": pct_pass,
        "pct_detractors": pct_det,
        "promoters": promoters,
        "passives": passives,
        "detractors": detractors,
        "avg_csat": avg_csat,
        "avg_sus": avg_sus,
        "avg_sessions": avg_sessions,
        "pct_high_eng": pct_high_eng,
        "adoption_rate": adoption_rate,
        "avg_ttfv": avg_ttfv,
        "retention_rate": retention_rate,
        "task_success_rate": task_success_rate,
        "overall_error_rate": overall_error_rate,
        "total_attempts": total_attempts,
        "total_errors": total_errors,
        "avg_risk_points": avg_risk_points,
        "high_risk_users": high_risk_users,
        "pct_high_risk": pct_high_risk
    }

def calculate_correlations(df, method="pearson", selected_cols=None):
    """Calculates correlation matrix for UX and HEART variables."""
    default_mapping = {
        "NPS_Response": "NPS",
        "CSAT_Response": "CSAT",
        "sus_score": "SUS",
        "CES_Response": "CES",
        "TTFV_min": "TTFV",
        "Errors": "Errors",
        "Sessions": "Sessions",
        "Core_Action": "Adoption",
        "Day7_Return": "Retention",
        "Task_Completed": "Task Success",
        "User_Error_Rate": "Error Rate %",
        "Ux_Risk_Points": "Risk Points"
    }
    cols = [c for c in default_mapping.keys() if c in df.columns]
    if selected_cols:
        cols = [c for c in selected_cols if c in df.columns]
    sub_df = df[cols].rename(columns={k: default_mapping.get(k, k) for k in cols})
    return sub_df.corr(method=method)

# -------------------------------------------------------------
# 4. Sidebar Controls & Global Filters
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
        uploaded = st.file_uploader("Upload .xlsx file", type=["xlsx", "xls"])
        if uploaded is not None:
            file_source = uploaded
        else:
            st.info("Using bundled HEART_ANALYSIS.xlsx until a file is uploaded.")
            file_source = locate_excel_file()
    else:
        file_source = locate_excel_file()
        st.caption(f"📁 Dataset: `HEART_ANALYSIS.xlsx`")
        
    st.markdown("---")
    st.markdown("### 🎯 Global Filters")
    
    try:
        sheets_data = load_workbook_data(file_source)
        df_ux_raw = sheets_data.get("ux_matrix", pd.DataFrame()).copy()
    except Exception as e:
        st.error(f"Error loading workbook: {e}")
        st.stop()
        
    nps_opts = df_ux_raw["nps_category"].dropna().unique().tolist() if "nps_category" in df_ux_raw.columns else []
    selected_nps = st.multiselect("NPS Category:", options=nps_opts, default=nps_opts)
    
    risk_opts = df_ux_raw["Ux_Risk_level"].dropna().unique().tolist() if "Ux_Risk_level" in df_ux_raw.columns else []
    selected_risk = st.multiselect("UX Risk Level:", options=risk_opts, default=risk_opts)
    
    eng_opts = df_ux_raw["Eng_flag"].dropna().unique().tolist() if "Eng_flag" in df_ux_raw.columns else []
    selected_eng = st.multiselect("Engagement Tier:", options=eng_opts, default=eng_opts)
    
    adopt_opts = df_ux_raw["Adoptation_Flag"].dropna().unique().tolist() if "Adoptation_Flag" in df_ux_raw.columns else []
    selected_adopt = st.multiselect("Adoption Status:", options=adopt_opts, default=adopt_opts)
    
    ret_opts = df_ux_raw["Retention_Flag"].dropna().unique().tolist() if "Retention_Flag" in df_ux_raw.columns else []
    selected_ret = st.multiselect("Day-7 Retention:", options=ret_opts, default=ret_opts)
    
    # Filter Execution
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
# 5. Header Banner & KPI Cards Ribbon
# -------------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <div class="hero-title">
        <span>❤️ Google HEART & UX Analytics Studio</span>
        <span class="badge badge-promoter" style="margin-left:auto;">Live Online</span>
    </div>
    <div class="hero-subtitle">
        Executive UX Intelligence, Multi-Metric Heatmaps, Behavioral Funnels & Usability Diagnostic Workbench for E-Learning
    </div>
</div>
""", unsafe_allow_html=True)

if len(filtered_df) == 0:
    st.warning("No user records match the selected filters. Please adjust sidebar criteria.")
    st.stop()

kpis = compute_heart_metrics(filtered_df)

# Render Scorecard Ribbon
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    nps_val = kpis.get("nps_score", 0)
    nps_color = "#10b981" if nps_val > 0 else "#ef4444"
    st.markdown(f"""
    <div class="kpi-card accent-happiness">
        <div class="kpi-category"><span>Happiness (H)</span><span>😊</span></div>
        <div class="kpi-value" style="color: {nps_color};">{nps_val:+.1f}</div>
        <div class="kpi-subtext"><strong>NPS Score</strong> ({kpis.get('pct_promoters', 0):.0f}% Prom | {kpis.get('pct_detractors', 0):.0f}% Det)</div>
    </div>
    """, unsafe_allow_html=True)
    
with c2:
    st.markdown(f"""
    <div class="kpi-card accent-engagement">
        <div class="kpi-category"><span>Engagement (E)</span><span>⚡</span></div>
        <div class="kpi-value">{kpis.get('avg_sessions', 0):.1f}</div>
        <div class="kpi-subtext"><strong>Avg Sessions</strong> ({kpis.get('pct_high_eng', 0):.0f}% High tier)</div>
    </div>
    """, unsafe_allow_html=True)
    
with c3:
    st.markdown(f"""
    <div class="kpi-card accent-adoption">
        <div class="kpi-category"><span>Adoption (A)</span><span>🚀</span></div>
        <div class="kpi-value">{kpis.get('adoption_rate', 0):.1f}%</div>
        <div class="kpi-subtext"><strong>Core Action</strong> (Avg TTFV: {kpis.get('avg_ttfv', 0):.1f}m)</div>
    </div>
    """, unsafe_allow_html=True)
    
with c4:
    st.markdown(f"""
    <div class="kpi-card accent-retention">
        <div class="kpi-category"><span>Retention (R)</span><span>🔄</span></div>
        <div class="kpi-value">{kpis.get('retention_rate', 0):.1f}%</div>
        <div class="kpi-subtext"><strong>Day-7 Return Rate</strong></div>
    </div>
    """, unsafe_allow_html=True)
    
with c5:
    st.markdown(f"""
    <div class="kpi-card accent-tasksuccess">
        <div class="kpi-category"><span>Task Success (T)</span><span>🎯</span></div>
        <div class="kpi-value">{kpis.get('task_success_rate', 0):.1f}%</div>
        <div class="kpi-subtext"><strong>Completion</strong> ({kpis.get('overall_error_rate', 0):.1f}% Error rate)</div>
    </div>
    """, unsafe_allow_html=True)
    
with c6:
    risk_pct = kpis.get("pct_high_risk", 0)
    risk_color = "#ef4444" if risk_pct > 20 else "#f59e0b"
    st.markdown(f"""
    <div class="kpi-card accent-risk">
        <div class="kpi-category"><span>UX Risk Level</span><span>⚠️</span></div>
        <div class="kpi-value" style="color: {risk_color};">{kpis.get('high_risk_users', 0)} <span style="font-size:13px; color:#94a3b8;">({risk_pct:.0f}%)</span></div>
        <div class="kpi-subtext"><strong>High-Risk Users</strong> (Avg Risk: {kpis.get('avg_risk_points', 0):.1f}/9)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 22px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. Main Application Tabs
# -------------------------------------------------------------
tab_heart, tab_heatmap, tab_risk, tab_sim, tab_users, tab_sheets = st.tabs([
    "📊 HEART Dashboard",
    "🔥 Heatmap Studio",
    "⚠️ UX Risk & Early Warning",
    "🔮 What-If Simulator",
    "👥 User Segment Explorer",
    "📑 Workbook Sheets"
])

# -------------------------------------------------------------
# TAB 1: GOOGLE HEART DASHBOARD
# -------------------------------------------------------------
with tab_heart:
    st.markdown("""
    <div class="section-box">
        <h3 style="margin-top:0; color:#f8fafc; font-weight:800; font-size: 19px;">
            ❤️ Google HEART Framework Visualizer
        </h3>
        <p style="color:#94a3b8; font-size:13px; margin-bottom:0;">
            Explore behavioral, perceptual, and efficiency indicators across all 5 framework pillars.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    pillar_tabs = st.tabs(["😊 Happiness (H)", "⚡ Engagement (E)", "🚀 Adoption (A)", "🔄 Retention (R)", "🎯 Task Success (T)"])
    
    # 1. Happiness
    with pillar_tabs[0]:
        h1, h2, h3 = st.columns([1.2, 1.2, 1.6])
        with h1:
            fig_nps_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=kpis.get("nps_score", 0),
                title={"text": "<b>Net Promoter Score (NPS)</b>", "font": {"size": 14, "color": "#f8fafc"}},
                gauge={
                    "axis": {"range": [-100, 100], "tickcolor": "#94a3b8"},
                    "bar": {"color": "#38bdf8", "thickness": 0.25},
                    "steps": [
                        {"range": [-100, 0], "color": "rgba(239, 68, 68, 0.3)"},
                        {"range": [0, 50], "color": "rgba(245, 158, 11, 0.3)"},
                        {"range": [50, 100], "color": "rgba(16, 185, 129, 0.3)"}
                    ]
                }
            ))
            fig_nps_gauge.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=220, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_nps_gauge, use_container_width=True)
            
            nps_dist = pd.DataFrame({
                "Category": ["Promoters (9-10)", "Passives (7-8)", "Detractors (0-6)"],
                "Count": [kpis.get("promoters", 0), kpis.get("passives", 0), kpis.get("detractors", 0)]
            })
            fig_nps_donut = px.pie(nps_dist, names="Category", values="Count", color="Category",
                                  color_discrete_map={"Promoters (9-10)": "#10b981", "Passives (7-8)": "#f59e0b", "Detractors (0-6)": "#ef4444"}, hole=0.55)
            fig_nps_donut.update_layout(title=dict(text="<b>NPS Distribution</b>", font=dict(size=13, color="#f8fafc")),
                                       template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=240, margin=dict(l=10, r=10, t=35, b=10),
                                       legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font=dict(size=10)))
            st.plotly_chart(fig_nps_donut, use_container_width=True)
            
        with h2:
            st.markdown(f"**CSAT Satisfaction (Avg: {kpis.get('avg_csat', 0):.2f}/5.0)**")
            if "CSAT_Response" in filtered_df.columns:
                csat_df = filtered_df["CSAT_Response"].value_counts().sort_index().reset_index()
                csat_df.columns = ["Rating", "Users"]
                csat_df["Label"] = csat_df["Rating"].apply(lambda x: f"{x} Star{'s' if x>1 else ''}")
                fig_csat = px.bar(csat_df, x="Label", y="Users", color="Rating", color_continuous_scale="Teal", text="Users")
                fig_csat.update_traces(textposition="outside")
                fig_csat.update_layout(title=dict(text="<b>CSAT Score Breakdown</b>", font=dict(size=13, color="#f8fafc")),
                                       template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       height=460, margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False)
                st.plotly_chart(fig_csat, use_container_width=True)
                
        with h3:
            st.markdown(f"**SUS Usability Score (Avg: {kpis.get('avg_sus', 0):.1f}/100)**")
            if "sus_score" in filtered_df.columns:
                fig_sus = px.histogram(filtered_df, x="sus_score", nbins=15, color="sus_category" if "sus_category" in filtered_df.columns else None, marginal="box")
                fig_sus.add_vline(x=68.0, line_dash="dash", line_color="#fbbf24", annotation_text="Benchmark (68.0)", annotation_font=dict(color="#fbbf24", size=11))
                fig_sus.update_layout(title=dict(text="<b>SUS Distribution vs Benchmark (68.0)</b>", font=dict(size=13, color="#f8fafc")),
                                      template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                      height=460, margin=dict(l=20, r=20, t=40, b=20), xaxis=dict(title="SUS Score (0-100)"), yaxis=dict(title="Users"))
                st.plotly_chart(fig_sus, use_container_width=True)

    # 2. Engagement
    with pillar_tabs[1]:
        e1, e2 = st.columns(2)
        with e1:
            if "Sessions" in filtered_df.columns:
                fig_sess = px.histogram(filtered_df, x="Sessions", nbins=12, color="Eng_flag" if "Eng_flag" in filtered_df.columns else None,
                                        color_discrete_map={"HIGH": "#10b981", "MEDIUM": "#3b82f6", "LOW": "#f59e0b"}, text_auto=True)
                fig_sess.update_layout(title=dict(text="<b>Sessions Distribution by Engagement Tier</b>", font=dict(size=14, color="#f8fafc")),
                                       template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_sess, use_container_width=True)
        with e2:
            if "Sessions" in filtered_df.columns and "CSAT_Response" in filtered_df.columns:
                fig_sess_csat = px.box(filtered_df, x="CSAT_Response", y="Sessions", color="CSAT_Response", points="all")
                fig_sess_csat.update_layout(title=dict(text="<b>Sessions vs User Satisfaction (CSAT)</b>", font=dict(size=14, color="#f8fafc")),
                                            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380, showlegend=False)
                st.plotly_chart(fig_sess_csat, use_container_width=True)

    # 3. Adoption
    with pillar_tabs[2]:
        a1, a2 = st.columns(2)
        with a1:
            if "Adoptation_Flag" in filtered_df.columns:
                adopt_df = filtered_df["Adoptation_Flag"].value_counts().reset_index()
                adopt_df.columns = ["Status", "Count"]
                fig_ad = px.pie(adopt_df, names="Status", values="Count", color="Status", color_discrete_map={"Adopted": "#8b5cf6", "Not Adopted": "#64748b"}, hole=0.6)
                fig_ad.update_layout(title=dict(text=f"<b>Core Action Adoption ({kpis.get('adoption_rate', 0):.1f}%)</b>", font=dict(size=14, color="#f8fafc")),
                                     template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=380)
                st.plotly_chart(fig_ad, use_container_width=True)
        with a2:
            if "TTFV_min" in filtered_df.columns:
                fig_ttfv = px.histogram(filtered_df, x="TTFV_min", nbins=12, color="CATEGORY" if "CATEGORY" in filtered_df.columns else None, text_auto=True)
                fig_ttfv.add_vline(x=5.0, line_dash="dash", line_color="#10b981", annotation_text="Target (≤5m)", annotation_font=dict(color="#10b981"))
                fig_ttfv.update_layout(title=dict(text=f"<b>Time to First Value (Avg: {kpis.get('avg_ttfv', 0):.1f} min)</b>", font=dict(size=14, color="#f8fafc")),
                                       template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380)
                st.plotly_chart(fig_ttfv, use_container_width=True)

    # 4. Retention
    with pillar_tabs[3]:
        r1, r2 = st.columns(2)
        with r1:
            if "Retention_Flag" in filtered_df.columns:
                ret_df = filtered_df["Retention_Flag"].value_counts().reset_index()
                ret_df.columns = ["Status", "Count"]
                fig_ret = px.bar(ret_df, x="Status", y="Count", color="Status", color_discrete_map={"Returned": "#10b981", "Not Returned": "#ef4444"}, text="Count")
                fig_ret.update_traces(textposition="outside")
                fig_ret.update_layout(title=dict(text=f"<b>Day-7 Return Rate ({kpis.get('retention_rate', 0):.1f}%)</b>", font=dict(size=14, color="#f8fafc")),
                                      template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380, showlegend=False)
                st.plotly_chart(fig_ret, use_container_width=True)
        with r2:
            if "Retention_Flag" in filtered_df.columns and "nps_category" in filtered_df.columns:
                ret_nps = pd.crosstab(filtered_df["nps_category"], filtered_df["Retention_Flag"], normalize="index") * 100
                ret_nps = ret_nps.reset_index()
                fig_rn = px.bar(ret_nps, x="nps_category", y=["Returned", "Not Returned"] if "Returned" in ret_nps.columns else ret_nps.columns[1:],
                                barmode="stack", color_discrete_map={"Returned": "#10b981", "Not Returned": "#ef4444"})
                fig_rn.update_layout(title=dict(text="<b>Day-7 Retention by NPS Segment (%)</b>", font=dict(size=14, color="#f8fafc")),
                                     template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380, yaxis=dict(range=[0, 100]))
                st.plotly_chart(fig_rn, use_container_width=True)

    # 5. Task Success
    with pillar_tabs[4]:
        t1, t2 = st.columns(2)
        with t1:
            if "Task_Complition_Flag" in filtered_df.columns:
                ts_df = filtered_df["Task_Complition_Flag"].value_counts().reset_index()
                ts_df.columns = ["Status", "Count"]
                fig_ts = px.pie(ts_df, names="Status", values="Count", color="Status", color_discrete_map={"Success": "#06b6d4", "Failed": "#ef4444"}, hole=0.55)
                fig_ts.update_layout(title=dict(text=f"<b>Task Completion Rate ({kpis.get('task_success_rate', 0):.1f}%)</b>", font=dict(size=14, color="#f8fafc")),
                                     template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=380)
                st.plotly_chart(fig_ts, use_container_width=True)
        with t2:
            if "Task_Attempts" in filtered_df.columns and "Errors" in filtered_df.columns:
                try:
                    import statsmodels
                    has_sm = True
                except ImportError:
                    has_sm = False
                fig_err = px.scatter(filtered_df, x="Task_Attempts", y="Errors",
                                     color="Task_Complition_Flag" if "Task_Complition_Flag" in filtered_df.columns else None,
                                     size="User_Error_Rate" if "User_Error_Rate" in filtered_df.columns else None,
                                     hover_data=["User_ID", "sus_score", "NPS_Response"] if "User_ID" in filtered_df.columns else None,
                                     trendline="ols" if has_sm else None,
                                     color_discrete_map={"Success": "#06b6d4", "Failed": "#ef4444"})
                fig_err.update_layout(title=dict(text="<b>Task Attempts vs Errors</b>", font=dict(size=14, color="#f8fafc")),
                                      template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380)
                st.plotly_chart(fig_err, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: INTERACTIVE HEATMAP STUDIO
# -------------------------------------------------------------
with tab_heatmap:
    st.markdown("""
    <div class="section-box">
        <h3 style="margin-top:0; color:#f8fafc; font-weight:800; font-size: 19px;">
            🔥 Interactive Heatmap Studio
        </h3>
        <p style="color:#94a3b8; font-size:13px; margin-bottom:0;">
            Explore linear correlations, usability question item diagnostics, cohort densities, and individual user matrices.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    hm_tabs = st.tabs(["📊 UX Correlation Matrix", "🎯 SUS 10-Question Diagnostic", "🔀 Cross-Tabulation Heatmap", "👥 User Cohort Performance Heatmap"])
    
    # Heatmap Tab 1: Correlation
    with hm_tabs[0]:
        st.markdown("#### 🔗 Multi-Metric UX & HEART Correlation Heatmap")
        
        all_corr_vars = ["NPS_Response", "CSAT_Response", "sus_score", "CES_Response", "TTFV_min", "Errors", "Sessions", "Core_Action", "Day7_Return", "Task_Completed", "User_Error_Rate", "Ux_Risk_Points"]
        labels_map = {"NPS_Response": "NPS", "CSAT_Response": "CSAT", "sus_score": "SUS Score", "CES_Response": "CES Effort", "TTFV_min": "TTFV (Min)", "Errors": "Errors", "Sessions": "Sessions", "Core_Action": "Adoption", "Day7_Return": "Retention", "Task_Completed": "Task Success", "User_Error_Rate": "Error Rate %", "Ux_Risk_Points": "Risk Points"}
        
        c_vars, c_meth, c_color, c_opt = st.columns([2.5, 1.2, 1.2, 1.5])
        with c_vars:
            sel_vars = st.multiselect("Variables to Correlate:", options=all_corr_vars, default=all_corr_vars, format_func=lambda x: labels_map.get(x, x))
        with c_meth:
            corr_m = st.selectbox("Method:", ["pearson", "spearman"])
        with c_color:
            corr_pal = st.selectbox("Palette:", ["RdBu_r", "Viridis", "Plasma", "Turbo", "Blues", "Tealrose"])
        with c_opt:
            show_txt = st.checkbox("Show Values", value=True)
            filter_r = st.slider("Filter |r| ≥", 0.0, 0.9, 0.0, 0.1)
            
        if len(sel_vars) >= 2:
            corr_matrix = calculate_correlations(filtered_df, method=corr_m, selected_cols=sel_vars)
            plot_corr = corr_matrix.copy()
            if filter_r > 0:
                plot_corr = plot_corr.map(lambda x: x if abs(x) >= filter_r else np.nan)
                
            txt_mat = [[f"{v:.2f}" if not np.isnan(v) else "" for v in row] for row in plot_corr.values] if show_txt else None
            
            fig_c = go.Figure(go.Heatmap(
                z=plot_corr.values,
                x=plot_corr.columns,
                y=plot_corr.index,
                text=txt_mat,
                texttemplate="%{text}" if show_txt else None,
                colorscale=corr_pal,
                zmin=-1.0 if corr_pal in ["RdBu_r", "Tealrose"] else 0.0,
                zmax=1.0,
                colorbar=dict(title=dict(text=f"{corr_m.capitalize()} r", side="right"), thickness=15, len=0.9),
                hoverongaps=False,
                hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>Correlation (r): <b>%{z:.3f}</b><extra></extra>"
            ))
            fig_c.update_layout(title=dict(text=f"<b>UX & HEART Correlation Matrix ({corr_m.upper()}, N={len(filtered_df)})</b>", font=dict(size=14, color="#f8fafc")),
                                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                height=520, margin=dict(l=40, r=40, t=50, b=40), xaxis=dict(tickangle=-30), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_c, use_container_width=True)
        else:
            st.info("Please select at least 2 variables.")

    # Heatmap Tab 2: SUS Questions Diagnostic
    with hm_tabs[1]:
        st.markdown("#### 🩺 System Usability Scale (SUS) 10-Question Diagnostic Heatmap")
        sus_cols = [f"SUS_Q{i}" for i in range(1, 11)]
        avail_sus = [c for c in sus_cols if c in filtered_df.columns]
        
        if len(avail_sus) == 10:
            sus_group = st.selectbox("Group SUS Questions By:", ["nps_category", "Ux_Risk_level", "Eng_flag", "Adoptation_Flag", "Retention_Flag", "Task_Complition_Flag"],
                                     format_func=lambda x: {"nps_category": "NPS Category", "Ux_Risk_level": "Risk Level", "Eng_flag": "Engagement Level", "Adoptation_Flag": "Adoption", "Retention_Flag": "Retention", "Task_Complition_Flag": "Task Success"}.get(x, x))
            
            sus_mean = filtered_df.groupby(sus_group)[avail_sus].mean().round(2)
            x_names = [SUS_SHORT_NAMES.get(c, c) for c in avail_sus]
            
            fig_sq = go.Figure(go.Heatmap(
                z=sus_mean.values,
                x=x_names,
                y=[str(idx) for idx in sus_mean.index],
                text=sus_mean.values,
                texttemplate="%{text:.2f}",
                colorscale="Viridis",
                zmin=1.0,
                zmax=5.0,
                colorbar=dict(title="Avg (1-5)", thickness=15),
                hovertemplate="Group: <b>%{y}</b><br>Question: <b>%{x}</b><br>Avg Score: <b>%{z:.2f} / 5.0</b><extra></extra>"
            ))
            fig_sq.update_layout(title=dict(text=f"<b>Average SUS Question Rating (1 to 5 scale) by {sus_group}</b>", font=dict(size=14, color="#f8fafc")),
                                 template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380, xaxis=dict(tickangle=-25))
            st.plotly_chart(fig_sq, use_container_width=True)
            
            with st.expander("📖 View Full SUS 10-Question Definitions"):
                col_p, col_n = st.columns(2)
                with col_p:
                    st.markdown("**🟢 Positive Usability Questions (Higher = Better):**")
                    for q in ["SUS_Q1", "SUS_Q3", "SUS_Q5", "SUS_Q7", "SUS_Q9"]:
                        st.markdown(f"- **{SUS_SHORT_NAMES[q]}**: *{SUS_QUESTIONS[q]}*")
                with col_n:
                    st.markdown("**🔴 Friction / Pain Points (Lower = Better):**")
                    for q in ["SUS_Q2", "SUS_Q4", "SUS_Q6", "SUS_Q8", "SUS_Q10"]:
                        st.markdown(f"- **{SUS_SHORT_NAMES[q]}**: *{SUS_QUESTIONS[q]}*")

    # Heatmap Tab 3: Cross Tabulation
    with hm_tabs[2]:
        st.markdown("#### 🔀 Categorical Cross-Tabulation & Density Heatmap")
        c_x, c_y, c_n = st.columns(3)
        cat_choices = {"nps_category": "NPS Category", "Ux_Risk_level": "Risk Level", "Eng_flag": "Engagement Level", "Adoptation_Flag": "Adoption Status", "Retention_Flag": "Retention Status", "Task_Complition_Flag": "Task Success"}
        valid_c = [k for k in cat_choices.keys() if k in filtered_df.columns]
        
        with c_x:
            cx_val = st.selectbox("X Dimension:", valid_c, index=0, format_func=lambda x: cat_choices.get(x, x))
        with c_y:
            cy_val = st.selectbox("Y Dimension:", valid_c, index=1 if len(valid_c)>1 else 0, format_func=lambda x: cat_choices.get(x, x))
        with c_n:
            norm_opt = st.selectbox("Display Mode:", ["Raw User Counts", "Row %", "Column %", "Total %"])
            
        norm_arg = False
        if norm_opt == "Row %": norm_arg = "index"
        elif norm_opt == "Column %": norm_arg = "columns"
        elif norm_opt == "Total %": norm_arg = "all"
        
        xtab = pd.crosstab(filtered_df[cy_val], filtered_df[cx_val], normalize=norm_arg)
        if norm_arg is not False:
            xtab = (xtab * 100).round(1)
            fmt_str = "%{text:.1f}%"
        else:
            fmt_str = "%{text} Users"
            
        fig_xt = go.Figure(go.Heatmap(
            z=xtab.values,
            x=xtab.columns.tolist(),
            y=xtab.index.tolist(),
            text=xtab.values,
            texttemplate=fmt_str,
            colorscale="Blues",
            colorbar=dict(title="Value", thickness=15),
            hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>Count/Pct: <b>%{z}</b><extra></extra>"
        ))
        fig_xt.update_layout(title=dict(text=f"<b>Cross Tabulation: {cat_choices.get(cy_val, cy_val)} vs {cat_choices.get(cx_val, cx_val)} ({norm_opt})</b>", font=dict(size=14, color="#f8fafc")),
                             template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380)
        st.plotly_chart(fig_xt, use_container_width=True)

    # Heatmap Tab 4: User Cohort Matrix
    with hm_tabs[3]:
        st.markdown("#### 👥 User-Level Multi-Metric Performance Matrix")
        top_n = st.slider("Users to Display:", 10, min(100, len(filtered_df)), min(30, len(filtered_df)), 5)
        sort_v = st.selectbox("Sort Users By:", ["Ux_Risk_Points", "sus_score", "NPS_Response", "TTFV_min", "Sessions", "Errors"])
        
        perf_cols = ["NPS_Response", "CSAT_Response", "sus_score", "Sessions", "TTFV_min", "Errors", "Ux_Risk_Points"]
        avail_p = [c for c in perf_cols if c in filtered_df.columns]
        
        sorted_u = filtered_df.sort_values(by=sort_v, ascending=False).head(top_n)
        norm_u = sorted_u[avail_p].copy()
        for col in norm_u.columns:
            c_min = filtered_df[col].min()
            c_max = filtered_df[col].max()
            norm_u[col] = ((sorted_u[col] - c_min) / (c_max - c_min) * 100) if c_max > c_min else 50.0
            
        u_ids = sorted_u["User_ID"].tolist() if "User_ID" in sorted_u.columns else [f"U{i}" for i in range(len(sorted_u))]
        
        fig_um = go.Figure(go.Heatmap(
            z=norm_u.values,
            x=[labels_map.get(c, c) for c in avail_p],
            y=u_ids,
            text=sorted_u[avail_p].values,
            texttemplate="%{text:.1f}",
            colorscale="Plasma",
            colorbar=dict(title="Scale (0-100)", thickness=14),
            hovertemplate="User: <b>%{y}</b><br>Metric: <b>%{x}</b><br>Raw Value: <b>%{text}</b><extra></extra>"
        ))
        fig_um.update_layout(title=dict(text=f"<b>Normalized User Performance Matrix (Top {top_n} Users sorted by {sort_v})</b>", font=dict(size=14, color="#f8fafc")),
                             template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             height=max(450, top_n * 18), yaxis=dict(dtick=1))
        st.plotly_chart(fig_um, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: UX RISK & EARLY WARNING
# -------------------------------------------------------------
with tab_risk:
    st.markdown("""
    <div class="section-box">
        <h3 style="margin-top:0; color:#f8fafc; font-weight:800; font-size: 19px;">
            ⚠️ UX Risk & Churn Early Warning Center
        </h3>
        <p style="color:#94a3b8; font-size:13px; margin-bottom:0;">
            Identify struggling users, friction hot-spots, and critical abandonment risk indicators.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    rk1, rk2 = st.columns([1, 1.4])
    with rk1:
        if "Ux_Risk_level" in filtered_df.columns:
            rk_cnt = filtered_df["Ux_Risk_level"].value_counts().reset_index()
            rk_cnt.columns = ["Risk Tier", "Users"]
            fig_rk = px.pie(rk_cnt, names="Risk Tier", values="Users", color="Risk Tier",
                            color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}, hole=0.55)
            fig_rk.update_layout(title=dict(text=f"<b>Risk Tier Distribution (Avg: {kpis.get('avg_risk_points', 0):.1f}/9)</b>", font=dict(size=14, color="#f8fafc")),
                                 template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig_rk, use_container_width=True)
    with rk2:
        if "Ux_Risk_Points" in filtered_df.columns:
            fig_rp = px.histogram(filtered_df, x="Ux_Risk_Points", nbins=10, color="Ux_Risk_level" if "Ux_Risk_level" in filtered_df.columns else None,
                                  color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}, text_auto=True)
            fig_rp.update_layout(title=dict(text="<b>UX Risk Points Breakdown (0 = Safe, 9 = Severe)</b>", font=dict(size=14, color="#f8fafc")),
                                 template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350, xaxis=dict(dtick=1))
            st.plotly_chart(fig_rp, use_container_width=True)
            
    st.markdown("#### 🚨 High-Risk Users Requiring Immediate Intervention")
    high_rk_df = filtered_df[filtered_df["Ux_Risk_level"] == "High"] if "Ux_Risk_level" in filtered_df.columns else filtered_df
    disp_cols = [c for c in ["User_ID", "Ux_Risk_Points", "Ux_Risk_level", "NPS_Response", "CSAT_Response", "sus_score", "CES_Response", "TTFV_min", "Errors", "User_Error_Rate", "Adoptation_Flag", "Retention_Flag", "Task_Complition_Flag"] if c in filtered_df.columns]
    st.dataframe(high_rk_df[disp_cols].sort_values(by="Ux_Risk_Points", ascending=False), use_container_width=True, hide_index=True)

# -------------------------------------------------------------
# TAB 4: WHAT-IF SIMULATOR
# -------------------------------------------------------------
with tab_sim:
    st.markdown("""
    <div class="section-box">
        <h3 style="margin-top:0; color:#f8fafc; font-weight:800; font-size: 19px;">
            🔮 Interactive UX Optimization & What-If Simulator
        </h3>
        <p style="color:#94a3b8; font-size:13px; margin-bottom:0;">
            Model the business impact of onboarding acceleration and usability error reduction on NPS and Retention.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown("#### ⚙️ Optimization Levers")
        ttfv_red = st.slider("Target TTFV Reduction (% Faster Value):", 0, 60, 30, 5)
        err_red = st.slider("Target Error Reduction (% Fewer Mistakes):", 0, 70, 40, 5)
        ad_boost = st.slider("Target Adoption Boost (% Increase):", 0, 40, 15, 5)
    with s_col2:
        st.markdown("#### 📈 Projected Metric Forecast")
        curr_nps = kpis.get("nps_score", 0)
        proj_nps = min(100.0, curr_nps + (ttfv_red * 0.45) + (err_red * 0.35))
        
        curr_ret = kpis.get("retention_rate", 0)
        proj_ret = min(100.0, curr_ret + (ttfv_red * 0.25) + (ad_boost * 0.30))
        
        curr_sus = kpis.get("avg_sus", 0)
        proj_sus = min(100.0, curr_sus + (err_red * 0.30) + (ttfv_red * 0.15))
        
        p1, p2, p3 = st.columns(3)
        p1.metric("Projected NPS", f"{proj_nps:+.1f}", delta=f"{proj_nps - curr_nps:+.1f}")
        p2.metric("Projected Retention", f"{proj_ret:.1f}%", delta=f"{proj_ret - curr_ret:+.1f}%")
        p3.metric("Projected SUS Score", f"{proj_sus:.1f}/100", delta=f"{proj_sus - curr_sus:+.1f}")
        
        st.info(f"💡 By reducing TTFV by {ttfv_red}% and eliminating {err_red}% of task friction, NPS is projected to reach **{proj_nps:+.1f}** and Day-7 Retention will climb to **{proj_ret:.1f}%**.")

# -------------------------------------------------------------
# TAB 5: USER SEGMENT EXPLORER
# -------------------------------------------------------------
with tab_users:
    st.markdown("""
    <div class="section-box">
        <h3 style="margin-top:0; color:#f8fafc; font-weight:800; font-size: 19px;">
            👥 User Segment Explorer & Data Export
        </h3>
        <p style="color:#94a3b8; font-size:13px; margin-bottom:0;">
            Search, sort, filter individual user records, and export cohort subsets.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    ux_c1, ux_c2, ux_c3 = st.columns([2, 1, 1])
    with ux_c1:
        sq = st.text_input("🔍 Search User ID:", placeholder="e.g. U001, U042...", key="usr_search")
    with ux_c2:
        sort_c = st.selectbox("Sort By:", [c for c in ["User_ID", "Ux_Risk_Points", "sus_score", "NPS_Response", "CSAT_Response", "TTFV_min", "User_Error_Rate", "Sessions"] if c in filtered_df.columns], index=1)
    with ux_c3:
        sort_asc = st.radio("Order:", ["Descending", "Ascending"], horizontal=True) == "Ascending"
        
    u_df = filtered_df.copy()
    if sq.strip():
        u_df = u_df[u_df["User_ID"].astype(str).str.contains(sq.strip(), case=False, na=False)]
    u_df = u_df.sort_values(by=sort_c, ascending=sort_asc)
    
    st.caption(f"Displaying {len(u_df)} of {len(filtered_df)} users")
    st.dataframe(u_df, use_container_width=True, hide_index=True)
    
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("📥 Download CSV", u_df.to_csv(index=False).encode('utf-8'), "heart_ux_users.csv", "text/csv")
    with d2:
        b = io.BytesIO()
        with pd.ExcelWriter(b, engine='openpyxl') as w:
            u_df.to_excel(w, index=False, sheet_name="Users")
        st.download_button("📊 Download Excel", b.getvalue(), "heart_ux_users.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# -------------------------------------------------------------
# TAB 6: WORKBOOK SHEETS INSPECTOR
# -------------------------------------------------------------
with tab_sheets:
    st.markdown("""
    <div class="section-box">
        <h3 style="margin-top:0; color:#f8fafc; font-weight:800; font-size: 19px;">
            📑 Original Excel Workbook Sheets Browser
        </h3>
        <p style="color:#94a3b8; font-size:13px; margin-bottom:0;">
            Browse and inspect all original sheets from <code>HEART_ANALYSIS.xlsx</code>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    sheet_sel = st.selectbox("Select Sheet:", list(sheets_data.keys()), index=0)
    st.dataframe(sheets_data[sheet_sel], use_container_width=True)
