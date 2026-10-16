# Transaction Data Quality & Reconciliation

An end-to-end finance analytics project that ingests mixed CSV/Excel transaction exports, standardises records, loads a SQLite ledger, runs data-quality and reconciliation controls, screens duplicate-payment candidates, and produces exception reports for review.

**Stack:** Python · pandas · NumPy · SQLAlchemy · SQLite · SQL · Streamlit · Plotly · pytest · GitHub Actions

> **Data notice:** All transaction and vendor records are synthetic and generated for demonstration. Metrics below describe this seeded sample, not a real company, audit engagement, or verified financial loss.

## Business question

Can a finance or audit analyst turn inconsistent transaction exports into a repeatable, traceable set of quality checks and investigation priorities?

## What it does

- **Ingests mixed files:** CSV and Excel exports, vendor master, and GL control totals.
- **Standardises records:** date and currency parsing, whitespace cleanup, and vendor-name normalisation.
- **Runs control checks:** critical-field completeness, transaction-ID uniqueness, vendor referential integrity, and GL-level reconciliation.
- **Screens for exceptions:** duplicate-payment candidates and Benford first-digit patterns.
- **Persists data:** cleaned transactions and vendor records in SQLite.
- **Reports findings:** KPI CSV, reconciliation details, transaction-level exceptions, a Benford table, and an interactive Streamlit dashboard.
- **Tests reproducibility:** automated unit tests and CI on Python 3.11 and 3.12.

## Architecture

~~~mermaid
flowchart TD
    A[CSV and Excel exports] --> B[Ingestion and standardisation]
    B --> C[(SQLite ledger)]
    C --> D[Data quality controls]
    C --> E[GL reconciliation]
    C --> F[Exception screening]
    D --> G[CSV reports and dashboard]
    E --> G
    F --> G
~~~

## Current synthetic baseline

The checked-in example outputs report 10,150 transactions across 275 distinct vendors. The pipeline flags 130 rows with missing critical fields, 79 orphan vendor references, 6 GL-account reconciliation breaks, and 290 duplicate-payment candidates. These counts are screening results—not findings of fraud or confirmed financial loss.

The reconciliation output intentionally includes large breaks because the scenario is designed to exercise exception handling. The source control totals are generated before planted transaction changes are applied, so they should not be interpreted as an independent real-world control source.

## Run on Windows (PowerShell)

~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.run_pipeline
python -m pytest -q
streamlit run dashboard/app.py
~~~

If PowerShell blocks environment activation, use the venv Python directly:

~~~powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.run_pipeline
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
~~~

To use the checked-in inputs without regenerating them, run: python -m src.run_pipeline --no-regen

## Key outputs

| Output | Purpose |
|---|---|
| outputs/kpis.csv | Population and control-check KPIs |
| outputs/exceptions_report.csv | Records requiring investigation, tagged by check |
| outputs/reconciliation.csv | Control total, actual total, variance, and status by GL account |
| outputs/benford.csv | Observed versus expected first-digit frequencies |
| outputs/EXECUTIVE_FINDINGS.md | Summary of sample findings and follow-up steps |
| outputs/DASHBOARD.md | Reporting notes |
| data/processed/ledger.db | Local SQLite build output (not committed) |

See docs/data_dictionary.md for field meanings and docs/interview_walkthrough.md for the business rationale, methodology, and limitations.

## Interpretation and limitations

- Duplicate matches are **candidates**; confirm them against invoices, payment references, posting dates, credit notes, and the approval trail.
- Benford analysis is a **screening heuristic**, not a fraud detector. Use it only when the population is suitable and interpret deviations with domain context.
- The synthetic control totals are purpose-built for this exercise and are not independent external evidence.
- The default reconciliation tolerance is £0.01; a real finance team should define tolerances and rounding rules.
- Exception counts can overlap across checks. Do not sum them as if they were distinct financial losses.
- This is an educational portfolio project, not financial, audit, or legal advice.
