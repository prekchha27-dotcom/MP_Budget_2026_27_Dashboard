# Madhya Pradesh Budget 2026-27
# Interactive Economic & Fiscal Data Analytics Dashboard

---

## Project Overview

This project is a comprehensive, beginner-friendly interactive data analytics dashboard built with **Python + Streamlit**. It transforms the Madhya Pradesh State Budget 2026-27 dataset into an understandable, explorable, and educational experience for anyone — even without an economics background.

The dashboard takes you on a journey:

> **DATA → UNDERSTANDING → EXPLORATION → COMPARISON → INTERPRETATION**

Every number is shown with its unit. Every term is explained in plain language. Every chart is accompanied by context about what it shows, why it matters, and what it cannot prove.

---

## Problem Statement

Government budget documents are packed with numbers, indicators, and financial jargon that most people find impenetrable. Key questions like "What does GSDP mean?", "Is this number big or small?", "What is the difference between BE and RE?", and "How does this compare to last year?" remain unanswered for ordinary citizens.

This dashboard bridges that gap.

---

## Project Objective

To build a professional data analytics project that:
- Helps a complete beginner understand the MP Budget 2026-27
- Explains every indicator, unit, and estimate type in plain language
- Allows exploration, comparison, and trend analysis
- Never presents misleading aggregations (no mixing of units)
- Distinguishes clearly between Actuals, BE, and RE
- Provides data-based observations without political conclusions

---

## Dataset Description

| Property | Value |
|----------|-------|
| File | `MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv.xlsx` |
| Total Rows | 341 (excluding header) |
| Columns | 9 |
| Unique Indicators | 114 |
| Indicator Categories | 13 |
| Financial Years | 13 (including Finance Commission award periods) |
| Core Budget Years | 2024-25, 2025-26, 2026-27 |
| Estimate Types | Actuals, BE, RE, Projection, Award Period variants |
| Units | Rs crore, Rs (per capita), % |
| Sectors | 14 distinct sectors |
| Missing Values | None in Value column |

