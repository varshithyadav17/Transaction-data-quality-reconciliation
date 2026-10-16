# Interview Walkthrough: Transaction Data Quality & Reconciliation

## 60-second summary

“I built a reproducible finance-analytics pipeline for messy CSV and Excel exports. It normalises amounts and dates, loads cleaned transactions and the vendor master into SQLite, and runs completeness, transaction-ID uniqueness, vendor referential-integrity, general-ledger reconciliation, duplicate-payment, and Benford screening checks. Outputs include a KPI extract, account-level variances, and record-level exceptions that can be reviewed in a small Streamlit dashboard. The data is synthetic; the value of the project is in control design, traceability, and analyst triage—not in claiming a real fraud finding.”

## Business workflow

1. Ingest exports from different source formats and preserve a source-file marker.
2. Standardise amount and date representations so equivalent values can be analysed consistently.
3. Load the prepared population into SQLite for reproducible querying.
4. Run independent checks for missing critical fields, duplicate IDs, orphan vendor IDs, and account-level reconciliation.
5. Screen and triage duplicate-payment candidates and first-digit patterns.
6. Report both overall control KPIs and transaction-level detail that can be traced back to the source.

## Why these checks?

- **Completeness:** missing amount, date, or vendor identifiers can make a record unusable for later tests.
- **Uniqueness:** repeated transaction IDs can indicate a duplicate extract, an ingestion defect, or an identifier issue; context decides which.
- **Referential integrity:** a populated transaction vendor ID absent from the master is a join/control exception.
- **Reconciliation:** aggregate ledger values are compared to the supplied control total for each GL account using a configurable tolerance.
- **Duplicate-payment candidate screening:** matches on vendor, invoice reference, and amount are efficient first-pass candidates, but should be validated against documents and payment history.
- **Benford screening:** a first-digit distribution can help prioritise review for suitable naturally occurring numeric populations; it is not suitable for every dataset and is not a fraud conclusion.

## Results to discuss

The checked-in baseline reports 10,150 rows, 275 distinct vendors, 130 rows with missing critical fields, 79 orphan vendor references, 6 account-level reconciliation breaks, and 290 duplicate-candidate rows. The Benford mean absolute deviation is 0.00271 under the current implementation's label thresholds.

Describe these figures as results on a synthetic, intentionally imperfect dataset. Duplicate candidates can overlap with other exceptions and do not imply a loss amount. The synthetic controls are created before selected ledger records are modified, which explains why the baseline is designed to show account-level breaks.

## Limitations and follow-up

- The current reconciliation control totals are synthetic; a production workflow would obtain independent totals and document source lineage.
- The current duplicate key is a heuristic. A real review may also use payment reference, invoice dates, currency, purchase order, and vendor-specific rules.
- Benford output is a screen whose usefulness depends on the population and amount-generation process.
- The project currently produces descriptive controls, not automatic remediation or a fraud classifier.
- A real workflow would assign each exception an owner, evidence requirement, disposition, and remediation status.

## Likely interview questions

**Why retain bad rows instead of dropping them?**  
Because the job of a data-quality pipeline is to make quality problems visible. Silently deleting them can hide the scale and pattern of a source issue.

**Why use SQLite?**  
It demonstrates a relational analytical store and SQL joins/aggregations without requiring a managed database server. The database is rebuildable and kept out of version control.

**Are the duplicate-payment candidates confirmed duplicates?**  
No. They are candidates on matching fields. Documents and payment evidence are required before making that claim.

**How would you improve it for production?**  
Add schema contracts, source-row lineage, idempotent loads, currency-aware reconciliation, threshold configuration, exception ownership/workflow, logging, and review sign-off.
