# Aegis Crest Financial - Developer Setup & Replication Guide

## Quick Start (3 Steps)

### Prerequisites
- Python 3.9+ installed
- Node.js 18+ and `npm` installed
- Git CLI

---

### Step 1: Clone Repository & Initialize Database
```bash
git clone https://github.com/bhriguverma/enterprise-banking-ops-analytics.git
cd enterprise-banking-ops-analytics

# 1. Install Python dependencies
python3 -m pip install faker pandas numpy openpyxl

# 2. Run Synthetic Data Generator (~861,000 rows across 13 tables)
python3 data_generation/generator.py

# 3. Load Analytical Views and Triggers
python3 -c "import sqlite3; conn=sqlite3.connect('aegis_banking.db'); conn.executescript(open('database/views.sql').read()); conn.executescript(open('database/stored_procedures.sql').read()); conn.commit();"
```

---

### Step 2: Build & Launch Interactive Web Dashboard
```bash
cd dashboards/webapp

# Install dependencies
npm install

# Build Next.js app
npm run build

# Start local server
npm run dev
```
Open **`http://localhost:3000`** in your browser to view the live dashboard and try the **Natural-Language-to-SQL AI Chat Engine**.

---

### Step 3: Generate Excel Reporting Workbook
```bash
# Run Excel workbook generator
python3 excel/generate_excel.py
```
Output workbook will be created at `excel/Aegis_Banking_Operations_Reporting.xlsx`.

---

## Directory Structure
```
enterprise-banking-ops-analytics/
├── aegis_banking.db           # 861k-row SQLite database
├── data_generation/
│   ├── generator.py           # 13-table data generator script
│   └── build_sql_queries.py   # SQL query library builder
├── database/
│   ├── schema.sql             # 3NF DDL schema
│   ├── views.sql              # Analytical views
│   └── stored_procedures.sql  # Operational triggers
├── sql_queries/
│   ├── tier1_foundational/    # 12 basic queries
│   ├── tier2_joins_aggregations/# 12 multi-table join queries
│   ├── tier3_window_ranking/  # 12 window & ranking queries
│   └── tier4_advanced_ctes_views/# 12 advanced CTE cohort queries
├── dashboards/
│   ├── powerbi/
│   │   └── dax_measures.dax   # Power BI DAX measure script
│   └── webapp/                # Next.js + Recharts + Tailwind web app
├── excel/
│   ├── generate_excel.py      # openpyxl generator script
│   └── Aegis_Banking_Operations_Reporting.xlsx
├── docs/
│   ├── ER_DIAGRAM.md
│   ├── KPI_DICTIONARY.md
│   ├── SCHEMA.md
│   └── SETUP.md
├── reports/
│   ├── executive_memo.md
│   ├── performance_case_study.md
│   └── process_improvement_diagram.md
└── README.md
```
