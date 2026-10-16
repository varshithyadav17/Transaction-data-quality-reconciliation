# Executive Findings — Synthetic Accounts-Payable Dataset

## Scope and data boundary

This report summarises the example outputs produced by the repository pipeline. The ledger, vendor master, and GL control totals are synthetic and intentionally include planted quality issues. This is an educational portfolio analysis, not the result of a real audit engagement.

## Findings at a glance

| Control / screen | Example result | Business relevance |
|---|---:|---|
| Population size | 10,150 rows | Establishes the population used in the checks |
| Distinct vendors | 275 | Vendor master population in this sample |
| Missing critical fields | 130 rows | Missing amount, date, or vendor fields weaken downstream analysis |
| Orphan vendor references | 79 rows | Transactions refer to IDs not present in the vendor master |
| GL reconciliation breaks | 6 accounts | Ledger totals do not match the supplied synthetic controls |
| Duplicate-payment candidates | 290 rows | Candidate groups require document-level corroboration |
| Benford mean absolute deviation | 0.00271 (labelled “close” by this code) | A population-level screen; not a verdict |

Counts can overlap because a record may fail more than one control. The 290 duplicate candidates are rows in matching groups, not necessarily 290 distinct duplicate payments or a confirmed loss amount.

## Recommended analyst follow-up

1. Validate the source population, extraction criteria, completeness, and file lineage.
2. Investigate missing critical fields with data owners and quantify their effect on downstream reports.
3. Trace orphan vendor IDs to master-data changes, interface errors, or timing differences.
4. Break reconciliation variances down by account and period; agree each item to evidence rather than merely changing tolerance.
5. Sample duplicate candidates and compare invoice number, vendor, amount, dates, payment reference, credit notes, and approval trail.
6. Use Benford deviations only when the amount population is appropriate for the technique; consider transaction-level context and other risk signals.

## Interpretation boundary

Benford screening and duplicate matching identify items for human review. Neither establishes fraud. The supplied control totals are deliberately separate from the final modified transaction population; therefore, these reconciliation breaks are a demonstration scenario, not evidence of a real accounting misstatement.
