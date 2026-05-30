"""
=============================================================
Logitech GCC B2B Deal Analytics — Data Preparation Pipeline
=============================================================
Author      : Vishvasundar Senthilnathan
GitHub      : https://github.com/Vishva-23
Description : End-to-end data cleaning, enrichment, and
              aggregation pipeline for the Logitech Global
              Customer Collaboration (GCC) deal dataset.

Dataset     : 449,262 rows x 27 columns (after cleaning)
Tools       : Python 3.12, pandas, numpy
=============================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────
RAW_FILE      = "data/deal_download_raw_data_set.xlsx"
EOL_FILE      = "data/EOL_SKUs_Reference.xlsx"
OUTPUT_CSV    = "data/Logitech_Full_Enriched_Data.csv"
ANALYSIS_DATE = pd.Timestamp("2026-04-24")   # Date of analysis

# ═══════════════════════════════════════════════════════════
# STEP 1: LOAD DATA
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 1: Loading raw data...")
print("=" * 60)

df = pd.read_excel(RAW_FILE, sheet_name="DataCW", header=20,
                   engine="calamine")
print(f"  Raw rows loaded     : {len(df):,}")

eol = pd.read_excel(EOL_FILE, sheet_name="EOL SKUs",
                    engine="calamine", header=1)
eol_product_numbers = set(
    eol["Product Number"].astype(str).str.strip()
)
print(f"  EOL SKUs reference  : {len(eol_product_numbers)} products")

# ═══════════════════════════════════════════════════════════
# STEP 2: CLEAN DATA
# ═══════════════════════════════════════════════════════════
print("\nSTEP 2: Cleaning data...")

# Remove ERROR rows, null rows, and the summary 'Total' row
df = df[
    df["B2B Sales Region"].notna()
    & (df["B2B Sales Region"] != "ERROR")
    & (df["B2B Sales Region"] != "Total")
].copy()
print(f"  After removing ERROR/null/Total rows : {len(df):,}")

# Fix date columns
for col in ["Close Date", "Created Date", "Last Modified Date"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Fix numeric columns
for col in ["Total Price (converted USD)", "Total Price (Local)",
            "Quantity", "Probability (%)"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"  Date and numeric columns parsed.")

# ═══════════════════════════════════════════════════════════
# STEP 3: DERIVE COLUMN Y — Account Type
# ═══════════════════════════════════════════════════════════
print("\nSTEP 3: Deriving Column Y — Account Type...")

# DEFINITION:
#   Global Strategic Customer = Company Segmentation = 'Global'
#                               AND Company Designation = 'Strategic'
#   Rationale: The dataset filter header states 'Strategic Group
#   Owner not equal to blank' — requiring both conditions ensures
#   only formally assigned strategic accounts are classified.
df["Account Type"] = np.where(
    (df["Company Segmentation"] == "Global")
    & (df["Company Designation"] == "Strategic"),
    "Global Strategic Customer",
    "Local Customer",
)

gsc_count = (df["Account Type"] == "Global Strategic Customer").sum()
local_count = (df["Account Type"] == "Local Customer").sum()
print(f"  Global Strategic rows : {gsc_count:,}")
print(f"  Local Customer rows   : {local_count:,}")

# ═══════════════════════════════════════════════════════════
# STEP 4: DERIVE COLUMN Z — Fiscal Year
#         DERIVE COLUMN AA — Fiscal Quarter
# ═══════════════════════════════════════════════════════════
print("\nSTEP 4: Deriving Columns Z (FY) and AA (FQ)...")

# Logitech FY runs April → March (e.g. FY2026 = Apr 2025 – Mar 2026)
# Fiscal Period column is already formatted as 'YYYY-QN'
# We extract directly — DO NOT derive from Close Date (calendar year
# logic would produce wrong fiscal year assignments).
df["FY"] = df["Fiscal Period"].str.split("-").str[0]
df["FQ"] = df["Fiscal Period"].str.split("-").str[1]

print(f"  FY values  : {sorted(df['FY'].dropna().unique())}")
print(f"  FQ values  : {sorted(df['FQ'].dropna().unique())}")

# ═══════════════════════════════════════════════════════════
# STEP 5: EOL PRODUCT FLAG
# ═══════════════════════════════════════════════════════════
print("\nSTEP 5: Flagging EOL products...")

df["Is_EOL_Product"] = (
    df["Product Number"].astype(str).str.strip().isin(eol_product_numbers)
)
print(f"  EOL-flagged rows : {df['Is_EOL_Product'].sum():,}")

# ═══════════════════════════════════════════════════════════
# STEP 6: EOL IN FUTURE DEALS — KEY RISK FINDING
# ═══════════════════════════════════════════════════════════
print("\nSTEP 6: Analysing EOL risk in future pipeline...")

future_eol = df[
    df["Is_EOL_Product"] & (df["Close Date"] > ANALYSIS_DATE)
]
print(f"  ⚠ Future deals with EOL products  : {len(future_eol):,} rows")
print(f"  ⚠ Unique companies at risk         : {future_eol['Company Name'].nunique():,}")
print(f"  ⚠ Total USD at risk                : ${future_eol['Total Price (converted USD)'].sum():,.0f}")

# ═══════════════════════════════════════════════════════════
# STEP 7: EXPORT ENRICHED DATASET
# ═══════════════════════════════════════════════════════════
print("\nSTEP 7: Exporting enriched dataset...")

df.to_csv(OUTPUT_CSV, index=False)
print(f"  Exported to : {OUTPUT_CSV}")
print(f"  Final shape : {df.shape[0]:,} rows x {df.shape[1]} columns")

# ═══════════════════════════════════════════════════════════
# STEP 8: PRINT SUMMARY STATS
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("ANALYSIS SUMMARY")
print("=" * 60)

won = df[df["Stage(SFDC)"] == "Closed Won"]
gsc = df[df["Account Type"] == "Global Strategic Customer"]

print(f"  Total rows (clean)         : {len(df):,}")
print(f"  Total revenue (USD)        : ${df['Total Price (converted USD)'].sum()/1e9:.2f}B")
print(f"  Closed Won revenue         : ${won['Total Price (converted USD)'].sum()/1e9:.2f}B")
print(f"  Unique companies           : {df['Company Name'].nunique():,}")
print(f"  Unique deals               : {df['Deal ID'].nunique():,}")
print(f"  GSC companies              : {gsc['Company Name'].nunique()}")
print(f"  GSC revenue                : ${gsc['Total Price (converted USD)'].sum()/1e9:.2f}B")
print(f"  GSC revenue share          : {100*gsc['Total Price (converted USD)'].sum()/df['Total Price (converted USD)'].sum():.1f}%")
print(f"  Top region                 : {df.groupby('B2B Sales Region')['Total Price (converted USD)'].sum().idxmax()}")
print(f"  Top product group          : {won.groupby('Product Group Name')['Total Price (converted USD)'].sum().idxmax()}")
print(f"  EOL pipeline risk (USD)    : ${future_eol['Total Price (converted USD)'].sum():,.0f}")
print("=" * 60)
print("Pipeline complete.")
