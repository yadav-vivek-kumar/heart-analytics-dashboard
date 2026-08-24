"""
Data loader and metric computation module for Google HEART & UX Analytics.
"""
import os
import pandas as pd
import numpy as np
import streamlit as st

def get_default_excel_path():
    """
    Finds the default Excel path for local or cloud (Streamlit Cloud) environments.
    """
    candidates = [
        os.path.join(os.path.dirname(__file__), "data", "HEART_ANALYSIS.xlsx"),
        os.path.join(os.path.dirname(__file__), "HEART_ANALYSIS.xlsx"),
        r"C:\DOCUMENTS\HEART_ANALYSIS.xlsx"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]

DEFAULT_EXCEL_PATH = get_default_excel_path()

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

@st.cache_data(show_spinner=False)
def load_all_data(file_source=None):
    """
    Loads all sheets from the Excel file.
    Returns a dictionary of DataFrames keyed by sheet name.
    """
    path = file_source if file_source is not None else DEFAULT_EXCEL_PATH
    
    if not os.path.exists(path) and not hasattr(path, "read"):
        raise FileNotFoundError(f"Excel file not found at: {path}")
        
    xl = pd.ExcelFile(path)
    sheets_dict = {}
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        sheets_dict[sheet] = df
        
    # Clean and enrich ux_matrix if present
    if "ux_matrix" in sheets_dict:
        df_ux = sheets_dict["ux_matrix"].copy()
        
        # Standardize categorical names
        if "nps_category" in df_ux.columns:
            # Fix typo 'DECTATOR' -> 'DETRACTOR'
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
            
        sheets_dict["ux_matrix"] = df_ux
        
    return sheets_dict

def compute_sus_score_from_questions(df):
    """
    Computes System Usability Scale (SUS) score based on 10 standardized questions (1-5 scale).
    Odd questions (1, 3, 5, 7, 9): score = response - 1
    Even questions (2, 4, 6, 8, 10): score = 5 - response
    Total score = Sum of contributions * 2.5 (0 - 100 scale)
    """
    odd_cols = ["SUS_Q1", "SUS_Q3", "SUS_Q5", "SUS_Q7", "SUS_Q9"]
    even_cols = ["SUS_Q2", "SUS_Q4", "SUS_Q6", "SUS_Q8", "SUS_Q10"]
    
    odd_sum = sum(df[col] - 1 for col in odd_cols if col in df.columns)
    even_sum = sum(5 - df[col] for col in even_cols if col in df.columns)
    
    sus = (odd_sum + even_sum) * 2.5
    return sus

