# Data Dictionary

All included records are synthetic. The raw inputs intentionally mix common export formats and selected quality issues.

## Raw inputs

### data/raw/transactions_2024_h1.csv, transactions_2024_h2.csv, transactions_2025.xlsx

| Field | Meaning | Control relevance |
|---|---|---|
| transaction_id | Identifier assigned to a transaction row | Uniqueness and traceability |
| vendor_id | Supplier key used to join the vendor master | Referential integrity |
| invoice_number | Supplier invoice reference | Duplicate-candidate screening |
| txn_date | Transaction date; formats vary across files | Completeness and period analysis |
| amount | Signed transaction amount; symbols/formatting vary | Reconciliation and outlier screening |
| currency | Currency code for the row | Currency consistency review |
| gl_account | General-ledger account code | Control-total aggregation |
| description | Short transaction description | Review context |

The ingest step appends __source_file before combining source exports. The cleaning stage standardises names and amount/date fields and removes exact duplicate rows. Rows with missing or unparseable critical fields are retained for controls where possible.

### data/raw/vendors.csv

| Field | Meaning |
|---|---|
| vendor_id | Vendor master key |
| vendor_name | Vendor display name, intentionally inconsistent in case/spacing |
| category | Broad synthetic spend category |

### data/raw/control_totals.csv

| Field | Meaning |
|---|---|
| gl_account | Account key used for reconciliation |
| control_total | Synthetic expected amount supplied for the account |

These control totals are generated before selected transaction changes are introduced. They are therefore an instructional benchmark, not an independent accounting control record.

## Main outputs

| File | Grain / key fields | Interpretation |
|---|---|---|
| outputs/kpis.csv | One row per pipeline run | Population totals and exception counts |
| outputs/exceptions_report.csv | One row per flagged record per applicable check; __check identifies the check | Rows for analyst investigation; checks may overlap |
| outputs/reconciliation.csv | One row per GL account | Control total, ledger total, variance, and tolerance result |
| outputs/benford.csv | One row per first digit 1–9 | Observed/expected frequency and observed count |
| data/processed/ledger.db | SQLite tables transactions and vendors | Local analytical store |