**Dataset Link:**  
[https://docs.google.com/spreadsheets/d/1vyzAQFhvVSAe6s75RVeM6ke-DlQ8ntzh/edit?usp=sharing&ouid=114347354897789822870&rtpof=true&sd=true](https://docs.google.com/spreadsheets/d/1vyzAQFhvVSAe6s75RVeM6ke-DlQ8ntzh/edit?usp=sharing&ouid=114347354897789822870&rtpof=true&sd=true)

**Source:** PRS Legislative Research — Madhya Pradesh Budget Analysis, presented on 18 February 2026.

---

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3.8+ | Core programming language |
| Streamlit | Interactive web dashboard |
| Pandas | Data loading, cleaning, manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive charts and visualisations |
| openpyxl | Reading .xlsx files |

---

## Project Structure

```
Budget_Analysis_2026-27_Madhya_Pradesh/
│
├── app.py                                          ← Single Streamlit application (ALL code here)
├── requirements.txt                                ← Python dependencies
├── README.md                                       ← This file
├── MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv.xlsx  ← Primary dataset
├── MP_Budget_2026_27_CSV_Terminology_Guide.docx    ← Terminology reference document
└── MP_Budget_2026_27_Project_Report.docx           ← Detailed project report
```

---

## Installation Instructions

### Step 1: Install Python

Download Python 3.8 or later from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Navigate to the project folder
cd path/to/Budget_Analysis_2026-27_Madhya_Pradesh

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — web dashboard framework
- `pandas` — data manipulation
- `numpy` — numerical operations
- `plotly` — interactive charts
- `openpyxl` — Excel file reading

### Step 4: Place the Dataset

Ensure the dataset file is in the same folder as `app.py`:

```
MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv.xlsx
```

The app also supports a CSV version named `MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv`.

### Step 5: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## Dashboard Features

### 10 Dashboard Sections (in navigation order):

| # | Section | Description |
|---|---------|-------------|
| 1 | 🏠 Home — Understand MP Budget | Beginner-friendly introduction with concept cards for GSDP, Receipts, Expenditure, Borrowings, Debt Repayment, and Fiscal Deficit. Explains Actuals / BE / RE and financial years in plain language. |
| 2 | 📚 Data Dictionary / Learn | **First stop for terminology.** Four tabs: (1) 💬 Ask a Question — keyword-matching chatbot covering 30 budget terms; (2) 📖 Column Guide — every dataset column explained; (3) 📘 Economic Terms A–Z — 14 major terms with examples; (4) 🔍 How to Read a Row — real dataset rows translated to plain English. |
| 3 | 📈 Economy — GSDP | GSDP trend (current prices), real growth rate, per capita comparison (MP vs India), sectoral share of GSDP. |
| 4 | 💰 Income & Receipts | Total and Net Receipts, Revenue Receipts, own tax revenue breakdown, central devolution & grants, revenue structure composition chart. |
| 5 | 💸 Expenditure | Total vs Net Expenditure, Revenue vs Capital Outlay, Committed Expenditure (Salaries + Pension + Interest), Subsidies & Transfers. |
| 6 | 🏦 Borrowings & Debt | Borrowings, Central Capex Loans, Debt Repayment, Fiscal Deficit (amount and % of GSDP), Outstanding Liabilities trend, Fiscal Balance history. |
| 7 | 🏗️ Sector Analysis | Cross-sector expenditure comparison, individual sector trend with **dynamic data-driven explanation box** below each line chart, sector share (%) of total expenditure. |
| 8 | 🔄 Year & Estimate Comparison | Interactive comparison of any indicator across years; automatic BE vs RE delta with % change calculation. |
| 9 | 🔍 Indicator Explorer | Full profile for any of 114 indicators: plain-language definition, category, available years/estimate types/sectors, value table (no Notes column), trend chart, statistics grouped by unit. |
| 10 | 💡 Insights & Decision Support | Data-based observations per category; data limitations; explicit list of what the dataset can and cannot prove. |

---

## Key Design Decisions

- **Data Dictionary at position 2** (immediately after Home) so beginners can learn terminology before exploring data
- **Terminology chatbot** in Data Dictionary — keyword-matching, covers 30 budget and economics terms
- **Dynamic explanation boxes** in Sector Analysis — auto-generated observations below each line chart (min, max, BE vs RE delta, direction change)
- **No Statistical Summary section** — removed to reduce complexity for non-economics users
- **Indicator Explorer table** shows `Financial_Year, Estimate_Type, Formatted Value, Unit, Sector` — no raw Notes column
- **Light theme** enforced via `.streamlit/config.toml` and inline CSS for full readability
- **Single-file architecture** — all frontend and backend in `app.py`; no separate modules

## Analytical Methods

- **Year-over-year comparison** with Actuals, BE, RE
- **BE vs RE delta analysis** — shows % change between original and revised estimates
- **Sectoral composition analysis** — horizontal bar charts by year and estimate type
- **Trend analysis** — line and bar charts across financial years
- **Fiscal ratio analysis** — all ratios computed from same-unit values only
- **Revenue composition analysis** — own resources vs central transfers

---

## Important Data Limitations

1. **BE and RE are not actual spending.** Only Actuals represent what truly happened.
2. **Units must never be mixed.** Rs crore and % values cannot be compared directly.
3. **GSDP is not government revenue.** It is the output of the entire economy.
4. **Per capita GSDP is a mathematical average**, not a reflection of every person's income.
5. **Blank Sector values are not missing data.** They represent whole-government figures.
6. **This dataset cannot tell us why numbers changed** — only what changed.
7. **Financial year projections (2027-28, 2028-29)** come from Medium Term Fiscal Policy documents — not actual figures.

---

## How to Interpret Actuals / BE / RE

| Type | What It Means | When Available |
|------|--------------|----------------|
| **Actuals** | Real, final recorded figure after year ends | For completed years (e.g., 2024-25) |
| **BE (Budget Estimate)** | Original plan presented when budget is announced | For current and future years |
| **RE (Revised Estimate)** | Updated estimate made mid-year | For current year (e.g., 2025-26) |

**Key comparisons:**
- **BE vs RE (same year):** Shows how plans changed during the year
- **RE vs next year's BE:** Shows how the new year's plan relates to the current revised estimate
- **BE vs Actuals (same year):** Shows forecast accuracy

---

## How to Interpret Units

| Unit | Meaning | Example |
|------|---------|---------|
| `Rs crore` | Rupees in crores (1 crore = 10 million) | 1502428 Rs crore = ₹15,02,428 crore |
| `Rs` | Rupees (used for per capita figures) | 170430 Rs = ₹1,70,430 per person |
| `%` | Percentage | 6 % = 6 percent (e.g., growth rate) |

---

## How to Avoid Misleading Comparisons

1. **Never average Rs crore values with % values.**
2. **Never sum percentages** unless they are component shares that add to 100%.
3. **Always check Estimate_Type** before comparing two values — compare Actuals to Actuals, BE to BE.
4. **Do not compare indicators across different sectors** unless they share the same unit and logical basis.
5. **Blank Sector ≠ missing data.** These rows represent whole-government or cross-sector totals.

---

## Future Improvements

- Add historical data beyond 2020-21 for longer trend analysis
- Add state-to-state comparison panel (requires additional datasets)
- Add inflation-adjusted expenditure comparisons
- Add PDF download of filtered tables and charts
- Add mobile-optimised layout
- Add population data for per capita expenditure calculations

---

*Source: PRS Legislative Research | MP Budget 2026-27 | Data presented: 18 February 2026*