def compute_heart_kpis(df):
    """
    Computes comprehensive Google HEART Framework metrics from a given UX dataframe.
    """
    n_users = len(df)
    if n_users == 0:
        return {}
        
    # --- HAPPINESS (H) ---
    # NPS
    promoters = (df["NPS_Response"] >= 9).sum() if "NPS_Response" in df.columns else 0
    passives = ((df["NPS_Response"] >= 7) & (df["NPS_Response"] <= 8)).sum() if "NPS_Response" in df.columns else 0
    detractors = (df["NPS_Response"] <= 6).sum() if "NPS_Response" in df.columns else 0
    
    pct_promoters = (promoters / n_users) * 100
    pct_passives = (passives / n_users) * 100
    pct_detractors = (detractors / n_users) * 100
    nps_score = pct_promoters - pct_detractors
    
    # CSAT
    avg_csat = df["CSAT_Response"].mean() if "CSAT_Response" in df.columns else 0.0
    csat_satisfied = (df["CSAT_Response"] >= 4).sum() if "CSAT_Response" in df.columns else 0
    pct_csat_satisfied = (csat_satisfied / n_users) * 100
    
    # SUS
    avg_sus = df["sus_score"].mean() if "sus_score" in df.columns else 0.0
    
    # --- ENGAGEMENT (E) ---
    avg_sessions = df["Sessions"].mean() if "Sessions" in df.columns else 0.0
    high_engagement = (df["Eng_flag"] == "HIGH").sum() if "Eng_flag" in df.columns else 0
    pct_high_eng = (high_engagement / n_users) * 100
    
    # --- ADOPTION (A) ---
    core_actions = (df["Core_Action"] == 1).sum() if "Core_Action" in df.columns else 0
    adoption_rate = (core_actions / n_users) * 100
    avg_ttfv = df["TTFV_min"].mean() if "TTFV_min" in df.columns else 0.0
    fast_ttfv_count = (df["TTFV_min"] <= 5).sum() if "TTFV_min" in df.columns else 0
    pct_fast_ttfv = (fast_ttfv_count / n_users) * 100
    
    # --- RETENTION (R) ---
    day7_returns = (df["Day7_Return"] == 1).sum() if "Day7_Return" in df.columns else 0
    retention_rate = (day7_returns / n_users) * 100
    
    # --- TASK SUCCESS (T) ---
    task_success_count = (df["Task_Completed"] == 1).sum() if "Task_Completed" in df.columns else 0
    task_success_rate = (task_success_count / n_users) * 100
    
    total_attempts = df["Task_Attempts"].sum() if "Task_Attempts" in df.columns else 0
    total_errors = df["Errors"].sum() if "Errors" in df.columns else 0
    overall_error_rate = (total_errors / total_attempts * 100) if total_attempts > 0 else 0.0
    avg_user_error_rate = df["User_Error_Rate"].mean() if "User_Error_Rate" in df.columns else 0.0
    
    # --- UX RISK ---
    avg_risk_points = df["Ux_Risk_Points"].mean() if "Ux_Risk_Points" in df.columns else 0.0
    high_risk_users = (df["Ux_Risk_level"] == "High").sum() if "Ux_Risk_level" in df.columns else 0
    pct_high_risk = (high_risk_users / n_users) * 100
    
    # CES (Customer Effort Score)
    avg_ces = df["CES_Response"].mean() if "CES_Response" in df.columns else 0.0
    low_effort_users = (df["CES_Response"] <= 3).sum() if "CES_Response" in df.columns else 0
    pct_low_effort = (low_effort_users / n_users) * 100

    return {
        "n_users": n_users,
        # Happiness
        "nps_score": nps_score,
        "pct_promoters": pct_promoters,
        "pct_passives": pct_passives,
        "pct_detractors": pct_detractors,
        "promoters": promoters,
        "passives": passives,
        "detractors": detractors,
        "avg_csat": avg_csat,
        "pct_csat_satisfied": pct_csat_satisfied,
        "avg_sus": avg_sus,
        # Engagement
        "avg_sessions": avg_sessions,
        "pct_high_eng": pct_high_eng,
        # Adoption
        "adoption_rate": adoption_rate,
        "avg_ttfv": avg_ttfv,
        "pct_fast_ttfv": pct_fast_ttfv,
        # Retention
        "retention_rate": retention_rate,
        # Task Success
        "task_success_rate": task_success_rate,
        "overall_error_rate": overall_error_rate,
        "avg_user_error_rate": avg_user_error_rate,
        "total_attempts": total_attempts,
        "total_errors": total_errors,
        # Risk & Effort
        "avg_risk_points": avg_risk_points,
        "high_risk_users": high_risk_users,
        "pct_high_risk": pct_high_risk,
        "avg_ces": avg_ces,
        "pct_low_effort": pct_low_effort
    }

def get_correlation_matrix(df, method="pearson", selected_cols=None):
    """
    Computes a correlation matrix for selected UX & HEART numeric variables.
    """
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
    
    available_cols = [c for c in default_mapping.keys() if c in df.columns]
    
    if selected_cols is not None:
        available_cols = [c for c in selected_cols if c in df.columns]
        
    sub_df = df[available_cols].copy()
    sub_df = sub_df.rename(columns={k: default_mapping.get(k, k) for k in available_cols})
    
    corr = sub_df.corr(method=method)
    return corr
