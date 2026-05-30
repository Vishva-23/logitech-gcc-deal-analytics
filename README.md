# 📊 Logitech B2B Deal Analytics — GCC Dashboard

> **Final-round data analytics assignment** built for Logitech's Global Customer Collaboration (GCC) team internship.  
> A complete end-to-end pipeline: raw data → Python prep → Tableau dashboard → strategic insights.

---

## 🖥️ Dashboard Preview

### Page 1 — Performance Overview
![Dashboard Page 1](assets/dashboard_page1.png)

### Page 2 — Strategic Intelligence & Risk Register
![Dashboard Page 2](assets/dashboard_page2.png)

---

## 🎯 Project Overview

| Detail | Value |
|---|---|
| **Dataset** | Logitech B2B deal data — 449,262 rows × 27 columns |
| **Scope** | FY2024–Q3 to FY2029, 4 global sales regions |
| **Tools** | Python 3.12 · pandas · numpy · Tableau Desktop |
| **Output** | Two-page interactive Tableau dashboard |
| **Context** | Final-round internship assignment — Global Customer Collaboration team |

---

## 📁 Repository Structure

```
logitech-gcc-deal-analytics/
│
├── README.md
│
├── data/
│   ├── sample_dataset_anonymised.csv   ← 500-row anonymised sample (same schema as real data)
│   ├── EOL_SKUs_Reference.xlsx         ← 14 officially discontinued product SKUs
│   └── data_dictionary.md              ← Column definitions and methodology notes
│
├── analysis/
│   ├── data_prep_pipeline.py           ← Full Python cleaning + enrichment script
│   └── analysis_summary.xlsx          ← 7-tab Excel output (summary tables per question)
│
├── dashboard/
│   ├── Logitech_GCC_Analytics.twbx    ← Tableau packaged workbook (open in Tableau Desktop/Reader)
│   ├── dashboard_page1.pdf            ← Page 1 — Performance Overview
│   └── dashboard_page2.pdf            ← Page 2 — Strategic Intelligence
│
├── presentation/
│   └── Logitech_Dashboard_Slide.pptx  ← Glassmorphism executive summary slide
│
└── assets/
    ├── dashboard_page1.png            ← Preview image for README
    └── dashboard_page2.png            ← Preview image for README
```

---

## 🔧 Data Preparation — Methodology

The raw dataset required three derived columns (as specified in the assignment brief):

### Column Y — Account Type
```python
Account Type = "Global Strategic Customer"
    IF Company Segmentation = "Global" AND Company Designation = "Strategic"
ELSE "Local Customer"
```
> **Rationale:** The dataset filter header states *"Strategic Group Owner not equal to blank"* — both conditions together identify formally assigned strategic accounts. This produced 208 unique Global Strategic companies (82,638 rows).

### Column Z — Fiscal Year & Column AA — Fiscal Quarter
```python
FY = Fiscal Period.split("-")[0]   # e.g. "2024-Q3" → "2024"
FQ = Fiscal Period.split("-")[1]   # e.g. "2024-Q3" → "Q3"
```
> ⚠️ **Important:** Logitech's fiscal year runs **April → March** (not January → December). FY2026 = April 2025 to March 2026. FY/FQ were extracted from the existing `Fiscal Period` column — **not** derived from `Close Date` — to avoid calendar-year errors.

### Bonus — EOL Product Flag
```python
Is_EOL_Product = Product Number IN [EOL SKUs reference sheet]
```
> Cross-referenced every row's Product Number against the 14 officially discontinued SKUs in the `EOL SKUs` tab. Used for the pipeline risk analysis.

### Data Quality
| Issue | Count | Action |
|---|---|---|
| ERROR rows | 12 | Removed |
| Fully null rows | 3 | Removed |
| "Total" summary row | 1 | Removed |
| Missing Life Cycle Status | ~8,500 (1.9%) | Kept (revenue still valid) |
| Missing Company Name | ~1,325 (0.3%) | Kept (product/deal data still valid) |

---

## 📈 Key Findings

### 1. 🏆 Top 10 Global Strategic Accounts
- **Nexus Industries** leads at **$68.2M** — more than double the #2 account
- Top 10 GSC accounts represent a disproportionate share of total GSC revenue
- **Strategic implication:** Revenue is highly concentrated — losing 2-3 top relationships would have immediate impact

