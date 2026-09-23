import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MP Budget 2026-27 Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  — FULL LIGHT THEME, HIGH CONTRAST
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── FORCE LIGHT BACKGROUND ON EVERYTHING — overrides Streamlit Cloud dark mode ── */
    html, body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main, .block-container,
    section[data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarNav"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stHeader"],
    [data-testid="stBottomBlockContainer"],
    div[class*="stApp"], div[class*="main"], div[class*="block-container"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] > div {
        background-color: #EFF3FF !important;
        color: #111111 !important;
    }
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] a { color: #111111 !important; }

    /* ── BODY TEXT ── */
    .main p, .main li, .main span, .main div,
    .block-container p, .block-container li,
    .block-container span, .block-container div,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] div,
    [data-testid="stMarkdownContainer"] { color: #111111 !important; background-color: transparent !important; }

    h1, h2, h3, h4, h5, h6,
    .main h1, .main h2, .main h3 { color: #0A2540 !important; }

    /* ── LABELS & FORM WIDGETS ── */
    label, .stRadio label, .stSelectbox label,
    .stMultiSelect label, .stSlider label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] * {
        color: #111111 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* ── SELECTBOX / INPUT BOXES ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div,
    [data-baseweb="base-input"],
    input, textarea {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 2px solid #1A56DB !important;
        border-radius: 6px !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] div,
    [data-baseweb="select"] li,
    [data-baseweb="popover"] *,
    [data-baseweb="menu"] * {
        color: #111111 !important;
        background-color: #FFFFFF !important;
    }
    /* placeholder text */
    input::placeholder, textarea::placeholder { color: #64748B !important; opacity: 1 !important; }

    /* ── RADIO BUTTONS ── */
    .stRadio div[role="radiogroup"] label {
        color: #111111 !important;
        font-size: 0.97rem !important;
        font-weight: 500 !important;
    }

    /* ── TABS ── */
    [data-testid="stTab"],
    button[data-baseweb="tab"],
    [role="tab"] {
        background-color: #DCE9FF !important;
        color: #0A2540 !important;
        font-weight: 700 !important;
        font-size: 0.97rem !important;
        border-radius: 6px 6px 0 0 !important;
    }
    [aria-selected="true"][data-baseweb="tab"],
    button[data-baseweb="tab"][aria-selected="true"],
    [role="tab"][aria-selected="true"] {
        background-color: #1A56DB !important;
        color: #FFFFFF !important;
        border-bottom: 3px solid #1A56DB !important;
    }

    /* ── STREAMLIT BUTTONS (st.button) — critical fix for Streamlit Cloud dark mode ── */
    .stButton > button,
    button[kind="secondary"],
    button[kind="primary"],
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"] {
        background-color: #1A56DB !important;
        color: #FFFFFF !important;
        border: 2px solid #1A56DB !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.45rem 1.1rem !important;
        cursor: pointer !important;
    }
    .stButton > button:hover,
    [data-testid="baseButton-secondary"]:hover,
    [data-testid="baseButton-primary"]:hover {
        background-color: #0E3FA8 !important;
        color: #FFFFFF !important;
        border-color: #0E3FA8 !important;
    }
    /* text inside buttons — force white */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    [data-testid="baseButton-secondary"] p,
    [data-testid="baseButton-primary"] p {
        color: #FFFFFF !important;
    }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"], details, summary {
        background-color: #F5F8FF !important;
        color: #111111 !important;
        border: 1px solid #B8CCFF !important;
        border-radius: 6px !important;
    }
    details summary p,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: #0A2540 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    details > div { background-color: #F5F8FF !important; color: #111111 !important; }

    /* ── ALERTS / INFO BOXES ── */
    [data-testid="stAlert"],
    [data-testid="stNotification"] {
        background-color: #EFF6FF !important;
        color: #111111 !important;
    }
    [data-testid="stAlert"] *,
    [data-testid="stNotification"] * { color: #111111 !important; }

    /* ── DATAFRAME / TABLE ── */
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] td,
    [data-testid="stTable"] th,
    [data-testid="stTable"] td,
    .dataframe th, .dataframe td {
        background-color: #F0F4FF !important;
        color: #111111 !important;
        border-color: #B8CCFF !important;
    }
    [data-testid="stDataFrame"] thead th { background-color: #1A56DB !important; color: #FFFFFF !important; }

    /* ── METRICS ── */
    [data-testid="stMetric"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"],
    [data-testid="metric-container"],
    [data-testid="metric-container"] * { color: #111111 !important; background-color: transparent !important; }

    /* ── CUSTOM COMPONENT CLASSES ── */
    .main-title {
        font-size: 2.0rem; font-weight: 800; color: #0A2540 !important;
        border-bottom: 4px solid #1A56DB; padding-bottom: 0.4rem; margin-bottom: 0.5rem;
        background-color: transparent !important;
    }
    .sub-title { font-size: 1.15rem; color: #1E3A5F !important; margin-bottom: 1.2rem; font-weight: 500; background-color: transparent !important; }
    .section-header {
        font-size: 1.3rem; font-weight: 700; color: #0A2540 !important;
        border-left: 5px solid #1A56DB; padding-left: 0.7rem;
        margin: 1.2rem 0 0.6rem 0; background-color: #DCE9FF !important;
        padding-top: 0.3rem; padding-bottom: 0.3rem; border-radius: 0 6px 6px 0;
    }
    .kpi-card {
        background: #FFFFFF !important; border: 2px solid #1A56DB !important;
        border-radius: 10px; padding: 1.1rem 0.8rem; text-align: center;
        box-shadow: 0 2px 8px rgba(26,86,219,0.15);
    }
    .kpi-value { font-size: 2.0rem; font-weight: 800; color: #0E3FA8 !important; display: block; }
    .kpi-label { font-size: 0.9rem; color: #1E293B !important; margin-top: 0.3rem; font-weight: 700; display: block; }
    .info-box {
        background: #DBEAFE !important; border-left: 5px solid #1A56DB;
        border-radius: 6px; padding: 0.9rem 1.1rem; margin: 0.7rem 0;
        font-size: 0.97rem; color: #0F172A !important; font-weight: 500;
    }
    .info-box b, .info-box strong { color: #0A2540 !important; }
    .warn-box {
        background: #FFFBEB !important; border-left: 5px solid #B45309;
        border-radius: 6px; padding: 0.9rem 1.1rem; margin: 0.7rem 0;
        font-size: 0.97rem; color: #0F172A !important; font-weight: 500;
    }
    .warn-box b, .warn-box strong { color: #78350F !important; }
    .concept-card {
        background: #FFFFFF !important; border: 2px solid #93ABDB !important;
        border-radius: 10px; padding: 1.1rem; margin: 0.5rem 0;
        color: #0F172A !important; box-shadow: 0 1px 4px rgba(0,0,0,0.10);
    }
    .concept-card b, .concept-card strong { color: #0A2540 !important; }
    .concept-card i, .concept-card em { color: #1E3A5F !important; }

    /* ── ESTIMATE BADGES — high contrast ── */
    .badge-actual {
        background: #166534; color: #FFFFFF !important;
        padding: 3px 10px; border-radius: 14px;
        font-size: 0.82rem; font-weight: 700; border: 1px solid #166534;
        display: inline-block;
    }
    .badge-be {
        background: #1A56DB; color: #FFFFFF !important;
        padding: 3px 10px; border-radius: 14px;
        font-size: 0.82rem; font-weight: 700; border: 1px solid #1A56DB;
        display: inline-block;
    }
    .badge-re {
        background: #92400E; color: #FFFFFF !important;
        padding: 3px 10px; border-radius: 14px;
        font-size: 0.82rem; font-weight: 700; border: 1px solid #92400E;
        display: inline-block;
    }

    .footer { text-align:center; font-size:0.8rem; color:#334155 !important; border-top:2px solid #93ABDB; padding-top:0.9rem; margin-top:2rem; background-color: transparent !important; }
    pre, code { background-color:#F0F4FF !important; color:#0F172A !important; border:1px solid #93ABDB !important; border-radius:4px; }
    hr { border-color:#93ABDB !important; }
    ::-webkit-scrollbar { width:8px; }
    ::-webkit-scrollbar-track { background:#F0F4FF; }
    ::-webkit-scrollbar-thumb { background:#6B8CDA; border-radius:4px; }

    /* ── CATCH-ALL: prevent any dark remnants from Streamlit Cloud ── */
    [data-testid="stAppViewBlockContainer"] { background-color: #FFFFFF !important; }
    .stSpinner > div { color: #1A56DB !important; }
    [data-testid="stStatusWidget"] { background-color: #FFFFFF !important; color: #111111 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING & CLEANING (in-memory only)
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv.xlsx")
    except FileNotFoundError:
        try:
            df = pd.read_csv("MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv")
        except FileNotFoundError:
            st.error("❌ Dataset file not found. Place 'MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv.xlsx' in the same folder as app.py.")
            st.stop()
    df.columns = [c.strip() for c in df.columns]
    for col in ["Indicator", "Indicator_Category", "Subcategory", "Financial_Year", "Estimate_Type", "Unit", "Notes"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df["Sector"] = df["Sector"].fillna("General / Total").astype(str).str.strip()
    df.loc[df["Sector"] == "", "Sector"] = "General / Total"
    df.loc[df["Sector"] == "nan", "Sector"] = "General / Total"
    df["HasSector"] = df["Sector"] != "General / Total"
    return df

df = load_data()

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def fmt_value(val, unit):
    if pd.isna(val): return "N/A"
    if unit == "Rs crore": return f"₹{val:,.0f} crore"
    elif unit == "Rs": return f"₹{val:,.0f}"
    elif unit == "%": return f"{val:.4g}%"
    return f"{val:,.4g} {unit}"

def fmt_crore(val):
    if val >= 100000: return f"₹{val/100000:.2f} lakh crore"
    return f"₹{val:,.0f} crore"

def estimate_badge(et):
    if et == "Actuals": return '<span class="badge-actual">ACTUAL</span>'
    elif et == "BE": return '<span class="badge-be">BUDGET ESTIMATE</span>'
    elif et == "RE": return '<span class="badge-re">REVISED ESTIMATE</span>'
    return f'<span style="background:#f3f4f6;padding:2px 8px;border-radius:12px;font-size:0.78rem;">{et}</span>'

# ── HIGH CONTRAST / ACCESSIBLE COLOUR PALETTE (WCAG AA, weak-eyesight friendly) ──
# Estimate types: widely separated hues, all pass 4.5:1 contrast on white
COLOR_MAP = {
    "Actuals":              "#0A6B3B",   # deep green  — clearly "real/done"
    "BE":                   "#1A56DB",   # strong blue  — "planned"
    "RE":                   "#B45309",   # deep amber   — "revised/mid-year"
    "Projection":           "#6B21A8",   # deep purple
    "14th FC Award Period": "#374151",   # dark grey
    "15th FC Award Period": "#374151",
    "16th FC Award Period": "#374151",
    "Award Period":         "#374151",
}

# Sector colours: 14 distinct, all ≥ 4.5:1 contrast on white bg
SECTOR_COLORS = {
    "Education":        "#1A56DB",   # strong blue
    "Health":           "#0A6B3B",   # deep green
    "Energy":           "#B45309",   # deep amber
    "Agriculture":      "#065F46",   # dark teal-green
    "Social Welfare":   "#6B21A8",   # deep purple
    "Rural Development":"#0E7490",   # dark cyan
    "Transport":        "#9A3412",   # dark orange-red
    "Irrigation":       "#1E40AF",   # navy blue
    "Urban Development":"#4C1D95",   # deep violet
    "Police":           "#374151",   # dark slate
    "Housing":          "#831843",   # dark rose
    "Water Supply":     "#134E4A",   # dark teal
    "Manufacturing":    "#7F1D1D",   # dark red
    "Services":         "#1F2937",   # charcoal
}

def get_color(et): return COLOR_MAP.get(et, "#374151")

def apply_chart_theme(fig, height=None):
    """Force white background + dark readable text on ALL Plotly charts.
    This overrides Streamlit Cloud dark-mode interference."""
    layout_kwargs = dict(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#111111", size=13, family="Arial, sans-serif"),
        title_font=dict(color="#0A2540", size=15, family="Arial, sans-serif"),
        legend=dict(
            bgcolor="#F0F4FF",
            bordercolor="#93ABDB",
            borderwidth=1,
            font=dict(color="#111111", size=12),
        ),
        xaxis=dict(
            color="#111111",
            title_font=dict(color="#111111", size=13),
            tickfont=dict(color="#111111", size=12),
            gridcolor="#D1D9F0",
            linecolor="#93ABDB",
            showgrid=True,
        ),
        yaxis=dict(
            color="#111111",
            title_font=dict(color="#111111", size=13),
            tickfont=dict(color="#111111", size=12),
            gridcolor="#D1D9F0",
            linecolor="#93ABDB",
            showgrid=True,
        ),
        margin=dict(t=60, b=60, l=60, r=30),
    )
    if height:
        layout_kwargs["height"] = height
    fig.update_layout(**layout_kwargs)
    # Force text labels on bars/lines to be dark and readable
    fig.update_traces(
        textfont=dict(color="#111111", size=12, family="Arial, sans-serif"),
        selector=dict(type="bar"),
    )
    fig.update_traces(
        textfont=dict(color="#111111", size=12, family="Arial, sans-serif"),
        selector=dict(type="scatter"),
    )
    # Fix all annotations (reference lines, labels)
    for ann in fig.layout.annotations:
        ann.font = dict(color="#111111", size=12)
    return fig

# ─────────────────────────────────────────────
# DATASET METADATA
# ─────────────────────────────────────────────
INDICATORS    = sorted(df["Indicator"].dropna().unique().tolist())
CATEGORIES    = sorted(df["Indicator_Category"].replace("",pd.NA).dropna().unique().tolist())
SUBCATEGORIES = sorted(df["Subcategory"].replace("",pd.NA).dropna().unique().tolist())
YEARS         = sorted(df["Financial_Year"].replace("",pd.NA).dropna().unique().tolist())
ESTIMATE_TYPES= sorted(df["Estimate_Type"].replace("",pd.NA).dropna().unique().tolist())
UNITS         = sorted(df["Unit"].replace("",pd.NA).dropna().unique().tolist())
SECTORS_RAW   = sorted(df["Sector"].replace("General / Total",pd.NA).dropna().unique().tolist())
CORE_YEARS    = ["2024-25","2025-26","2026-27"]
CORE_ET       = ["Actuals","BE","RE"]

# ─────────────────────────────────────────────
# CHATBOT KNOWLEDGE BASE  (used in DATA DICTIONARY page)
# ─────────────────────────────────────────────
CHATBOT_KB = {
    "gsdp": (
        "**GSDP (Gross State Domestic Product)** is the total market value of all goods and services produced within Madhya Pradesh in one financial year. "
        "Think of it as the 'size' of MP's economy. A higher GSDP generally means more economic activity. "
        "MP's GSDP at current prices for 2026-27 is budgeted at ₹18,48,274 crore.",
        ["gsdp","gross state domestic product","state gdp","economy size"]
    ),
    "be": (
        "**Budget Estimate (BE)** is the original plan the government makes at the START of a financial year. "
        "It is a forecast — not money already spent. The MP government prepares BE in February for the year starting 1 April. "
        "Example: 2026-27 BE for Total Expenditure = ₹4,23,360 crore.",
        ["be","budget estimate","original estimate","planned budget"]
    ),
    "re": (
        "**Revised Estimate (RE)** is an updated version of the Budget Estimate, prepared MID-YEAR (usually in December/January) "
        "after the government sees actual collections and spending. RE is more realistic than BE but still not the final figure. "
        "Example: 2025-26 RE for Total Expenditure = ₹3,79,839 crore vs BE of ₹4,05,315 crore.",
        ["re","revised estimate","mid year","revised budget"]
    ),
    "actuals": (
        "**Actuals** are the real, final figures AFTER a financial year ends and accounts are officially closed. "
        "They represent ground truth — what actually happened. Example: 2024-25 Actuals for Total Expenditure = ₹3,45,938 crore.",
        ["actuals","actual","real figure","actual spending","actual amount"]
    ),
    "financial year": (
        "In India, a **Financial Year** runs from **1 April to 31 March** of the next calendar year. "
        "So '2026-27' = 1 April 2026 to 31 March 2027. The government uses this because the monsoon (which affects agriculture and revenue) "
        "runs April–September, making April a logical start.",
        ["financial year","fiscal year","fy","year","april march"]
    ),
    "receipts": (
        "**Receipts** are all the money/resources that come to the government. This includes taxes collected, "
        "grants received from the central government, and borrowings. "
        "Total Receipts 2026-27 BE = ₹4,23,655 crore. Net Receipts (excluding borrowings) = ₹3,17,465 crore.",
        ["receipts","revenue","income","money coming","government income","total receipts"]
    ),
    "expenditure": (
        "**Expenditure** is all the money the government spends — on salaries, roads, hospitals, schools, pensions, subsidies, etc. "
        "Total Expenditure 2026-27 BE = ₹4,23,360 crore. Net Expenditure (excluding debt repayment) = ₹3,88,923 crore.",
        ["expenditure","spending","expense","spend","total expenditure"]
    ),
    "borrowings": (
        "**Borrowings** are loans the government takes when expenditure exceeds receipts. "
        "The government borrows from markets, banks, and the central government. "
        "Total Borrowings 2026-27 BE = ₹1,06,190 crore. Borrowings add to the state's total outstanding liabilities.",
        ["borrowings","borrow","loan","debt","state loan","total borrowings"]
    ),
    "fiscal deficit": (
        "**Fiscal Deficit** = Total Expenditure - Total Receipts (excluding borrowings). "
        "It is the gap that the government fills by borrowing. "
        "2026-27 BE: Rs 71,458 crore = 3.9% of GSDP. The 16th Finance Commission recommends a limit of 3% of GSDP from 2026-27.",
        ["fiscal deficit","deficit","gap","fiscal gap","deficit gsdp"]
    ),
    "revenue surplus": (
        "**Revenue Surplus** = Revenue Receipts minus Revenue Expenditure. "
        "A positive value means the government's day-to-day income exceeds its day-to-day spending. "
        "MP 2026-27 BE Revenue Surplus = Rs 44 crore (very small, near zero).",
        ["revenue surplus","revenue balance","surplus"]
    ),
    "primary deficit": (
        "**Primary Deficit** = Fiscal Deficit minus Interest Payments. "
        "It shows the deficit BEFORE interest obligations. A falling primary deficit suggests improving fiscal management. "
        "2026-27 BE: Rs 37,724 crore = 2% of GSDP.",
        ["primary deficit","primary balance","interest payments deficit"]
    ),
    "committed expenditure": (
        "**Committed Expenditure** is spending the government is LEGALLY OBLIGATED to make — it cannot easily be cut. "
        "It includes Salaries, Pensions, and Interest Payments. "
        "2026-27 BE Total Committed = Rs 1,37,826 crore = 45% of estimated revenue receipts.",
        ["committed expenditure","salaries pensions interest","obligatory","committed"]
    ),
    "salaries": (
        "**Salaries** = payments to government employees. 2026-27 BE = Rs 75,574 crore = 24.5% of revenue receipts. "
        "This is a committed expenditure — it must be paid regardless of fiscal conditions.",
        ["salaries","salary","wages","employee pay"]
    ),
    "pension": (
        "**Pension** = payments to retired government employees. 2026-27 BE = Rs 28,518 crore = 9.2% of revenue receipts. "
        "Like salaries, this is committed and cannot be easily reduced.",
        ["pension","pensions","retired","retirement"]
    ),
    "interest payment": (
        "**Interest Payment** = interest paid on accumulated borrowings. 2026-27 BE = Rs 33,735 crore = 10.9% of revenue receipts. "
        "Higher outstanding debt means higher interest payments every year.",
        ["interest payment","interest","debt interest","loan interest"]
    ),
    "subsidies": (
        "**Subsidies and Transfers** = money given by the government to support people, sectors, or utilities. "
        "2025-26 BE Total = Rs 69,407 crore = 4.1% of GSDP (higher than all-states average of 2.7%). "
        "Includes power subsidies (Rs 25,142 crore), cash transfers (Rs 20,821 crore), and agriculture subsidies.",
        ["subsidies","transfers","subsidy","cash transfer","power subsidy"]
    ),
    "capital outlay": (
        "**Capital Outlay** = spending on creating physical assets like roads, dams, buildings, equipment. "
        "2026-27 BE = Rs 78,920 crore. Unlike revenue expenditure, capital outlay creates long-term assets.",
        ["capital outlay","capital expenditure","capex","infrastructure","asset creation"]
    ),
    "revenue expenditure": (
        "**Revenue Expenditure** = day-to-day running costs — salaries, pensions, interest, grants, subsidies. "
        "2026-27 BE = Rs 3,08,659 crore. Does NOT create long-term assets.",
        ["revenue expenditure","running costs","day to day","operational"]
    ),
    "central capex loans": (
        "**Central Capex Loans** are 50-year interest-free loans from the central government specifically for capital expenditure. "
        "They are EXCLUDED from the state's normal borrowing ceiling. 2026-27 BE = Rs 16,200 crore.",
        ["central capex","capex loan","50 year","interest free loan","central loan"]
    ),
    "debt repayment": (
        "**Debt Repayment** = amount repaid on earlier borrowings (principal, not interest). "
        "2026-27 BE = Rs 34,437 crore. This is why Total Expenditure is greater than Net Expenditure.",
        ["debt repayment","repayment","repay","principal repayment","loan repayment"]
    ),
    "outstanding liabilities": (
        "**Outstanding Liabilities** = total accumulated debt of the state at end of financial year. "
        "Includes borrowings + public account liabilities (provident funds etc.). "
        "2026-27 BE = 32.5% of GSDP. Projected to fall to 31% by 2028-29.",
        ["outstanding liabilities","total debt","accumulated debt","state debt","liabilities"]
    ),
    "per capita gsdp": (
        "**Per Capita GSDP** = GSDP divided by population. It gives a rough idea of average income per person. "
        "MP 2024-25 Actuals = Rs 1,70,430. India 2024-25 = Rs 2,34,859. "
        "Note: per capita GSDP does NOT show how income is distributed — it is an average.",
        ["per capita","per person","average income","per capita gsdp","per head"]
    ),
    "own tax revenue": (
        "**State's Own Tax Revenue** = taxes collected BY the state government (e.g. SGST, Sales Tax, State Excise, Stamp Duty). "
        "2026-27 BE = Rs 1,17,667 crore = 6.4% of GSDP. SGST is the largest component (36% share).",
        ["own tax","state tax","sgst","sales tax","state revenue","own revenue"]
    ),
    "tax devolution": (
        "**Central Tax Devolution** = MP's share of central taxes (like Income Tax, GST) distributed by the Finance Commission. "
        "MP's share in divisible pool: 7.35% for 2026-31 (16th FC). 2026-27 BE = Rs 1,12,137 crore.",
        ["devolution","tax devolution","central taxes","divisible pool","finance commission share"]
    ),
    "finance commission": (
        "The **Finance Commission** is a constitutional body that decides how central tax revenues are shared between the central "
        "and state governments. The 16th Finance Commission covers 2026-31. MP gets 7.35% of the divisible pool.",
        ["finance commission","fc","16th fc","15th fc","14th fc","divisible pool"]
    ),
    "sector": (
        "A **Sector** in this dataset refers to a specific area of government activity like Education, Health, Agriculture, Energy, etc. "
        "Blank sector = General/Total meaning the indicator applies to the whole government, not one specific sector. "
        "10 sectors together account for about 63-64% of total state expenditure.",
        ["sector","sectoral","education sector","health sector","agriculture sector"]
    ),
    "sgst": (
        "**SGST (State Goods and Services Tax)** = the state's share of GST collected. "
        "It is the largest source of MP's own tax revenue (36% share). "
        "2026-27 BE = Rs 42,311 crore.",
        ["sgst","gst","goods services tax","state gst"]
    ),
    "unit": (
        "**Units** tell you what a number means. In this dataset: "
        "Rs crore = Indian Rupees in crore (1 crore = 10 million); "
        "Rs = Indian Rupees (used for per capita figures); "
        "% = Percentage. "
        "NEVER mix units in comparisons. Rs crore and % cannot be averaged together.",
        ["unit","units","rs crore","rupees","percentage","what is crore"]
    ),
    "spse": (
        "**State Public Sector Enterprises (SPSEs)** are companies owned by the state government. "
        "In 2022-23, 12 SPSEs that finalised accounts reported a combined loss of Rs 1,941 crore. "
        "3 power sector discoms accounted for 91% of this loss.",
        ["spse","state enterprise","public sector","discom","power company"]
    ),
}

def chatbot_response(user_q):
    import re as _re
    q = user_q.lower().strip()
    q = _re.sub(r'[^\w\s]', ' ', q)
    best_key = None
    best_score = 0
    for key, (answer, keywords) in CHATBOT_KB.items():
        score = sum(1 for kw in keywords if kw in q)
        if key in q:
            score += 2
        if score > best_score:
            best_score = score
            best_key = key
    if best_key and best_score > 0:
        return CHATBOT_KB[best_key][0]
    words = set(q.split())
    for key, (answer, keywords) in CHATBOT_KB.items():
        for kw in keywords:
            if any(w in kw for w in words if len(w) > 3):
                return CHATBOT_KB[key][0]
    return ("I don't have a specific answer for that yet. Try asking about: GSDP, BE, RE, Actuals, Receipts, "
            "Expenditure, Borrowings, Fiscal Deficit, Committed Expenditure, Subsidies, Sector, "
            "Financial Year, Debt Repayment, or Own Tax Revenue.")

# ─────────────────────────────────────────────
# NAVIGATION  — 11 sections
# ─────────────────────────────────────────────
PAGES = [
    "🏠 Home — Understand MP Budget",
    "📚 Data Dictionary / Learn",
    "📈 Economy — GSDP",
    "💰 Income & Receipts",
    "💸 Expenditure",
    "🏦 Borrowings & Debt",
    "🏗️ Sector Analysis",
    "🔄 Year & Estimate Comparison",
    "🔍 Indicator Explorer",
    "💡 Insights & Decision Support",
]

st.sidebar.markdown("## 📊 MP Budget 2026-27")
st.sidebar.markdown("*Interactive Analytics Dashboard*")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate to:", PAGES, label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:0.78rem;color:#334155;'>
<b>Dataset:</b> 341 observations · 9 columns<br>
<b>Source:</b> PRS Legislative Research<br>
<b>Budget presented:</b> 18 Feb 2026
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ═══════════════════════════════════════════════════════════
if page == PAGES[0]:
    st.markdown('<div class="main-title">Madhya Pradesh Budget 2026-27</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Understanding the State\'s Economy and Government Finances — An interactive data analytics dashboard for everyone, even without an economics background.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-box">
    <b>Welcome!</b> This dashboard turns the numbers from the Madhya Pradesh State Budget 2026-27 into plain-language
    understanding. Every chart comes with an explanation. Every number is shown with its unit.
    Every term is explained in simple words.
    </div>""", unsafe_allow_html=True)

    cols = st.columns(4)
    for i,(val,label) in enumerate([("341","Data Observations"),("114","Unique Indicators"),("3","Budget Years Covered"),("13","Indicator Categories")]):
        with cols[i]:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{val}</div><div class="kpi-label">{label}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">What is the MP Budget?</div>', unsafe_allow_html=True)
    st.markdown("""
The **Madhya Pradesh State Budget** is the government's annual financial plan. It says:
- **How much money** the government expects to receive (receipts)
- **How much money** it plans to spend (expenditure)
- **Where the gap** between the two will be filled (borrowings)

Think of it like a household budget — but for a state of over **8.5 crore people**.
The budget was presented by the Finance Minister on **18 February 2026**.
""")

    st.markdown('<div class="section-header">The Big Picture — 6 Key Concepts</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="concept-card"><b>🏭 GSDP</b><br><i>Gross State Domestic Product</i><br><br>
        The total value of everything produced in MP in a year. Measures how big the state's economy is.<br><br>
        <b>2026-27 BE: ₹18,48,274 crore</b></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="concept-card"><b>💰 RECEIPTS</b><br><i>Money coming to government</i><br><br>
        Taxes + central government share + grants + borrowings.<br><br>
        <b>2026-27 BE: ₹4,23,655 crore</b></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="concept-card"><b>💸 EXPENDITURE</b><br><i>Money used by government</i><br><br>
        Salaries, roads, hospitals, pensions, subsidies — everything the government spends.<br><br>
        <b>2026-27 BE: ₹4,23,360 crore</b></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="concept-card"><b>🏦 BORROWINGS</b><br><i>Additional financing</i><br><br>
        When expenditure exceeds receipts, the government borrows. Adds to total debt.<br><br>
        <b>2026-27 BE: ₹1,06,190 crore</b></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="concept-card"><b>🔄 DEBT REPAYMENT</b><br><i>Repaying earlier borrowings</i><br><br>
        Every year the government repays some of what it borrowed in past years.<br><br>
        <b>2026-27 BE: ₹34,437 crore</b></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="concept-card"><b>📉 FISCAL DEFICIT</b><br><i>The gap filled by borrowing</i><br><br>
        Total Expenditure minus Total Receipts. Government borrows to fill this gap.<br><br>
        <b>2026-27 BE: ₹71,458 crore (3.9% of GSDP)</b></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Understanding Budget Estimates (BE, RE, Actuals)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="concept-card" style="border-top:3px solid #2563eb;">
        <span class="badge-be">BUDGET ESTIMATE (BE)</span><br><br>
        The <b>original plan</b> made at the start of a financial year. It is a forecast — not actual money spent.
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="concept-card" style="border-top:3px solid #d97706;">
        <span class="badge-re">REVISED ESTIMATE (RE)</span><br><br>
        An <b>updated estimate</b> made mid-year after seeing real collections and spending.
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="concept-card" style="border-top:3px solid #16a34a;">
        <span class="badge-actual">ACTUALS</span><br><br>
        The <b>real, final figure</b> after the year ends and accounts are closed. Ground truth.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">What is a Financial Year?</div>', unsafe_allow_html=True)
    st.info("In India, a financial year runs from **1 April to 31 March** of the next calendar year. So '2026-27' means 1 April 2026 to 31 March 2027.")

    with st.expander("📖 How to read Value + Unit together"):
        st.markdown("""
| Value | Unit | What it means |
|-------|------|---------------|
| 1848274 | Rs crore | ₹18,48,274 crore (≈ ₹18.5 lakh crore) |
| 170430 | Rs | ₹1,70,430 (per person) |
| 6 | % | 6 percent |
| 3.9 | % | 3.9 percent of GSDP |

**Never mix units.** Rs crore figures and % figures cannot be averaged together.
        """)

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 2 — DATA DICTIONARY / LEARN
# ═══════════════════════════════════════════════════════════
elif page == PAGES[1]:
    st.markdown('<div class="main-title">📚 Data Dictionary & Learning Centre</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Understand every term in the dataset — plain language explanations for beginners.</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["💬 Ask a Question", "📖 Column Guide", "📘 Economic Terms A–Z", "🔍 How to Read a Row"])

    # ── TAB 1: CHATBOT ──────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">💬 Ask About Any Budget Term</div>', unsafe_allow_html=True)
        st.markdown("""<div class="info-box">Type any budget or economics term below and get a plain-language explanation.
        Examples: <b>What is GSDP?</b> · <b>Explain BE</b> · <b>What are subsidies?</b> · <b>What is fiscal deficit?</b>
        </div>""", unsafe_allow_html=True)
        user_question = st.text_input("Your question:", placeholder="e.g. What is GSDP? or Explain fiscal deficit")
        if user_question and user_question.strip():
            answer = chatbot_response(user_question)
            st.markdown(f"""<div class="concept-card" style="border-left:5px solid #2563EB;">
            <b>Answer:</b><br><br>{answer}
            </div>""", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Or click a topic to learn:**")
        topic_cols = st.columns(4)
        quick_topics = ["GSDP","BE","RE","Actuals","Fiscal Deficit","Borrowings","Subsidies","Committed Expenditure",
                        "Own Tax Revenue","Sector","Financial Year","Per Capita GSDP"]
        for idx, topic in enumerate(quick_topics):
            with topic_cols[idx % 4]:
                if st.button(topic, key=f"quick_{topic}"):
                    ans = chatbot_response(topic)
                    st.markdown(f"""<div class="concept-card">{ans}</div>""", unsafe_allow_html=True)

    # ── TAB 2: COLUMN GUIDE ─────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">📖 Dataset Column Explanations</div>', unsafe_allow_html=True)
        cols_info = [
            ("Indicator","The name of the economic or fiscal measure being recorded. Examples: GSDP (current prices), Total Expenditure, Fiscal Deficit."),
            ("Indicator_Category","A broad grouping of indicators. Examples: GSDP, Expenditure, Receipts, Borrowings, Fiscal Position."),
            ("Subcategory","A more specific classification within the category. Examples: Net Expenditure, Own Tax Revenue, Committed Expenditure."),
            ("Financial_Year","The Indian financial year (1 April – 31 March). Format: 2024-25 means April 2024 to March 2025."),
            ("Estimate_Type","Whether the figure is: Actuals (real final data), BE (original plan), RE (mid-year revised plan), or Projection."),
            ("Value","The numeric value of the indicator. ALWAYS read together with Unit."),
            ("Unit","What the Value means: Rs crore (₹ in crore), Rs (₹ per person), or % (percentage)."),
            ("Sector","The area of government activity, e.g. Education, Health, Agriculture. Blank = General / Total (applies to the whole government)."),
            ("Notes","Source reference (e.g. Table 1, narrative p.2) and any important context about the data point."),
        ]
        for col_name, col_desc in cols_info:
            st.markdown(f"""<div class="concept-card">
            <b style="font-size:1.05rem;color:#1D4ED8;">{col_name}</b><br>{col_desc}
            </div>""", unsafe_allow_html=True)

    # ── TAB 3: ECONOMIC TERMS A–Z ───────────────────────────
    with tab3:
        st.markdown('<div class="section-header">📘 Major Economic & Budget Terms</div>', unsafe_allow_html=True)
        terms = [
            ("GSDP (Gross State Domestic Product)",
             "Total market value of all goods and services produced in MP in one year.",
             "Measures the size of MP's economy. Higher GSDP = larger economy.",
             "If MP produces ₹18 lakh crore worth of goods/services in 2026-27, GSDP = ₹18 lakh crore."),
            ("Current Prices vs Constant Prices",
             "Current prices = values at today's prices (includes inflation). Constant prices = adjusted for inflation to a fixed base year (2011-12).",
             "Constant price growth tells you real growth; current price growth includes inflation.",
             "If GSDP grows 11% in current prices but inflation is 5%, real growth is ~6%."),
            ("GSDP Growth Rate",
             "The % change in GSDP from one year to the next.",
             "MP's 2024-25 GSDP growth at constant prices = 6% (India = 6.5%).",
             "A 6% growth rate means the economy grew by 6% after removing inflation."),
            ("Per Capita GSDP",
             "GSDP divided by the state's population. A rough indicator of average income per person.",
             "MP 2024-25 = ₹1,70,430. India = ₹2,34,859. Does NOT show income distribution.",
             "If 10 people share ₹100, average = ₹10. But some may have ₹50, others ₹1."),
            ("Fiscal Deficit",
             "Total Expenditure minus Total Receipts (excluding borrowings). The gap filled by borrowing.",
             "2026-27 BE = ₹71,458 crore = 3.9% of GSDP.",
             "If you earn ₹80 but spend ₹100, your fiscal deficit is ₹20."),
            ("Revenue Surplus",
             "Revenue Receipts minus Revenue Expenditure. Positive = day-to-day income > day-to-day spending.",
             "MP 2026-27 BE = ₹44 crore (near-zero). A Revenue Deficit means day-to-day spending funded by borrowing.",
             "Think of it as: monthly salary vs monthly bills (excluding investments)."),
            ("Primary Deficit",
             "Fiscal Deficit minus Interest Payments. Shows deficit before interest burden.",
             "2026-27 BE = ₹37,724 crore = 2% of GSDP. Falling primary deficit signals improving finances.",
             "If total deficit is ₹70,000 crore and interest is ₹33,000 crore, primary deficit = ₹37,000 crore."),
            ("Outstanding Liabilities",
             "Total accumulated debt at end of financial year (borrowings + public account liabilities).",
             "2026-27 BE = 32.5% of GSDP. Higher % means larger debt relative to economy.",
             "Like a household's total loan outstanding vs annual income."),
            ("Committed Expenditure",
             "Expenditure the government is legally obligated to make: Salaries + Pensions + Interest.",
             "2026-27 BE = ₹1,37,826 crore = 45% of revenue receipts. Hard to cut.",
             "Think of rent + EMI + insurance — fixed monthly obligations."),
            ("Capital Outlay",
             "Spending on creating physical assets: roads, dams, buildings, equipment.",
             "2026-27 BE = ₹78,920 crore. Creates long-term assets unlike revenue expenditure.",
             "Building a school = capital outlay. Teacher salary = revenue expenditure."),
            ("Central Tax Devolution",
             "MP's constitutionally guaranteed share of centrally collected taxes.",
             "MP gets 7.35% of divisible pool (16th FC, 2026-31). 2026-27 BE = ₹1,12,137 crore.",
             "Like receiving a fixed share of a common pot based on Finance Commission formula."),
            ("Finance Commission",
             "Constitutional body that decides central-state tax sharing and grants every 5 years.",
             "16th FC covers 2026-31. MP gets 7.35% of divisible pool.",
             "Like a referee deciding how to split national tax revenues between states."),
            ("SGST",
             "State Goods and Services Tax — the state's share of GST on goods and services.",
             "Largest source of MP's own tax revenue. 2026-27 BE = ₹42,311 crore (36% share).",
             "When you buy something and pay GST, the state gets SGST."),
            ("Subsidies and Transfers",
             "Money given by government to support people (cash transfers), sectors (agriculture), or utilities (power).",
             "MP 2025-26 BE = ₹69,407 crore = 4.1% of GSDP (above all-states average of 2.7%).",
             "Ladli Behna Yojana (₹23,883 crore) is a cash transfer scheme."),
        ]
        for name, what, why, example in terms:
            with st.expander(f"📌 {name}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**What is it?**\n\n{what}")
                    st.markdown(f"**Simple example:**\n\n*{example}*")
                with c2:
                    st.markdown(f"**Why does it matter?**\n\n{why}")

    # ── TAB 4: HOW TO READ A ROW ────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">🔍 How to Read an Actual Dataset Row</div>', unsafe_allow_html=True)
        st.markdown("""<div class="info-box">
        Each row in the dataset represents <b>one data point</b> — a single measurement for one indicator, one year, one estimate type.
        Below are real rows from the dataset, translated into plain language.
        </div>""", unsafe_allow_html=True)

        example_rows = [
            {
                "Indicator": "GSDP (current prices)",
                "Category": "GSDP", "Subcategory": "GSDP",
                "Financial_Year": "2026-27", "Estimate_Type": "BE",
                "Value": "18,48,274", "Unit": "Rs crore", "Sector": "—",
                "Plain": "In 2026-27, the government has estimated (Budget Estimate) that the total value of everything produced in Madhya Pradesh will be ₹18,48,274 crore. This is at current market prices (not adjusted for inflation). This is a PLAN made in February 2026 — not confirmed actual data."
            },
            {
                "Indicator": "Fiscal Deficit as % of GSDP",
                "Category": "Fiscal Position", "Subcategory": "Fiscal Deficit",
                "Financial_Year": "2024-25", "Estimate_Type": "Actuals",
                "Value": "4.3", "Unit": "%", "Sector": "—",
                "Plain": "In 2024-25, the actual (real, final) fiscal deficit was 4.3% of GSDP. This means the government's spending exceeded its non-borrowing receipts by an amount equal to 4.3% of the state economy. This is ACTUAL data — the year has ended and accounts are closed."
            },
            {
                "Indicator": "Sector Expenditure - Education Sports Arts and Culture",
                "Category": "Sector Expenditure", "Subcategory": "Sector",
                "Financial_Year": "2026-27", "Estimate_Type": "BE",
                "Value": "52,917", "Unit": "Rs crore", "Sector": "Education",
                "Plain": "In 2026-27, the government has budgeted (Budget Estimate) ₹52,917 crore for the Education, Sports, Arts and Culture sector. This is 13% more than the 2025-26 Revised Estimate. This is a planned figure — it may change if actual collections differ."
            },
            {
                "Indicator": "Per Capita GSDP (current prices)",
                "Category": "GSDP", "Subcategory": "Per Capita GSDP",
                "Financial_Year": "2024-25", "Estimate_Type": "Actuals",
                "Value": "1,70,430", "Unit": "Rs", "Sector": "—",
                "Plain": "In 2024-25, the average GSDP per person in MP was ₹1,70,430 (actual). Note: this is an AVERAGE — it does not mean every person earned this amount. Some earned much more, others much less. For comparison, India's per capita GDP was ₹2,34,859."
            },
            {
                "Indicator": "Borrowings",
                "Category": "Borrowings", "Subcategory": "Total Borrowings",
                "Financial_Year": "2025-26", "Estimate_Type": "RE",
                "Value": "1,01,153", "Unit": "Rs crore", "Sector": "—",
                "Plain": "In 2025-26, the Revised Estimate for total borrowings is ₹1,01,153 crore. This is lower than the original Budget Estimate of ₹1,08,751 crore — suggesting the government revised its borrowing needs downward mid-year. This is still NOT the actual final figure."
            },
        ]
        for ex in example_rows:
            with st.expander(f"📄 Row: {ex['Indicator']} | {ex['Financial_Year']} | {ex['Estimate_Type']}"):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown("**Raw data values:**")
                    st.markdown(f"""
| Field | Value |
|-------|-------|
| Indicator | {ex['Indicator']} |
| Category | {ex['Category']} |
| Subcategory | {ex['Subcategory']} |
| Financial Year | {ex['Financial_Year']} |
| Estimate Type | {ex['Estimate_Type']} |
| Value | {ex['Value']} |
| Unit | {ex['Unit']} |
| Sector | {ex['Sector']} |
""")
                with c2:
                    st.markdown("**In plain words:**")
                    st.markdown(f"""<div class="info-box">{ex['Plain']}</div>""", unsafe_allow_html=True)

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 3 — ECONOMY / GSDP
# ═══════════════════════════════════════════════════════════
elif page == PAGES[2]:
    st.markdown('<div class="main-title">📈 Economy — GSDP</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Gross State Domestic Product: the size and growth of Madhya Pradesh\'s economy.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-box">
    <b>What is GSDP?</b> Gross State Domestic Product = total value of all goods and services produced in MP in one year.
    Think of it as the economy's size. A larger GSDP means more economic activity. The dataset contains GSDP at
    <b>current prices</b> (includes inflation) and growth rate at <b>constant prices</b> (adjusted for inflation, base 2011-12).
    </div>""", unsafe_allow_html=True)

    # KPI row
    gsdp_df = df[df["Indicator_Category"] == "GSDP"].copy()
    gsdp_curr = gsdp_df[gsdp_df["Subcategory"] == "GSDP"].copy()
    val_2627_be = gsdp_curr[(gsdp_curr["Financial_Year"]=="2026-27")&(gsdp_curr["Estimate_Type"]=="BE")]["Value"]
    val_2425_act = gsdp_curr[(gsdp_curr["Financial_Year"]=="2024-25")&(gsdp_curr["Estimate_Type"]=="Actuals")]["Value"]
    growth_row = gsdp_df[(gsdp_df["Subcategory"]=="GSDP Growth")&(gsdp_df["Financial_Year"]=="2024-25")]
    pc_row = gsdp_df[(gsdp_df["Subcategory"]=="Per Capita GSDP")&(gsdp_df["Financial_Year"]=="2024-25")]

    kc = st.columns(4)
    with kc[0]:
        v = val_2627_be.values[0] if len(val_2627_be) > 0 else None
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">GSDP 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[1]:
        v2 = val_2425_act.values[0] if len(val_2425_act) > 0 else None
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v2) if v2 else 'N/A'}</span>
        <span class="kpi-label">GSDP 2024-25 Actuals</span></div>""", unsafe_allow_html=True)
    with kc[2]:
        g = growth_row["Value"].values[0] if len(growth_row) > 0 else None
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{g}%</span>
        <span class="kpi-label">MP Growth 2024-25 (const. prices)</span></div>""", unsafe_allow_html=True)
    with kc[3]:
        pc = pc_row["Value"].values[0] if len(pc_row) > 0 else None
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">₹{pc:,.0f}</span>
        <span class="kpi-label">Per Capita GSDP 2024-25 (₹)</span></div>""", unsafe_allow_html=True)

    st.markdown("---")
    tab_g1, tab_g2, tab_g3, tab_g4 = st.tabs(["📊 GSDP Trend", "📈 Growth Rate", "👤 Per Capita", "🏭 Sectoral Share"])

    with tab_g1:
        st.markdown('<div class="section-header">GSDP at Current Prices — Across Years & Estimate Types</div>', unsafe_allow_html=True)
        plot_df = gsdp_curr[gsdp_curr["Value"].notna()].copy()
        if not plot_df.empty:
            fig = px.bar(plot_df, x="Financial_Year", y="Value", color="Estimate_Type",
                         barmode="group", title="GSDP at Current Prices (₹ crore)",
                         color_discrete_map=COLOR_MAP,
                         labels={"Value":"GSDP (₹ crore)","Financial_Year":"Financial Year","Estimate_Type":"Estimate Type"})
            fig.update_traces(texttemplate="%{y:,.0f}", textposition="outside",
                              textfont=dict(color="#111111", size=11))
            apply_chart_theme(fig)
            fig.update_layout(legend_title="Estimate Type")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>What this shows:</b> GSDP values for 2024-25 (Actuals), 2025-26 (BE and RE), and 2026-27 (BE).<br>
        <b>Why it matters:</b> Comparing BE vs RE for the same year shows how the estimate changed mid-year.<br>
        <b>How to read it:</b> Taller bar = larger GSDP. Green = Actual (real), Blue = Budget Estimate, Orange = Revised Estimate.<br>
        <b>Important:</b> 2026-27 BE is a plan, not confirmed data. 2024-25 Actuals are the most reliable figure.
        </div>""", unsafe_allow_html=True)

        st.markdown("**Data table:**")
        disp = plot_df[["Financial_Year","Estimate_Type","Value","Unit"]].copy()
        disp["Formatted Value"] = disp.apply(lambda r: fmt_value(r["Value"], r["Unit"]), axis=1)
        st.dataframe(disp[["Financial_Year","Estimate_Type","Formatted Value","Unit"]].reset_index(drop=True), use_container_width=True)

    with tab_g2:
        st.markdown('<div class="section-header">GSDP Growth Rate (Constant Prices, Base 2011-12)</div>', unsafe_allow_html=True)
        growth_df = gsdp_df[gsdp_df["Subcategory"]=="GSDP Growth"].copy()
        india_df = gsdp_df[gsdp_df["Subcategory"]=="GSDP Growth (India reference)"].copy()
        if not growth_df.empty:
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=growth_df["Financial_Year"], y=growth_df["Value"],
                                  name="MP GSDP Growth %", marker_color="#2563EB",
                                  text=growth_df["Value"].apply(lambda v: f"{v}%"), textposition="outside"))
            if not india_df.empty:
                fig2.add_trace(go.Scatter(x=india_df["Financial_Year"], y=india_df["Value"],
                                          mode="markers+text", name="India GDP Growth %",
                                          marker=dict(color="#DC2626", size=12, symbol="diamond"),
                                          text=india_df["Value"].apply(lambda v: f"India: {v}%"),
                                          textposition="top center"))
            apply_chart_theme(fig2)
            fig2.update_layout(title="MP GSDP Growth Rate vs India (2024-25, Constant Prices)",
                                yaxis_title="Growth Rate (%)", xaxis_title="Financial Year",
                                legend=dict(orientation="h", bgcolor="#F0F4FF", font=dict(color="#111111")))
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>What this shows:</b> How fast MP's economy grew in real terms (inflation removed).<br>
        <b>Why it matters:</b> Real growth tells you if the economy is actually producing more, not just due to rising prices.<br>
        <b>MP 2024-25:</b> 6% growth. <b>India 2024-25:</b> 6.5% growth (reference only).<br>
        <b>Important:</b> Only 2024-25 data available for this indicator. Cannot draw a multi-year trend from one point.
        </div>""", unsafe_allow_html=True)

    with tab_g3:
        st.markdown('<div class="section-header">Per Capita GSDP — MP vs India (2024-25 Actuals)</div>', unsafe_allow_html=True)
        pc_df = gsdp_df[(gsdp_df["Subcategory"].isin(["Per Capita GSDP","Per Capita GDP (India reference)"]))].copy()
        if not pc_df.empty:
            pc_df["Label"] = pc_df["Subcategory"].str.replace("Per Capita ","").str.replace("(India reference)","India").str.strip()
            fig3 = px.bar(pc_df, x="Label", y="Value", color="Label",
                          title="Per Capita GSDP/GDP at Current Prices (₹, 2024-25 Actuals)",
                          color_discrete_sequence=["#2563EB","#DC2626"],
                          labels={"Value":"Per Capita (₹)","Label":""})
            fig3.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside",
                               textfont=dict(color="#111111", size=11))
            apply_chart_theme(fig3)
            fig3.update_layout(showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>What this shows:</b> Average GSDP per person in MP (₹1,70,430) vs India average (₹2,34,859) in 2024-25.<br>
        <b>Why it matters:</b> It gives a rough comparison of MP's economic output per person relative to the national average.<br>
        <b>Important:</b> Per capita figures are simple averages. They do NOT show inequality or income distribution.
        MP's lower per capita does NOT automatically mean every MP resident is poorer than average.<br>
        <b>MP per capita was 10% higher than 2023-24</b> (as per dataset notes).
        </div>""", unsafe_allow_html=True)

    with tab_g4:
        st.markdown('<div class="section-header">Sectoral Share of GSDP (2024-25 Actuals, Current Prices)</div>', unsafe_allow_html=True)
        sec_df = gsdp_df[(gsdp_df["Subcategory"]=="Sectoral Share of GSDP")&(gsdp_df["Value"].notna())].copy()
        if not sec_df.empty:
            fig4 = px.pie(sec_df, names="Sector", values="Value",
                          title="GSDP Sectoral Composition — 2024-25 Actuals (%)",
                          color="Sector",
                          color_discrete_map=SECTOR_COLORS,
                          hole=0.35)
            fig4.update_traces(texttemplate="%{label}: %{value}%", textposition="inside",
                               textfont=dict(color="#FFFFFF", size=12))
            apply_chart_theme(fig4)
            st.plotly_chart(fig4, use_container_width=True)
            st.dataframe(sec_df[["Sector","Value","Unit","Financial_Year","Estimate_Type"]].reset_index(drop=True), use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>What this shows:</b> Agriculture = 44%, Services = 37%, Manufacturing = 19% of GSDP in 2024-25.<br>
        <b>Why it matters:</b> MP has a larger agricultural share than most large Indian states, reflecting its rural economy.<br>
        <b>Important:</b> Only 2024-25 Actuals data available. Cannot show how composition changed over multiple years.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 4 — INCOME & RECEIPTS
# ═══════════════════════════════════════════════════════════
elif page == PAGES[3]:
    st.markdown('<div class="main-title">💰 Income & Receipts</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">All the money and resources coming to the MP government.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-box">
    <b>What are Receipts?</b> Receipts = everything that comes in to the government. This includes:
    own taxes (SGST, Sales Tax, Excise), central tax devolution, central grants, non-debt capital receipts, and borrowings.
    <b>Total Receipts</b> includes borrowings. <b>Net Receipts</b> excludes borrowings.
    </div>""", unsafe_allow_html=True)

    rec_df = df[df["Indicator_Category"].isin(["Receipts","Own Tax Revenue"])].copy()
    tr_df = df[df["Indicator"]=="Total Receipts"].copy()
    nr_df = df[df["Indicator"]=="Net Receipts (excl. borrowings)"].copy()
    rr_df = df[df["Indicator"]=="Revenue Receipts"].copy()
    otr_df = df[df["Indicator"]=="State's Own Tax Revenue"].copy()

    # KPIs
    kc = st.columns(4)
    def get_val(dframe, fy, et):
        r = dframe[(dframe["Financial_Year"]==fy)&(dframe["Estimate_Type"]==et)]["Value"]
        return r.values[0] if len(r) > 0 else None
    with kc[0]:
        v = get_val(tr_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Total Receipts 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[1]:
        v = get_val(nr_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Net Receipts 2026-27 BE (excl. borrowings)</span></div>""", unsafe_allow_html=True)
    with kc[2]:
        v = get_val(rr_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Revenue Receipts 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[3]:
        v = get_val(otr_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Own Tax Revenue 2026-27 BE</span></div>""", unsafe_allow_html=True)

    st.markdown("---")
    tab_r1, tab_r2, tab_r3, tab_r4 = st.tabs(["📊 Receipts Trend", "🏠 Own Tax Revenue", "🏛️ Central Transfers", "📋 Revenue Structure"])

    with tab_r1:
        st.markdown('<div class="section-header">Total & Net Receipts — Year & Estimate Comparison</div>', unsafe_allow_html=True)
        comb = pd.concat([tr_df.assign(Series="Total Receipts"), nr_df.assign(Series="Net Receipts")])
        comb = comb[comb["Value"].notna()].copy()
        if not comb.empty:
            fig = px.bar(comb, x="Financial_Year", y="Value", color="Estimate_Type",
                         facet_col="Series", barmode="group",
                         color_discrete_map=COLOR_MAP,
                         title="Total & Net Receipts by Year & Estimate Type (₹ crore)",
                         labels={"Value":"₹ crore","Financial_Year":"Financial Year"})
            apply_chart_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>What this shows:</b> Total Receipts (including borrowings) and Net Receipts (excluding borrowings) across years.<br>
        <b>Why it matters:</b> Net Receipts is a better measure of the government's own resource mobilisation.<br>
        <b>Note:</b> Net Receipts 2026-27 BE = ₹3,17,465 crore, a 14% increase over 2025-26 RE per the dataset notes.
        </div>""", unsafe_allow_html=True)

    with tab_r2:
        st.markdown('<div class="section-header">State\'s Own Tax Revenue Components (2026-27 BE)</div>', unsafe_allow_html=True)
        otr_comp_df = df[df["Indicator_Category"]=="Own Tax Revenue"].copy()
        be_2627 = otr_comp_df[(otr_comp_df["Estimate_Type"]=="BE")&(otr_comp_df["Financial_Year"]=="2026-27")&(otr_comp_df["Unit"]=="Rs crore")].copy()
        if not be_2627.empty:
            fig2 = px.bar(be_2627.sort_values("Value", ascending=True),
                          y="Subcategory", x="Value", orientation="h",
                          title="Own Tax Revenue Components — 2026-27 BE (₹ crore)",
                          color="Value", color_continuous_scale="Blues",
                          labels={"Value":"₹ crore","Subcategory":"Tax Head"})
            fig2.update_traces(texttemplate="₹%{x:,.0f}", textposition="outside",
                               textfont=dict(color="#111111", size=11))
            apply_chart_theme(fig2)
            fig2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("**Own Tax Revenue — Year Comparison (₹ crore):**")
        otr_trend = otr_df[otr_df["Unit"]=="Rs crore"].copy()
        if not otr_trend.empty:
            fig3 = px.line(otr_trend, x="Financial_Year", y="Value", color="Estimate_Type",
                           markers=True, color_discrete_map=COLOR_MAP,
                           title="State's Own Tax Revenue Trend (₹ crore)",
                           labels={"Value":"₹ crore"})
            fig3.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""<div class="info-box">
        <b>Largest own tax source:</b> SGST (₹42,311 crore, 36% share). Followed by Sales Tax/VAT and State Excise.<br>
        <b>Why it matters:</b> Own tax revenue is the government's self-generated income — not dependent on central transfers.<br>
        <b>Own Tax Revenue as % of GSDP:</b> 6.3% (2024-25 Actuals), 6.4% (2026-27 BE).
        </div>""", unsafe_allow_html=True)

    with tab_r3:
        st.markdown('<div class="section-header">Central Transfers: Devolution & Grants-in-Aid</div>', unsafe_allow_html=True)
        dev_df = df[df["Indicator"]=="Share in Central Taxes (Devolution)"].copy()
        grn_df = df[df["Indicator"]=="Grants-in-aid from Centre"].copy()
        ctr = pd.concat([dev_df.assign(Series="Tax Devolution"), grn_df.assign(Series="Grants from Centre")])
        ctr = ctr[ctr["Unit"]=="Rs crore"].copy()
        if not ctr.empty:
            fig4 = px.bar(ctr, x="Financial_Year", y="Value", color="Series",
                          barmode="group", facet_col="Estimate_Type",
                          color_discrete_sequence=["#2563EB","#16A34A"],
                          title="Central Tax Devolution & Grants-in-Aid (₹ crore)",
                          labels={"Value":"₹ crore"})
            fig4.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("""<div class="info-box">
        <b>Central Tax Devolution 2026-27 BE:</b> ₹1,12,137 crore (36% of revenue receipts).<br>
        <b>Grants from Centre 2026-27 BE:</b> ₹54,505 crore (18% of revenue receipts).<br>
        <b>MP's share in divisible pool:</b> 7.35% (16th FC, 2026-31) — slightly lower than 15th FC (7.85%).<br>
        <b>What this means:</b> 54% of MP's revenue receipts come from the central government.
        </div>""", unsafe_allow_html=True)

    with tab_r4:
        st.markdown('<div class="section-header">Revenue Receipts Structure — 2026-27 BE</div>', unsafe_allow_html=True)
        comp_2627 = {
            "Own Tax Revenue": 117667,
            "Own Non-Tax Revenue": 24394,
            "Central Tax Devolution": 112137,
            "Grants from Centre": 54505,
        }
        comp_df = pd.DataFrame(list(comp_2627.items()), columns=["Source","Value (₹ crore)"])
        fig5 = px.pie(comp_df, names="Source", values="Value (₹ crore)",
                      title="Revenue Receipts Composition — 2026-27 BE",
                      hole=0.35, color_discrete_sequence=["#2563EB","#7C3AED","#16A34A","#D97706"])
        fig5.update_traces(texttemplate="%{label}<br>₹%{value:,.0f} cr", textposition="inside",
                           textfont=dict(color="#FFFFFF", size=12))
        apply_chart_theme(fig5)
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>Own resources (46%):</b> Own Tax + Own Non-Tax Revenue = ₹1,42,061 crore.<br>
        <b>From Centre (54%):</b> Devolution (36%) + Grants (18%) = ₹1,66,642 crore.<br>
        <b>What this means:</b> More than half of MP's regular revenue comes from the central government.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 5 — EXPENDITURE
# ═══════════════════════════════════════════════════════════
elif page == PAGES[4]:
    st.markdown('<div class="main-title">💸 Expenditure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">How the MP government uses its money — salaries, infrastructure, subsidies, and more.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-box">
    <b>Total Expenditure</b> = all spending including debt repayment.<br>
    <b>Net Expenditure</b> = Total Expenditure minus Debt Repayment (shows what was actually spent on programmes).<br>
    <b>Revenue Expenditure</b> = day-to-day costs (salaries, pensions, interest, subsidies).<br>
    <b>Capital Outlay</b> = investment in assets (roads, dams, buildings).<br>
    <b>Committed Expenditure</b> = legally obligated spending that cannot easily be cut.
    </div>""", unsafe_allow_html=True)

    te_df = df[df["Indicator"]=="Total Expenditure"].copy()
    ne_df = df[df["Indicator"]=="Net Expenditure (excl. debt repayment)"].copy()
    re_df = df[df["Indicator"]=="Revenue Expenditure"].copy()
    co_df = df[df["Indicator"]=="Capital Outlay"].copy()
    ce_df = df[df["Indicator"]=="Total Committed Expenditure"].copy()

    kc = st.columns(4)
    def gv(dframe, fy, et):
        r = dframe[(dframe["Financial_Year"]==fy)&(dframe["Estimate_Type"]==et)]["Value"]
        return r.values[0] if len(r) > 0 else None
    with kc[0]:
        v = gv(te_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Total Expenditure 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[1]:
        v = gv(ne_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Net Expenditure 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[2]:
        v = gv(co_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Capital Outlay 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[3]:
        v = gv(ce_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Committed Expenditure 2026-27 BE</span></div>""", unsafe_allow_html=True)

    st.markdown("---")
    tab_e1, tab_e2, tab_e3, tab_e4 = st.tabs(["📊 Expenditure Trend", "📌 Committed Expenditure", "💰 Subsidies & Transfers", "🏗️ Expenditure Breakdown"])

    with tab_e1:
        st.markdown('<div class="section-header">Total vs Net Expenditure — Year & Estimate Type</div>', unsafe_allow_html=True)
        comb_e = pd.concat([te_df.assign(Series="Total Expenditure"), ne_df.assign(Series="Net Expenditure")])
        comb_e = comb_e[comb_e["Unit"]=="Rs crore"].copy()
        if not comb_e.empty:
            fig = px.line(comb_e, x="Financial_Year", y="Value", color="Estimate_Type",
                          line_dash="Series", markers=True, color_discrete_map=COLOR_MAP,
                          title="Total & Net Expenditure (₹ crore)",
                          labels={"Value":"₹ crore","Financial_Year":"Financial Year","Estimate_Type":"Estimate Type"})
            fig.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("""<div class="info-box">
        <b>Difference between Total and Net Expenditure:</b> The gap = Debt Repayment (₹34,437 crore in 2026-27 BE).<br>
        <b>Why it matters:</b> Net Expenditure tells you how much was actually spent on government programmes vs repaying old loans.<br>
        <b>Note:</b> BE vs RE comparison for 2025-26 shows the RE (₹3,79,839 crore) was lower than BE (₹4,05,315 crore).
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">Revenue Expenditure vs Capital Outlay</div>', unsafe_allow_html=True)
        rev_cap = pd.concat([re_df.assign(Series="Revenue Expenditure"), co_df.assign(Series="Capital Outlay")])
        rev_cap = rev_cap[rev_cap["Unit"]=="Rs crore"].copy()
        if not rev_cap.empty:
            fig2 = px.bar(rev_cap, x="Financial_Year", y="Value", color="Series",
                          barmode="group", facet_col="Estimate_Type",
                          color_discrete_sequence=["#DC2626","#2563EB"],
                          title="Revenue Expenditure vs Capital Outlay (₹ crore)",
                          labels={"Value":"₹ crore"})
            fig2.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""<div class="info-box">
        Revenue Expenditure is consistently ~4× larger than Capital Outlay. Revenue Expenditure covers day-to-day operations.
        Capital Outlay creates infrastructure. A higher share of Capital Outlay can mean more investment in long-term assets.
        </div>""", unsafe_allow_html=True)

    with tab_e2:
        st.markdown('<div class="section-header">Committed Expenditure — Salaries, Pension & Interest</div>', unsafe_allow_html=True)
        sal_df = df[df["Indicator"]=="Salaries"].copy()
        pen_df = df[df["Indicator"]=="Pension"].copy()
        int_df = df[df["Indicator"]=="Interest Payment"].copy()
        sal_df["Component"] = "Salaries"
        pen_df["Component"] = "Pension"
        int_df["Component"] = "Interest Payment"
        committed_comb = pd.concat([sal_df, pen_df, int_df, ce_df.assign(Component="Total Committed")])
        committed_comb = committed_comb[committed_comb["Unit"]=="Rs crore"].copy()
        if not committed_comb.empty:
            fig3 = px.bar(committed_comb[committed_comb["Component"]!="Total Committed"],
                          x="Financial_Year", y="Value", color="Component",
                          barmode="stack", facet_col="Estimate_Type",
                          color_discrete_sequence=["#1D4ED8","#7C3AED","#DC2626"],
                          title="Committed Expenditure Components (₹ crore)",
                          labels={"Value":"₹ crore"})
            fig3.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig3, use_container_width=True)

        kc2 = st.columns(3)
        for col, ind, label, pct in zip(kc2,
            [sal_df, pen_df, int_df],
            ["Salaries 2026-27 BE","Pension 2026-27 BE","Interest 2026-27 BE"],
            ["24.5% of Revenue Receipts","9.2% of Revenue Receipts","10.9% of Revenue Receipts"]):
            v = gv(col if isinstance(col, pd.DataFrame) else ind,"2026-27","BE")
            # use ind, not col
        vals = [(gv(sal_df,"2026-27","BE"),"Salaries 2026-27 BE","24.5% of Revenue Receipts"),
                (gv(pen_df,"2026-27","BE"),"Pension 2026-27 BE","9.2% of Revenue Receipts"),
                (gv(int_df,"2026-27","BE"),"Interest 2026-27 BE","10.9% of Revenue Receipts")]
        for c2, (v2, lbl, pct) in zip(kc2, vals):
            with c2:
                st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v2) if v2 else 'N/A'}</span>
                <span class="kpi-label">{lbl}<br><small>{pct}</small></span></div>""", unsafe_allow_html=True)

        st.markdown("""<div class="info-box">
        <b>What is committed expenditure?</b> These are legally obligated payments. The government MUST pay them.<br>
        <b>2026-27 BE Total Committed = ₹1,37,826 crore = 45% of estimated revenue receipts.</b><br>
        <b>In 2024-25 Actuals it was 43%</b> — so committed expenditure is consuming a growing share of revenue.<br>
        <b>Important:</b> This does NOT automatically mean the budget is in trouble. But it limits flexibility for other spending.
        </div>""", unsafe_allow_html=True)

    with tab_e3:
        st.markdown('<div class="section-header">Subsidies & Transfers — 2018-19 Actuals vs 2025-26 BE</div>', unsafe_allow_html=True)
        sub_df = df[(df["Subcategory"]=="Subsidies and Transfers")&(df["Unit"]=="Rs crore")].copy()
        if not sub_df.empty:
            fig4 = px.bar(sub_df, x="Financial_Year", y="Value", color="Indicator",
                          barmode="group", color_discrete_sequence=px.colors.qualitative.Set2,
                          title="Subsidies & Transfers by Category (₹ crore)",
                          labels={"Value":"₹ crore","Indicator":"Category"})
            fig4.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("""<div class="info-box">
        <b>Total Subsidies & Transfers 2025-26 BE:</b> ₹69,407 crore = 4.1% of GSDP.<br>
        <b>All-states average:</b> ~2.7% of GSDP. MP's share is higher.<br>
        <b>Largest component — Power (Energy):</b> ₹25,142 crore (2025-26 BE).<br>
        <b>Cash Transfers (incl. Ladli Behna):</b> ₹20,821 crore (2025-26 BE).<br>
        <b>What this does NOT prove:</b> Whether subsidies are efficient or effective. This is spending data only.
        </div>""", unsafe_allow_html=True)

    with tab_e4:
        st.markdown('<div class="section-header">Expenditure Categories — 2026-27 BE Composition</div>', unsafe_allow_html=True)
        comp_dict = {
            "Revenue Expenditure": gv(re_df,"2026-27","BE"),
            "Capital Outlay": gv(co_df,"2026-27","BE"),
            "Loans & Advances": gv(df[df["Indicator"]=="Loans given by State"],"2026-27","BE"),
        }
        comp_dict = {k: v for k, v in comp_dict.items() if v is not None}
        if comp_dict:
            comp_df2 = pd.DataFrame(list(comp_dict.items()), columns=["Category","Value"])
            fig5 = px.pie(comp_df2, names="Category", values="Value",
                          title="Net Expenditure Composition — 2026-27 BE",
                          hole=0.35, color_discrete_sequence=["#DC2626","#2563EB","#D97706"])
            fig5.update_traces(texttemplate="%{label}<br>₹%{value:,.0f}", textposition="inside")
            fig5.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig5, use_container_width=True)
        st.markdown("""<div class="info-box">
        Revenue Expenditure dominates (~79%), reflecting ongoing commitments. Capital Outlay (~20%) represents
        infrastructure investment. Loans & Advances (~0.3%) are loans given by the state to entities.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 6 — BORROWINGS & DEBT
# ═══════════════════════════════════════════════════════════
elif page == PAGES[5]:
    st.markdown('<div class="main-title">🏦 Borrowings & Debt</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">How the government finances its deficit and manages accumulated debt.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-box">
    <b>Borrowings</b> = loans taken to fill the gap between receipts and expenditure.<br>
    <b>Central Capex Loans</b> = 50-year interest-free central government loans for capital works (excluded from borrowing ceiling).<br>
    <b>Debt Repayment</b> = principal repaid on earlier borrowings.<br>
    <b>Outstanding Liabilities</b> = total accumulated debt at year-end (borrowings + provident funds etc.).<br>
    <b>Fiscal Deficit</b> = the gap that borrowings are meant to fill.
    </div>""", unsafe_allow_html=True)

    bor_df = df[df["Indicator"]=="Borrowings"].copy()
    cc_df  = df[df["Indicator"]=="Central Capex Loans (50-yr interest-free)"].copy()
    dr_df  = df[df["Indicator"]=="Repayment of Debt"].copy()
    fd_df  = df[df["Indicator"]=="Fiscal Deficit"].copy()
    fd_pct = df[df["Indicator"]=="Fiscal Deficit as % of GSDP"].copy()
    ol_df  = df[df["Indicator"]=="Outstanding Liabilities as % of GSDP"].copy()
    fb_df  = df[df["Indicator"]=="Fiscal Balance as % of GSDP"].copy()

    kc = st.columns(4)
    def gv(dframe, fy, et):
        r = dframe[(dframe["Financial_Year"]==fy)&(dframe["Estimate_Type"]==et)]["Value"]
        return r.values[0] if len(r) > 0 else None

    with kc[0]:
        v = gv(bor_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Borrowings 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[1]:
        v = gv(cc_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Central Capex Loans 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[2]:
        v = gv(dr_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Debt Repayment 2026-27 BE</span></div>""", unsafe_allow_html=True)
    with kc[3]:
        v = gv(fd_df,"2026-27","BE")
        st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{fmt_crore(v) if v else 'N/A'}</span>
        <span class="kpi-label">Fiscal Deficit 2026-27 BE</span></div>""", unsafe_allow_html=True)

    st.markdown("---")
    tab_b1, tab_b2, tab_b3, tab_b4 = st.tabs(["📊 Borrowings Trend", "📉 Fiscal Deficit", "📈 Outstanding Liabilities", "🔄 Fiscal Balance History"])

    with tab_b1:
        st.markdown('<div class="section-header">Borrowings & Debt Repayment — Year Comparison</div>', unsafe_allow_html=True)
        bd_comb = pd.concat([bor_df.assign(Series="Borrowings"), cc_df.assign(Series="Central Capex Loans"), dr_df.assign(Series="Debt Repayment")])
        bd_comb = bd_comb[bd_comb["Unit"]=="Rs crore"].copy()
        if not bd_comb.empty:
            fig = px.bar(bd_comb, x="Financial_Year", y="Value", color="Series",
                         barmode="group", facet_col="Estimate_Type",
                         color_discrete_sequence=["#2563EB","#7C3AED","#DC2626"],
                         title="Borrowings, Central Capex Loans & Debt Repayment (₹ crore)",
                         labels={"Value":"₹ crore","Financial_Year":"Financial Year"})
            fig.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>Borrowings 2026-27 BE:</b> ₹1,06,190 crore. Includes ₹16,200 crore Central Capex Loans (interest-free, 50 years).<br>
        <b>Debt Repayment 2026-27 BE:</b> ₹34,437 crore — the government repays part of what it borrowed in earlier years.<br>
        <b>Central Capex Loans are special:</b> They are interest-free for 50 years and EXCLUDED from the normal state borrowing limit.
        </div>""", unsafe_allow_html=True)

    with tab_b2:
        st.markdown('<div class="section-header">Fiscal Deficit — Amount and % of GSDP</div>', unsafe_allow_html=True)
        if not fd_df.empty:
            fig2 = px.bar(fd_df[fd_df["Unit"]=="Rs crore"], x="Financial_Year", y="Value",
                          color="Estimate_Type", barmode="group",
                          color_discrete_map=COLOR_MAP,
                          title="Fiscal Deficit (₹ crore)",
                          labels={"Value":"₹ crore"})
            fig2.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig2, use_container_width=True)

        if not fd_pct.empty:
            fig3 = px.bar(fd_pct, x="Financial_Year", y="Value",
                          color="Estimate_Type", barmode="group",
                          color_discrete_map=COLOR_MAP,
                          title="Fiscal Deficit as % of GSDP",
                          labels={"Value":"% of GSDP"})
            fig3.add_hline(y=3.0, line_dash="dash", line_color="#DC2626",
                           annotation_text="16th FC Recommended Limit: 3%", annotation_position="top right")
            fig3.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""<div class="info-box">
        <b>2024-25 Actuals:</b> 4.3% of GSDP. <b>2025-26 RE:</b> 4.5%. <b>2026-27 BE:</b> 3.9%.<br>
        <b>16th Finance Commission recommended limit:</b> 3% of GSDP (starting 2026-27).<br>
        <b>What this does NOT prove:</b> Whether the deficit is sustainable. That requires analysis of debt trajectory,
        growth rates, and interest costs — which the dataset provides partially.
        </div>""", unsafe_allow_html=True)

    with tab_b3:
        st.markdown('<div class="section-header">Outstanding Liabilities as % of GSDP — Multi-Year Trend</div>', unsafe_allow_html=True)
        if not ol_df.empty:
            fig4 = px.line(ol_df.sort_values("Financial_Year"), x="Financial_Year", y="Value",
                           color="Estimate_Type", markers=True, color_discrete_map=COLOR_MAP,
                           title="Outstanding Liabilities as % of GSDP (Multi-Year)",
                           labels={"Value":"% of GSDP"})
            fig4.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig4, use_container_width=True)
            st.dataframe(ol_df[["Financial_Year","Estimate_Type","Value","Unit"]].reset_index(drop=True), use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>What this shows:</b> Accumulated debt as % of GSDP from 2020-21 to projections for 2028-29.<br>
        <b>2026-27 BE:</b> 32.5%. <b>Projected 2028-29:</b> 31.0% — suggesting a planned downward trajectory.<br>
        <b>Important:</b> Projections are plans, not guaranteed outcomes. Outstanding liabilities include borrowings
        AND public account liabilities (e.g. provident funds) — not just government loans.
        </div>""", unsafe_allow_html=True)

    with tab_b4:
        st.markdown('<div class="section-header">Fiscal Balance as % of GSDP — Historical Trend</div>', unsafe_allow_html=True)
        if not fb_df.empty:
            fig5 = px.line(fb_df.sort_values("Financial_Year"), x="Financial_Year", y="Value",
                           color="Estimate_Type", markers=True, color_discrete_map=COLOR_MAP,
                           title="Fiscal Balance as % of GSDP (negative = deficit)",
                           labels={"Value":"% of GSDP"})
            fig5.add_hline(y=0, line_color="#111111", line_width=1)
            fig5.add_hline(y=-3.0, line_dash="dash", line_color="#DC2626",
                           annotation_text="16th FC Limit: -3%")
            fig5.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig5, use_container_width=True)
        st.markdown("""<div class="info-box">
        <b>2020-21 Actuals:</b> -5.4% (COVID year). <b>2022-23 Actuals:</b> -3.1%. <b>2024-25 Actuals:</b> -4.3%.<br>
        <b>2026-27 BE target:</b> -3.9%. <b>Projected 2027-28 and 2028-29:</b> -3.0% (matching 16th FC limit).<br>
        <b>Remember:</b> Negative % = deficit. Near-zero or positive = surplus.
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="warn-box">
        <b>⚠️ What this dataset CANNOT tell us:</b> Whether the deficit level is "too high" or "acceptable" 
        requires comparing with growth rates, debt servicing capacity, and borrowing costs — 
        information not fully available in this dataset. These are signals to investigate, not automatic conclusions.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 7 — SECTOR ANALYSIS
# ═══════════════════════════════════════════════════════════
elif page == PAGES[6]:
    st.markdown('<div class="main-title">🏗️ Sector Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">How government expenditure is distributed across key sectors of MP\'s economy.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-box">
    <b>What is Sector Expenditure?</b> This shows how much the government spends on each area like Education, Health, Agriculture, Energy, etc.
    10 selected sectors together account for ~63-64% of total state expenditure.
    A blank Sector value = 'General / Total' (applies to the whole government, not a specific sector).
    </div>""", unsafe_allow_html=True)

    sec_exp = df[(df["Indicator_Category"]=="Sector Expenditure")&(df["Unit"]=="Rs crore")].copy()
    sec_pct = df[df["Indicator_Category"]=="Sector Expenditure % of Total"].copy()
    sectors_available = sorted(sec_exp["Sector"].replace("General / Total", pd.NA).dropna().unique().tolist())

    tab_s1, tab_s2, tab_s3 = st.tabs(["📊 Cross-Sector Comparison", "📈 Sector Trend", "📋 Sector Share %"])

    with tab_s1:
        st.markdown('<div class="section-header">Cross-Sector Expenditure — Selected Year & Estimate Type</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            sel_fy_s = st.selectbox("Financial Year:", [y for y in YEARS if y in sec_exp["Financial_Year"].unique()], index=2, key="sec_fy")
        with col2:
            sel_et_s = st.selectbox("Estimate Type:", [e for e in CORE_ET if e in sec_exp[sec_exp["Financial_Year"]==sel_fy_s]["Estimate_Type"].unique()], key="sec_et")

        filtered_s = sec_exp[(sec_exp["Financial_Year"]==sel_fy_s)&(sec_exp["Estimate_Type"]==sel_et_s)&
                              (sec_exp["Subcategory"]=="Sector")&(sec_exp["Sector"]!="General / Total")].copy()
        if not filtered_s.empty:
            fig_s1 = px.bar(filtered_s.sort_values("Value", ascending=True),
                            y="Sector", x="Value", orientation="h",
                            title=f"Sector Expenditure — {sel_fy_s} {sel_et_s} (₹ crore)",
                            color="Sector", color_discrete_map=SECTOR_COLORS,
                            labels={"Value":"₹ crore","Sector":"Sector"})
            fig_s1.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111",
                                  showlegend=False)
            fig_s1.update_traces(texttemplate="₹%{x:,.0f}", textposition="outside")
            st.plotly_chart(fig_s1, use_container_width=True)

            total_sel = filtered_s["Value"].sum()
            top_sector = filtered_s.loc[filtered_s["Value"].idxmax()]
            low_sector = filtered_s.loc[filtered_s["Value"].idxmin()]
            st.markdown(f"""<div class="info-box">
            <b>What this shows:</b> Government expenditure across {len(filtered_s)} sectors for {sel_fy_s} ({sel_et_s}).<br>
            <b>Largest sector:</b> {top_sector['Sector']} — ₹{top_sector['Value']:,.0f} crore ({top_sector['Value']/total_sel*100:.1f}% of shown sectors).<br>
            <b>Smallest shown sector:</b> {low_sector['Sector']} — ₹{low_sector['Value']:,.0f} crore.<br>
            <b>Sum of shown sectors:</b> ₹{total_sel:,.0f} crore.<br>
            <b>Note:</b> The dataset notes that 10 selected sectors together = ~63-64% of total state expenditure.
            </div>""", unsafe_allow_html=True)
        else:
            st.warning(f"No sector expenditure data for {sel_fy_s} {sel_et_s}.")

    with tab_s2:
        st.markdown('<div class="section-header">Individual Sector Expenditure Trend</div>', unsafe_allow_html=True)
        sel_sector = st.selectbox("Select Sector:", sectors_available, key="sec_trend_sector")
        sector_trend = sec_exp[(sec_exp["Sector"]==sel_sector)&(sec_exp["Subcategory"]=="Sector")].copy()

        if not sector_trend.empty:
            fig_s2 = px.line(sector_trend, x="Financial_Year", y="Value", color="Estimate_Type",
                             markers=True, color_discrete_map=COLOR_MAP,
                             title=f"{sel_sector} Sector Expenditure Trend (₹ crore)",
                             labels={"Value":"₹ crore","Financial_Year":"Financial Year"})
            fig_s2.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig_s2, use_container_width=True)

            # Dynamic explanation box
            act_rows = sector_trend[sector_trend["Estimate_Type"]=="Actuals"]
            be_rows  = sector_trend[sector_trend["Estimate_Type"]=="BE"]
            re_rows  = sector_trend[sector_trend["Estimate_Type"]=="RE"]
            max_row = sector_trend.loc[sector_trend["Value"].idxmax()] if not sector_trend.empty else None
            min_row = sector_trend.loc[sector_trend["Value"].idxmin()] if not sector_trend.empty else None

            explanation_parts = [f"<b>📊 Data-based observations for {sel_sector}:</b>"]
            if max_row is not None:
                explanation_parts.append(f"• Highest recorded value: ₹{max_row['Value']:,.0f} crore ({max_row['Financial_Year']} {max_row['Estimate_Type']})")
            if min_row is not None:
                explanation_parts.append(f"• Lowest recorded value: ₹{min_row['Value']:,.0f} crore ({min_row['Financial_Year']} {min_row['Estimate_Type']})")

            # Compare 2025-26 BE vs RE if both exist
            be_2526 = be_rows[be_rows["Financial_Year"]=="2025-26"]["Value"]
            re_2526 = re_rows[re_rows["Financial_Year"]=="2025-26"]["Value"]
            if len(be_2526) > 0 and len(re_2526) > 0:
                b, r = be_2526.values[0], re_2526.values[0]
                delta = (r - b) / b * 100
                direction = "higher" if r > b else "lower"
                explanation_parts.append(f"• 2025-26 RE (₹{r:,.0f} crore) was {abs(delta):.1f}% {direction} than 2025-26 BE (₹{b:,.0f} crore)")

            # Compare 2025-26 RE vs 2026-27 BE direction
            re_2526_v = re_rows[re_rows["Financial_Year"]=="2025-26"]["Value"]
            be_2627_v = be_rows[be_rows["Financial_Year"]=="2026-27"]["Value"]
            if len(re_2526_v) > 0 and len(be_2627_v) > 0:
                prev, nxt = re_2526_v.values[0], be_2627_v.values[0]
                chg = (nxt - prev) / prev * 100
                word = "increase" if nxt > prev else "decrease"
                explanation_parts.append(f"• 2026-27 BE shows a {abs(chg):.1f}% {word} over 2025-26 RE (₹{nxt:,.0f} cr vs ₹{prev:,.0f} cr)")

            if len(act_rows) > 0:
                act_latest = act_rows.sort_values("Financial_Year").iloc[-1]
                explanation_parts.append(f"• Most recent Actuals: ₹{act_latest['Value']:,.0f} crore ({act_latest['Financial_Year']})")

            explanation_parts.append("• Note: These are dataset observations. This dashboard does not draw conclusions about policy quality or outcomes.")
            st.markdown(f"""<div class="info-box">{"<br>".join(explanation_parts)}</div>""", unsafe_allow_html=True)

            st.dataframe(sector_trend[["Financial_Year","Estimate_Type","Value","Unit"]].reset_index(drop=True), use_container_width=True)
        else:
            st.info(f"No trend data found for {sel_sector}.")

    with tab_s3:
        st.markdown('<div class="section-header">Sector Share of Total Expenditure (%)</div>', unsafe_allow_html=True)
        if not sec_pct.empty:
            pct_filtered = sec_pct[sec_pct["Unit"]=="%"].copy()
            if not pct_filtered.empty:
                fig_s3 = px.bar(pct_filtered, x="Financial_Year", y="Value",
                                color="Indicator", barmode="group",
                                color_discrete_sequence=px.colors.qualitative.Set1,
                                title="Sector Share of Total Expenditure (%) by Year",
                                labels={"Value":"% of Total Expenditure"})
                fig_s3.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
                st.plotly_chart(fig_s3, use_container_width=True)
            st.dataframe(pct_filtered[["Indicator","Financial_Year","Estimate_Type","Value","Unit"]].reset_index(drop=True), use_container_width=True)

        st.markdown("""<div class="info-box">
        <b>What this shows:</b> Each sector's share of total state expenditure as a percentage.<br>
        <b>Education:</b> ~13-14% consistently. <b>Energy:</b> fell from 10.3% (2024-25 Actuals) to 8.2% (2026-27 BE).<br>
        <b>Rural Development:</b> jumped from 3.7% (2024-25 Actuals) to 6.1% (2026-27 BE).<br>
        <b>Important:</b> A falling % does not mean absolute spending fell. Total expenditure is growing, so % shares can shift.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 8 — YEAR & ESTIMATE COMPARISON
# ═══════════════════════════════════════════════════════════
elif page == PAGES[7]:
    st.markdown('<div class="main-title">🔄 Year & Estimate Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Compare any indicator across financial years and estimate types (Actuals, BE, RE).</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-box">
    <b>How to use:</b> Select an indicator and compare its values across years or between estimate types.
    Example: Compare 2025-26 BE vs 2025-26 RE to see how estimates changed mid-year.
    Only indicators with matching units will be compared — never mix % with ₹ crore.
    </div>""", unsafe_allow_html=True)

    money_indicators = sorted(df[df["Unit"]=="Rs crore"]["Indicator"].dropna().unique().tolist())
    pct_indicators   = sorted(df[df["Unit"]=="%"]["Indicator"].dropna().unique().tolist())

    tab_c1, tab_c2 = st.tabs(["💹 Monetary Indicators (₹ crore)", "📊 Percentage Indicators (%)"])

    with tab_c1:
        sel_ind_m = st.selectbox("Select Monetary Indicator:", money_indicators, key="cmp_money")
        ind_data_m = df[(df["Indicator"]==sel_ind_m)&(df["Unit"]=="Rs crore")].copy()
        if not ind_data_m.empty:
            fig_c1 = px.bar(ind_data_m, x="Financial_Year", y="Value", color="Estimate_Type",
                            barmode="group", color_discrete_map=COLOR_MAP,
                            title=f"{sel_ind_m} — Comparison by Year & Estimate Type",
                            labels={"Value":"₹ crore","Financial_Year":"Financial Year","Estimate_Type":"Estimate Type"})
            fig_c1.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside")
            fig_c1.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig_c1, use_container_width=True)
            disp_m = ind_data_m[["Financial_Year","Estimate_Type","Value","Unit"]].copy()
            disp_m["Formatted"] = disp_m.apply(lambda r: fmt_value(r["Value"], r["Unit"]), axis=1)
            st.dataframe(disp_m[["Financial_Year","Estimate_Type","Formatted","Unit"]].reset_index(drop=True), use_container_width=True)

            # Quick BE vs RE comparison
            fy_options = sorted(ind_data_m["Financial_Year"].unique().tolist())
            fy_sel = st.selectbox("Pick year for BE vs RE comparison:", [y for y in fy_options if
                                   "BE" in ind_data_m[ind_data_m["Financial_Year"]==y]["Estimate_Type"].values and
                                   "RE" in ind_data_m[ind_data_m["Financial_Year"]==y]["Estimate_Type"].values], key="be_re_fy")
            if fy_sel:
                be_v = ind_data_m[(ind_data_m["Financial_Year"]==fy_sel)&(ind_data_m["Estimate_Type"]=="BE")]["Value"]
                re_v = ind_data_m[(ind_data_m["Financial_Year"]==fy_sel)&(ind_data_m["Estimate_Type"]=="RE")]["Value"]
                if len(be_v) > 0 and len(re_v) > 0:
                    b, r = be_v.values[0], re_v.values[0]
                    diff = r - b
                    pct_diff = diff / b * 100
                    direction = "higher" if diff > 0 else "lower"
                    st.markdown(f"""<div class="info-box">
                    <b>{fy_sel} BE vs RE for {sel_ind_m}:</b><br>
                    BE = ₹{b:,.0f} crore · RE = ₹{r:,.0f} crore<br>
                    RE was <b>₹{abs(diff):,.0f} crore ({abs(pct_diff):.1f}%) {direction}</b> than BE.<br>
                    This means the revised estimate moved {direction} from the original budget plan.
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("No data for this indicator.")

    with tab_c2:
        sel_ind_p = st.selectbox("Select Percentage Indicator:", pct_indicators, key="cmp_pct")
        ind_data_p = df[(df["Indicator"]==sel_ind_p)&(df["Unit"]=="%")].copy()
        if not ind_data_p.empty:
            fig_c2 = px.line(ind_data_p.sort_values("Financial_Year"), x="Financial_Year", y="Value",
                             color="Estimate_Type", markers=True, color_discrete_map=COLOR_MAP,
                             title=f"{sel_ind_p} — Trend by Year & Estimate Type (%)",
                             labels={"Value":"%","Financial_Year":"Financial Year"})
            fig_c2.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
            st.plotly_chart(fig_c2, use_container_width=True)
            disp_p = ind_data_p[["Financial_Year","Estimate_Type","Value","Unit"]].copy()
            disp_p["Formatted"] = disp_p.apply(lambda r: fmt_value(r["Value"], r["Unit"]), axis=1)
            st.dataframe(disp_p[["Financial_Year","Estimate_Type","Formatted","Unit"]].reset_index(drop=True), use_container_width=True)
        else:
            st.info("No data for this indicator.")

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 9 — INDICATOR EXPLORER
# ═══════════════════════════════════════════════════════════
elif page == PAGES[8]:
    st.markdown('<div class="main-title">🔍 Indicator Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Explore any of the 114 indicators in the dataset — full context, chart, and statistics.</div>', unsafe_allow_html=True)

    INDICATOR_DEFINITIONS = {
        "GSDP (current prices)": "Total market value of all goods and services produced in MP in a year, measured at current market prices (includes inflation).",
        "GSDP Growth Rate (constant prices 2011-12)": "Percentage change in GSDP measured at constant 2011-12 prices — removes inflation to show 'real' economic growth.",
        "Per Capita GSDP (current prices)": "GSDP divided by the state's population. A rough average of economic output per person. Does NOT show income distribution.",
        "India GDP Growth Rate (constant prices)": "India's national GDP growth rate at constant prices — provided as a reference benchmark for MP's growth rate.",
        "India Per Capita GDP (current prices)": "India's national per capita GDP — provided as a reference benchmark for MP's per capita GSDP.",
        "Total Expenditure": "All government spending including debt repayment. The broadest measure of government expenditure.",
        "Net Expenditure (excl. debt repayment)": "Total Expenditure minus Debt Repayment. Shows how much was spent on programmes vs repaying loans.",
        "Revenue Expenditure": "Day-to-day operating costs: salaries, pensions, interest payments, grants, subsidies. Does not create long-term assets.",
        "Capital Outlay": "Spending on physical assets: roads, dams, government buildings, equipment. Creates long-term infrastructure.",
        "Total Receipts": "All resources coming to the government including borrowings, taxes, grants, and other receipts.",
        "Net Receipts (excl. borrowings)": "Total Receipts minus Borrowings. Shows government's own resource mobilisation excluding debt.",
        "Revenue Receipts": "Recurring government income: own taxes + central devolution + central grants. Does not include borrowings.",
        "Borrowings": "Total loans taken by the state government to finance its deficit. Adds to outstanding liabilities.",
        "Central Capex Loans (50-yr interest-free)": "50-year interest-free loans from the central government for capital expenditure. Excluded from state's normal borrowing ceiling.",
        "Repayment of Debt": "Principal amount repaid on earlier borrowings during the year. Not the same as interest payments.",
        "Fiscal Deficit": "Total Expenditure minus Total Non-Borrowing Receipts. The gap filled by borrowing.",
        "Fiscal Deficit as % of GSDP": "Fiscal Deficit expressed as a share of GSDP. Key measure of fiscal sustainability.",
        "Revenue Surplus": "Revenue Receipts minus Revenue Expenditure. Positive = day-to-day income exceeds day-to-day spending.",
        "Primary Deficit": "Fiscal Deficit minus Interest Payments. Shows deficit before interest burden is accounted for.",
        "Salaries": "Payments to government employees. A major component of committed expenditure.",
        "Pension": "Payments to retired government employees. A committed, legally obligated expense.",
        "Interest Payment": "Interest paid on accumulated government borrowings. Rises as outstanding debt grows.",
        "Total Committed Expenditure": "Sum of Salaries + Pension + Interest Payments. Cannot easily be reduced; legally obligated.",
        "Outstanding Liabilities as % of GSDP": "Accumulated total debt as a % of GSDP. Measures the state's debt burden relative to its economy.",
        "State's Own Tax Revenue": "Taxes collected directly by the state: SGST, Sales Tax, State Excise, Stamp Duty, Vehicle Tax, etc.",
        "Share in Central Taxes (Devolution)": "MP's constitutionally guaranteed share of centrally collected taxes, distributed by the Finance Commission.",
        "Grants-in-aid from Centre": "Grants given by the central government to MP for various purposes including centrally sponsored schemes.",
    }

    sel_indicator = st.selectbox("Select Indicator:", INDICATORS, key="ind_explorer")
    ind_df = df[df["Indicator"]==sel_indicator].copy()

    if not ind_df.empty:
        cat = ind_df["Indicator_Category"].iloc[0]
        subcat = ind_df["Subcategory"].iloc[0]
        units_avail = ind_df["Unit"].dropna().unique().tolist()
        years_avail = sorted(ind_df["Financial_Year"].dropna().unique().tolist())
        et_avail    = sorted(ind_df["Estimate_Type"].dropna().unique().tolist())
        sectors_avail = sorted(ind_df["Sector"].replace("General / Total",pd.NA).dropna().unique().tolist())

        definition = INDICATOR_DEFINITIONS.get(sel_indicator,
            f"This indicator belongs to the '{cat}' category, subcategory '{subcat}'. "
            f"It measures aspects of {'government finances' if cat in ['Expenditure','Receipts','Borrowings','Fiscal Position','Committed Expenditure','Debt Repayment'] else 'the state economy'}. "
            "Refer to the dataset notes column for source information.")

        col_meta, col_kpi = st.columns([2,1])
        with col_meta:
            st.markdown(f"""<div class="concept-card">
            <b style="font-size:1.1rem;color:#1D4ED8;">{sel_indicator}</b><br><br>
            <b>Category:</b> {cat} &nbsp;|&nbsp; <b>Subcategory:</b> {subcat}<br><br>
            <b>What this indicator means:</b><br>{definition}<br><br>
            <b>Years available:</b> {', '.join(years_avail)}<br>
            <b>Estimate types:</b> {', '.join(et_avail)}<br>
            <b>Units:</b> {', '.join(units_avail)}<br>
            <b>Sectors:</b> {', '.join(sectors_avail) if sectors_avail else 'General / Total (whole-government indicator)'}
            </div>""", unsafe_allow_html=True)
        with col_kpi:
            n_obs = len(ind_df)
            st.markdown(f"""<div class="kpi-card"><span class="kpi-value">{n_obs}</span><span class="kpi-label">Observations</span></div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for unit_group in units_avail:
                unit_sub = ind_df[ind_df["Unit"]==unit_group]["Value"].dropna()
                if len(unit_sub) > 0 and unit_group != "%":
                    st.markdown(f"""<div class="kpi-card" style="margin-top:0.5rem;">
                    <span class="kpi-value" style="font-size:1.2rem;">{fmt_value(unit_sub.max(), unit_group)}</span>
                    <span class="kpi-label">Max ({unit_group})</span></div>""", unsafe_allow_html=True)

        st.markdown("---")
        # Chart — per unit group
        for unit_group in units_avail:
            unit_sub = ind_df[ind_df["Unit"]==unit_group].copy()
            if unit_sub.empty: continue
            st.markdown(f'<div class="section-header">Chart — {unit_group}</div>', unsafe_allow_html=True)
            if len(unit_sub) >= 2:
                fig_ie = px.bar(unit_sub, x="Financial_Year", y="Value",
                                color="Estimate_Type", barmode="group",
                                color_discrete_map=COLOR_MAP,
                                title=f"{sel_indicator} ({unit_group})",
                                labels={"Value":unit_group,"Financial_Year":"Financial Year","Estimate_Type":"Estimate Type"})
                if unit_group == "Rs crore":
                    fig_ie.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside")
                elif unit_group == "%":
                    fig_ie.update_traces(texttemplate="%{y:.4g}%", textposition="outside")
                fig_ie.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#111111")
                st.plotly_chart(fig_ie, use_container_width=True)

        # Data table — no Notes column
        st.markdown('<div class="section-header">Data Table</div>', unsafe_allow_html=True)
        show_cols = ["Financial_Year","Estimate_Type","Value","Unit","Sector"]
        show_cols = [c for c in show_cols if c in unit_sub.columns]
        disp_ie = ind_df[show_cols].copy()
        disp_ie.insert(2, "Formatted Value", disp_ie.apply(lambda r: fmt_value(r["Value"],r["Unit"]), axis=1))
        final_cols = ["Financial_Year","Estimate_Type","Formatted Value","Unit","Sector"]
        st.dataframe(disp_ie[[c for c in final_cols if c in disp_ie.columns]].reset_index(drop=True), use_container_width=True)

        # Statistics — per unit group
        st.markdown('<div class="section-header">Statistics (grouped by Unit — never mixing units)</div>', unsafe_allow_html=True)
        for unit_group in units_avail:
            unit_sub2 = ind_df[(ind_df["Unit"]==unit_group)&(ind_df["Value"].notna())]["Value"]
            if len(unit_sub2) == 0: continue
            if unit_group == "%":
                st.warning(f"⚠️ Unit = %. Mean/sum of percentages shown below are only meaningful if all values measure the same thing. Interpret with caution.")
            sc = st.columns(5)
            stats = [
                ("Count", f"{len(unit_sub2)}"),
                ("Min", fmt_value(unit_sub2.min(), unit_group)),
                ("Mean", fmt_value(unit_sub2.mean(), unit_group)),
                ("Median", fmt_value(unit_sub2.median(), unit_group)),
                ("Max", fmt_value(unit_sub2.max(), unit_group)),
            ]
            for col, (lbl, val) in zip(sc, stats):
                with col:
                    st.metric(lbl, val)
    else:
        st.warning("No data found for this indicator.")

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 10 — INSIGHTS & DECISION SUPPORT
# ═══════════════════════════════════════════════════════════
elif page == PAGES[9]:
    st.markdown('<div class="main-title">💡 Insights & Decision Support</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Data-based observations from the dataset — what the numbers show and what they cannot prove.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="warn-box">
    <b>Important:</b> The observations below are derived directly from the dataset values. This dashboard does NOT:
    make political recommendations, claim causation, or evaluate government performance.
    Every observation is traceable to a specific data point.
    </div>""", unsafe_allow_html=True)

    tab_i1, tab_i2, tab_i3 = st.tabs(["📊 Key Observations", "⚠️ Data Limitations", "📖 What This Data Can & Cannot Tell Us"])

    with tab_i1:
        st.markdown('<div class="section-header">Data-Based Observations from the Dataset</div>', unsafe_allow_html=True)

        observations = [
            ("🏭 Economy",
             "GSDP at current prices grew from ₹15,02,428 crore (2024-25 Actuals) to a 2026-27 BE of ₹18,48,274 crore. "
             "The 2025-26 RE (₹16,69,750 crore) was ₹24,727 crore lower than the 2025-26 BE (₹16,94,477 crore). "
             "MP's real GSDP growth in 2024-25 was 6% at constant prices vs India's 6.5%.",
             "GSDP, Per Capita GSDP, GSDP Growth Rate"),
            ("💰 Receipts",
             "Total Receipts 2026-27 BE = ₹4,23,655 crore. 46% from own resources, 54% from central transfers. "
             "Own Tax Revenue 2026-27 BE = ₹1,17,667 crore (6.4% of GSDP). SGST is the largest own tax source (₹42,311 crore, 36% share). "
             "Grants from Centre grew from ₹32,678 crore (2024-25 Actuals) to ₹54,505 crore (2026-27 BE).",
             "Total Receipts, Revenue Receipts, Own Tax Revenue, Grants-in-aid"),
            ("💸 Expenditure",
             "Total Expenditure 2026-27 BE = ₹4,23,360 crore. Net Expenditure (excl. debt repayment) = ₹3,88,923 crore. "
             "For 2025-26, the RE (₹3,79,839 crore) was ₹25,476 crore lower than the BE (₹4,05,315 crore). "
             "Capital Outlay 2026-27 BE = ₹78,920 crore (8% increase over 2025-26 RE).",
             "Total Expenditure, Net Expenditure, Capital Outlay"),
            ("📌 Committed Expenditure",
             "Committed Expenditure (Salaries + Pensions + Interest) rose from 43% of revenue receipts (2024-25 Actuals) "
             "to a budgeted 45% (2026-27 BE). Interest Payments alone = ₹33,735 crore (10.9% of revenue receipts) in 2026-27 BE.",
             "Salaries, Pension, Interest Payment, Total Committed Expenditure"),
            ("🏦 Borrowings & Deficit",
             "Borrowings 2026-27 BE = ₹1,06,190 crore, lower than 2025-26 BE (₹1,08,751 crore). "
             "Fiscal Deficit as % of GSDP: 4.3% (2024-25 Actuals) → 4.5% (2025-26 RE) → 3.9% (2026-27 BE). "
             "The 16th Finance Commission recommends an annual limit of 3% of GSDP from 2026-27.",
             "Borrowings, Fiscal Deficit, Outstanding Liabilities"),
            ("🏗️ Sectors",
             "Education is consistently the largest sector (₹52,917 crore, 13.7% of total expenditure in 2026-27 BE). "
             "Rural Development showed the largest % jump: from 3.7% share (2024-25 Actuals) to 6.1% (2026-27 BE). "
             "Energy sector expenditure fell from ₹34,130 crore (2025-26 BE) to ₹31,843 crore (2026-27 BE). "
             "Social Welfare 2026-27 BE = ₹40,400 crore (includes Ladli Behna Yojana ₹23,883 crore).",
             "Sector Expenditure (Education, Health, Agriculture, Energy, etc.)"),
            ("💰 Subsidies",
             "Total Subsidies & Transfers 2025-26 BE = ₹69,407 crore = 4.1% of GSDP, higher than the all-states average of ~2.7% of GSDP. "
             "Power subsidies = ₹25,142 crore (largest component). Cash Transfers = ₹20,821 crore. "
             "In 2018-19 Actuals, total subsidies were ₹26,825 crore = 3.23% of GSDP.",
             "Subsidies and Transfers (Power, Cash Transfers, Agriculture, Social Security)"),
            ("📈 Outstanding Liabilities",
             "Outstanding Liabilities as % of GSDP: 27.5% (2022-23) → 30% (2023-24) → 31.2% (2024-25) → 32.5% (2026-27 BE). "
             "Projections show this is expected to decline to 31% by 2028-29 per the dataset.",
             "Outstanding Liabilities as % of GSDP"),
        ]

        for icon_label, obs_text, indicators_cited in observations:
            with st.expander(f"📌 {icon_label}"):
                st.markdown(f"""<div class="concept-card">{obs_text}<br><br>
                <small><b>Source indicators:</b> {indicators_cited}</small></div>""", unsafe_allow_html=True)

    with tab_i2:
        st.markdown('<div class="section-header">⚠️ Data Limitations & Quality Notes</div>', unsafe_allow_html=True)
        limitations = [
            ("Missing multi-year GSDP growth data",
             "GSDP Growth Rate is available only for 2024-25 (Actuals). A single data point cannot establish a trend."),
            ("Sectoral GSDP share — one year only",
             "Agriculture/Manufacturing/Services shares of GSDP are only available for 2024-25 Actuals. Historical comparison is not possible from this dataset."),
            ("Subsidies data gap",
             "Subsidies & Transfers data has only 2018-19 Actuals and 2025-26 BE — the years in between are not in the dataset."),
            ("2024-25 BE figures (Table 8)",
             "Some 2024-25 BE figures appear in the dataset (rows 276–318). These represent original plans for 2024-25, for which Actuals are also available, enabling a BE vs Actuals comparison."),
            ("SPSE data",
             "SPSE (State Public Sector Enterprise) data is only for 2022-23 and covers only 12 of 32 SPSEs that had finalised accounts."),
            ("Government Guarantees — mid-year figure",
             "Outstanding Government Guarantees is shown as of 31 Dec 2025 (mid-year), not end-of-year. Not directly comparable to annual figures."),
            ("Finance Commission data — periods not years",
             "Finance Commission indicators use period labels (2015-20, 2021-26, 2026-31) rather than annual years. These cannot be plotted on a standard annual timeline."),
            ("Projections vs Actuals",
             "Fiscal Balance and Outstanding Liabilities include Projections for 2027-28 and 2028-29. These are planned targets, not confirmed outcomes."),
        ]
        for title, desc in limitations:
            st.markdown(f"""<div class="concept-card">
            <b>⚠️ {title}</b><br>{desc}
            </div>""", unsafe_allow_html=True)

    with tab_i3:
        st.markdown('<div class="section-header">What This Dataset CAN Help Us Understand</div>', unsafe_allow_html=True)
        can_do = [
            "The size of MP's economy (GSDP) in 2024-25 and projected values for 2025-26 and 2026-27.",
            "How MP's real GDP growth (6%) compared to India's (6.5%) in 2024-25.",
            "The composition of MP's economy: Agriculture 44%, Services 37%, Manufacturing 19% (2024-25 Actuals).",
            "How government receipts are structured: 46% own resources, 54% from centre (2026-27 BE).",
            "The breakdown of government expenditure: Revenue vs Capital, Committed vs Discretionary.",
            "How fiscal deficit has changed: 4.3% (2024-25 Actuals) vs 3.9% (2026-27 BE).",
            "How accumulated debt compares to the economy (Outstanding Liabilities as % of GSDP).",
            "Differences between original Budget Estimates and Revised Estimates.",
            "Which sectors received the most government expenditure and how this changed.",
            "Which tax heads contribute most to own revenue (SGST is largest at 36% share).",
            "How committed expenditure (Salaries+Pensions+Interest) has grown as a % of revenue.",
        ]
        for item in can_do:
            st.markdown(f"✅ {item}")

        st.markdown("---")
        st.markdown('<div class="section-header">What This Dataset CANNOT Prove</div>', unsafe_allow_html=True)
        cannot_do = [
            "Whether higher expenditure in a sector leads to better outcomes (e.g. more health spending ≠ better health automatically).",
            "Whether the fiscal deficit is 'too high' or 'acceptable' — this requires comparing with economic growth, interest rates, and borrowing costs not fully available here.",
            "Whether GSDP growth was evenly distributed across the population — per capita GSDP is an average, not a distributional measure.",
            "Why a specific number increased or decreased — the dataset records what happened, not why.",
            "Whether any specific government policy caused an observed change — correlation is not causation.",
            "How MP compares to other states — this dataset contains only MP data (with India GDP/per capita as reference only).",
            "Whether borrowing levels are sustainable long-term — sustainability analysis requires interest rate data and growth projections beyond this dataset.",
            "Whether government employees are over- or under-paid — salary data shows totals, not individual or sector-level pay.",
            "Whether subsidies reached their intended beneficiaries — this dataset shows expenditure amounts, not delivery outcomes.",
            "The quality or efficiency of government spending in any sector.",
        ]
        for item in cannot_do:
            st.markdown(f"❌ {item}")

    st.markdown('<div class="footer">Made with IBM Bob</div>', unsafe_allow_html=True)

