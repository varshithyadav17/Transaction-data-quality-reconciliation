# User Stories & Acceptance Criteria — Transaction Controls

> User stories are drafted for a hypothetical finance-operations workflow. They are not sourced from interviews or an approved production backlog.

## Epic: Prepare a trustworthy transaction population

### US-01 — Standardise imports
**As an AP analyst**, I want CSV and Excel transaction exports normalised consistently so that equivalent source values can be compared.

**Acceptance criteria**
- Given a supported file with documented columns, when the pipeline runs, then dates and amounts are converted using explicit parsing rules.
- Given an unsupported or unparseable value, when the row is processed, then the issue is surfaced in a quality output rather than silently treated as valid.
- Given multiple source files, when records are combined, then source-file context is retained where available.

### US-02 — Identify missing critical fields
**As an AP analyst**, I want missing critical values flagged so that affected records can be corrected or excluded under an approved rule.

**Acceptance criteria**
- Given a row with a missing critical field, when quality checks run, then the row is represented in the relevant exception output.
- Given a clean row, when quality checks run, then it is not falsely marked missing.
- The report states the fields considered critical.

### US-03 — Detect vendor reference mismatches
**As a vendor master-data owner**, I want transaction IDs that do not map to the vendor master so that master-data or interface issues can be investigated.

**Acceptance criteria**
- Given a populated transaction vendor ID absent from the vendor master, when referential-integrity checks run, then it is flagged.
- Given a valid mapped vendor ID, then it is not flagged as orphaned.
- The output retains the transaction key and vendor key needed to locate the issue.

## Epic: Apply financial controls

### US-04 — Review reconciliation variances
**As a financial controller**, I want ledger totals compared with a specified control total by GL account so that material differences are visible.

**Acceptance criteria**
- Given a control total and ledger total for an account, when the reconciliation runs, then expected amount, actual amount, variance and pass/fail status are produced.
- Given a configured tolerance, then status is evaluated against that tolerance rather than a hidden constant.
- The report identifies the origin and limitations of the control-total source.

### US-05 — Review duplicate-payment candidates
**As an AP analyst**, I want potential duplicate patterns surfaced with matching fields so that I can validate them against original evidence.

**Acceptance criteria**
- Given matching vendor, invoice reference and amount fields under the configured rule, then a candidate group is produced.
- Candidate language does not state that fraud or duplicate payment is confirmed.
- The review guidance lists relevant corroborating evidence such as invoice, payment reference, credit note and approval trail.

## Epic: Communicate findings

### US-06 — Filter and export exceptions
**As an AP manager**, I want to filter exception types and export the relevant rows so that triage can be shared in a review.

**Acceptance criteria**
- Given the dashboard, then the analyst can view overall KPIs and relevant exception details.
- Given a filtered result, then the visible subset can be downloaded.
- Summary counts and row-level outputs use documented definitions and retain overlapping-check caveats.

## Traceability

| Story | Requirement | Evidence |
|---|---|---|
| US-01 | BR-01, BR-02 | Source context + normalised pipeline outputs |
| US-02 | BR-03 | Quality checks and exception report |
| US-03 | BR-04 | Referential-integrity results |
| US-04 | BR-05 | GL reconciliation report |
| US-05 | BR-06 | Candidate screening and review guidance |
| US-06 | BR-07 | Streamlit dashboard and download |

## Release acceptance checklist

- [ ] Input schema and critical fields are documented.
- [ ] A fresh run reproduces the example outputs.
- [ ] Automated tests pass.
- [ ] Reconciliation source and tolerance are shown.
- [ ] Duplicate candidates are not described as confirmed duplicates.
- [ ] Dashboard output can be traced to the underlying report.
- [ ] Synthetic-data limitations appear in the README and report.
