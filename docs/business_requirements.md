# Business Requirements Brief — Transaction Data Quality & Reconciliation

> **Case-study boundary:** This is a hypothetical accounts-payable / finance-operations scenario built on synthetic data. No real company, finance team, or audit engagement supplied requirements or signed off on this brief.

## 1. Problem statement

Finance analysts receive transaction exports in mixed CSV and Excel formats. Inconsistent dates and amount formats, missing fields, vendor-reference mismatches, suspected duplicate records, and differences against account control totals can make downstream reporting less reliable. Reviewing every row manually is slow and makes investigation decisions harder to reproduce.

## 2. Business objective

Design a repeatable analyst workflow that standardises transaction records, applies explicit controls, traces exceptions to reviewable rows, and summarises issues for a finance decision-maker. The goal of this prototype is improved **visibility and repeatability**; it does not establish that any real financial loss was prevented.

## 3. Illustrative stakeholders

| Role | Need / decision |
|---|---|
| Accounts Payable (AP) analyst | Review exceptions with transaction-level evidence |
| AP / Finance manager | Prioritise issues and monitor resolution |
| Vendor master-data owner | Resolve invalid or missing vendor references |
| Financial controller | Review account-level reconciliation variances |
| Data / IT support | Confirm source formats, mappings, and refresh reliability |
| Internal audit / controls reviewer | Understand control logic, evidence, and limitations |

These roles are proposed for the scenario and have not been interviewed.

## 4. Scope

**In scope:** CSV/XLSX ingestion; basic field normalisation; completeness and ID uniqueness checks; vendor referential-integrity checks; GL-level comparison to supplied control totals; duplicate-payment candidate screening; first-digit screening as an optional heuristic; SQLite storage; summary and exception outputs; dashboard filtering and CSV download.

**Out of scope:** payment blocking, automatic vendor-master edits, payment release decisions, fraud determination, ERP integration, approval workflows, production access control, and financial/audit sign-off.

## 5. Business requirements

| ID | Requirement | Priority | Acceptance evidence |
|---|---|---|---|
| BR-01 | Preserve the source-file context for ingested rows | Must | Output rows retain source lineage where available |
| BR-02 | Standardise date and amount representations before aggregation | Must | Known parseable sample values produce consistent normalized values |
| BR-03 | Identify records missing critical fields and duplicate transaction IDs | Must | Separate counts and row-level exceptions are produced |
| BR-04 | Flag transaction vendor IDs not found in the vendor master | Must | Orphan references are extractable for follow-up |
| BR-05 | Reconcile transaction totals by GL account against a configured control source and tolerance | Must | Output includes expected value, actual value, variance, and status |
| BR-06 | Produce reviewable duplicate-payment candidates with the matching basis visible | Should | Matching groups can be traced to source rows; candidate status is not labelled as confirmed fraud |
| BR-07 | Give an analyst a filterable view of issues and downloadable detail | Should | Check type and records can be filtered and exported |
| BR-08 | Make the run reproducible and testable | Must | Fixed sample, documented commands, automated tests, and CI |

## 6. Non-functional requirements

- **Traceability:** definitions and assumptions are documented; exceptions can be traced to the applicable check.
- **Repeatability:** a clean environment can regenerate analytical outputs from documented inputs.
- **Interpretability:** thresholds, keys, and limitations are explicit rather than hidden in the dashboard.
- **Data safety:** portfolio sample records are synthetic; no credentials or production finance records are required.

## 7. Business rules and assumptions

- The supplied control totals are an instructional reference, not an independent source of accounting truth.
- Reconciliation tolerance is configurable; the current example uses £0.01.
- Exceptions can overlap. Exception-row counts must not be added together as if they were unique transactions or financial loss.
- Duplicate matching produces candidates that require invoice, payment, credit-note, and approval evidence.
- Benford screening is only an investigation heuristic for suitable populations.

## 8. Definition of done

The pipeline produces documented KPI, reconciliation, and exception outputs; the dashboard exposes those outputs; the tests pass; the run instructions work in a fresh environment; and reporting clearly distinguishes synthetic observations from verified business outcomes.

## 9. Key risks and dependencies

| Risk / dependency | Mitigation |
|---|---|
| Incorrect or incomplete source mapping | Validate schemas and retain source-file metadata |
| Control totals are not independent | State their source and confirm against an approved finance control in a real deployment |
| False positives from heuristic matching | Require human review and record disposition |
| Currency or sign conventions differ | Define currency-aware rules before production use |
| Unclear exception ownership | Assign an owner, evidence requirement, status, and resolution date in a future workflow |
