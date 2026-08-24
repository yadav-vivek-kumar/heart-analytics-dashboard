# ❤️ Google HEART & UX Analytics Studio

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-6.x-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An executive-grade, interactive UX Intelligence & Google HEART Framework Analytics application built with **Streamlit** and **Plotly**. Features automated metric calculation, multi-dimensional correlation and usability diagnostic heatmaps, user cohort segmentation, churn early warning detection, and a what-if optimization simulator.

---

## 🌟 Key Application Features

1. **📊 Executive HEART Dashboard & Scorecard Ribbon**:
   - **Happiness (H)**: Net Promoter Score (NPS) gauge & distribution donut, Customer Satisfaction (CSAT) rating breakdown, and System Usability Scale (SUS) score distribution vs. 68.0 industry benchmark.
   - **Engagement (E)**: Session frequency distributions and cross-analysis with user satisfaction.
   - **Adoption (A)**: Core action adoption funnel and Time-to-First-Value (TTFV in minutes) vs. target thresholds (≤5 min).
   - **Retention (R)**: Day-7 return rate and cohort comparison across promoter/detractor segments.
   - **Task Success (T)**: Task completion success rate and usability error vs. attempt regression scatter plots.

2. **🔥 Multi-Dimensional Heatmap Studio**:
   - **Correlation Heatmap**: Interactive Pearson & Spearman correlation matrix across 12 UX dimensions with customizable colormaps, numerical annotations, and threshold filtering.
   - **SUS 10-Question Diagnostic Heatmap**: Item-level breakdown of all 10 standard SUS questions across user segments (Promoters, Risk tiers, Engagement levels).
   - **Cross-Tabulation Heatmap**: Bivariate contingency density heatmaps (e.g. NPS Category vs. Retention).
   - **User Cohort Performance Matrix**: Min-max normalized multi-metric heatmap across individual users.

3. **⚠️ UX Risk & Churn Early Warning Center**:
   - Automated UX Risk scoring (0–9 scale), risk tier categorization (High, Medium, Low), and high-risk user detection table with prescriptive optimization action items.

4. **🔮 Interactive What-If Optimization Simulator**:
   - Real-time simulation levers to forecast the business impact of onboarding velocity gains and error reductions on NPS and Retention.

5. **👥 User Segment Explorer & Data Table**:
   - Searchable, sortable, and filterable user records table with one-click **CSV** and **Excel** export.

6. **📑 Original Workbook Sheet Inspector**:
   - Complete browser for all 8 workbook sheets (`README`, `Raw_Data`, `ux_matrix`, `NPS_ANALYSIS`, `Sus_analysis`, `CES_TTFV`, `Task_analysis`, `Corelation`).

---

## 📁 Repository Structure

```
heart_analytics_app/
├── app.py                      # Main Streamlit application entry point
├── data_loader.py              # Data ingestion & metric calculations with caching
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   └── config.toml             # Streamlit theme & server configuration
├── data/
│   └── HEART_ANALYSIS.xlsx     # Bundled UX & HEART workbook dataset
├── assets/
│   └── styles.css              # Glassmorphic custom CSS styling
└── components/
    ├── kpi_cards.py            # KPI metric cards ribbon
    ├── heart_dashboard.py      # Google HEART framework visualizer
    ├── heatmap_studio.py       # Interactive Heatmap Studio (Plotly)
    ├── risk_analyzer.py        # UX Risk scoring & high-risk user table
    ├── user_explorer.py        # Filterable user table with CSV/Excel export
    └── sheet_viewer.py         # Multi-sheet workbook browser
```

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/yadav-vivek-kumar/heart-analytics-dashboard.git
cd heart-analytics-dashboard
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Streamlit app
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ How to Deploy on Streamlit Cloud (Free)

1. **Push to GitHub**:
   - Create a new public repository on [GitHub](https://github.com/new) (e.g. `heart-analytics-dashboard`).
   - Push your code:
     ```bash
     git init
     git add .
     git commit -m "Initial commit: Google HEART & UX Analytics Studio"
     git branch -M main
     git remote add origin https://github.com/yadav-vivek-kumar/heart-analytics-dashboard.git
     git push -u origin main
     ```

2. **Deploy on Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
   - Click **"New app"** (or **"Create app"**).
   - Select your repository: `yadav-vivek-kumar/heart-analytics-dashboard`.
   - Set **Branch** to `main`.
   - Set **Main file path** to `app.py`.
   - Click **"Deploy!"**.

Your application will be live with a public URL in less than 2 minutes!

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