### 2. 📦 Top Performing Product Group
- **Video Collaboration Group** dominates at **$2.02B (52.6% of total revenue)**
- Every other product group sits below the dataset average
- **Strategic implication:** Post-COVID hybrid work drove massive conference room investment — a structural, not cyclical, trend

### 3. 📈 GSC Revenue Trend
- Growth trajectory: **$102M (FY24) → $203M (FY25) → $231M (FY26)** — nearly doubling in 2 years
- Apparent cliff after FY2027-Q1 is a **pipeline visibility window, not a business decline** — future deals haven't been booked yet

### 4. 🏅 Top Closed Won Deals by Calendar Year
- **Nexus Industries** appears in all 4 years, growing from $3.8M → $27.4M (7× in 2 years)
- Single largest deal: **Vector Diamond Marine — $7.6M** (2025)
- **Pattern:** Strategic accounts show compounding YoY growth; local accounts show one-time spike buying

---

## 🚨 EOL Risk Finding (Unrequested — Proactive Analysis)

> **20 future deals across 20 companies are committing to End-of-Life products.**  
> **Total revenue at risk: $199,318 USD**

| Rank | Company | Region | EOL Product | Close Year | USD at Risk |
|---|---|---|---|---|---|
| 1 | Champion455 Enterprises | EAD | Logitech ConferenceCam Connect | 2027 | $78,343 |
| 2 | Pacific Commerce | EAD | TAP | 2026 | $30,001 |
| 3 | Momentum Research | GEM | TAP | 2026 | $22,921 |
| 4 | Expert853 Industries | GEM | TAP | 2026 | $16,045 |
| … | 16 more companies | … | … | … | … |

**Key pattern:** TAP appears in 12 of 20 deals across EAD and GEM — this is systemic, not isolated.  
**Recommended fix:** Add an automated EOL check in the deal creation tool to block discontinued SKUs at entry.

---

## 💡 Bonus Insights (Not in the Brief)

### New vs Returning Customer Revenue
Revenue shifted from **100% new customers in 2023** to **76% returning customers in 2025** — Logitech's business transitioned from acquisition-driven to retention-driven in just 2 years.

> **Recommendation:** Track **Net Revenue Retention** as a primary GCC KPI going forward.

### GSC Cross-Sell Depth
The average Global Strategic company buys across **6.4 of 16 available product groups** — a **60% wallet share gap** inside accounts Logitech already owns and trusts.

> **Opportunity:** If the 208 GSC accounts bought peripherals at the same rate as local customers, that's meaningful incremental revenue from zero acquisition cost.

---

## 🛠 How to Run the Pipeline

### Requirements
```bash
pip install pandas numpy openpyxl python-calamine pyarrow
```

### Run
```bash
# Clone the repo
git clone https://github.com/Vishva-23/logitech-gcc-deal-analytics.git
cd logitech-gcc-deal-analytics

# Run the data prep pipeline
python analysis/data_prep_pipeline.py
```

> **Note:** The full raw dataset (449k rows, 54MB XLSX) is not included for confidentiality reasons. A 500-row anonymised sample with identical schema is provided in `data/sample_dataset_anonymised.csv`. The pipeline logic is fully documented and reproducible.

---

## 📊 How to View the Dashboard

1. Download `dashboard/Logitech_GCC_Analytics.twbx`
2. Open in **Tableau Desktop** or free **[Tableau Reader](https://www.tableau.com/products/reader)**
3. Navigate between **"Overview"** and **"Deep Insights"** tabs using the buttons at the top of each dashboard

---

## 🏢 Context

This project was built as a **final-round take-home assignment** for Logitech's **Data & Analytics Intern** role on the Global Customer Collaboration team (Cork, Ireland). The assignment was completed over 5 days and presented in a live 45-minute video interview.

The dataset and company names in the raw data are anonymised (Logitech's own anonymisation). All analysis, methodology decisions, visualisation, and strategic recommendations are original work.

---

## 📬 Contact

**Vishvasundar Senthilnathan**  
📧 [vishvaks2306@gmail.com](mailto:vishvaks2306@gmail.com)  
🔗 [linkedin.com/in/vishva-ks](https://linkedin.com/in/vishva-ks)  
🐙 [github.com/Vishva-23](https://github.com/Vishva-23)  
📍 Cork, Ireland

---

## 📄 Licence

This project is for portfolio and educational purposes. The original dataset belongs to Logitech. All company names in the sample data are fictional.
