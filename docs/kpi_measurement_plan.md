# KPI & Measurement Plan — Transaction Controls

> Baseline figures below are generated from the checked-in synthetic scenario. Any production targets are proposals to agree with process owners, not commitments or proven improvements.

## KPI catalogue

| KPI | Definition | Current synthetic baseline | Proposed use / decision |
|---|---|---:|---|
| Population rows | Number of ingested transaction rows in the current sample | 10,150 | Verify population and refresh completeness |
| Missing-critical-field rows | Rows failing at least one configured critical-field completeness check | 130 | Route to source owner and monitor repeat defects |
| Orphan vendor references | Transaction vendor IDs with no matching vendor master record | 79 | Investigate master-data/interface issues |
| GL accounts outside tolerance | Number of GL-account reconciliations failing the configured tolerance | 6 | Triage variance and confirm control-source validity |
| Duplicate-payment candidate rows | Rows belonging to matching groups under the configured heuristic | 290 | Human-review queue; not confirmed duplicates |
| Reconciliation variance | Ledger aggregate minus approved control total by account | See generated reconciliation output | Evidence-based disposition by account |
| Exception disposition rate (future) | Exceptions with documented outcome / all exceptions reviewed | Not currently measured | Monitor whether the review process closes the loop |

## Measurement rules

- State period, source files, population rules, currency, sign convention, and tolerance alongside each run.
- Do not sum exception counts into a total number of unique bad transactions; checks can overlap.
- Do not infer cash loss from a duplicate candidate count or an account variance in this synthetic setup.
- A real baseline should use an approved independent control source and confirmed data lineage.
- Benford results are a secondary screening metric only and require suitability review.

## Proposed pilot success criteria (to agree before a real pilot)

1. 100% of scheduled input files are accounted for by a documented row-count and file-level reconciliation.
2. 100% of exceptions in the pilot sample have a check type and enough key fields to locate the source row.
3. Every material reconciliation variance has a documented review disposition, owner, and supporting evidence before sign-off.
4. At least 95% of records pass schema and required-field checks, **if** the process owner confirms that this is an appropriate starting threshold; otherwise establish target from measured source quality.
5. Compare analyst handling time and repeat-exception rate against a measured baseline before claiming efficiency gains.

These are draft acceptance ideas, not achieved results. Thresholds need stakeholder agreement and baseline validation.

## Measurement design

1. **Baseline:** observe one or more comparable reporting cycles, document current manual effort, rework, exception volume and reconciliation completion time.
2. **Pilot:** run the standardised checks alongside the existing process so results can be reconciled before relying on the new output.
3. **Quality gate:** validate independent control totals and sample exceptions against source evidence.
4. **Evaluate:** compare completeness, unresolved variance, repeat defects, review time and false-positive burden.
5. **Decide:** adopt, revise, or roll back based on accuracy, usefulness, and control-owner approval.

## Data owners and cadence (proposed)

| Measure | Primary reviewer | Cadence |
|---|---|---|
| Input completeness / parsing | Data or interface owner | Every load |
| GL variance | Financial controller | Each close / reporting cycle |
| Exception triage and disposition | AP manager | Weekly during pilot |
| Repeat vendor-reference defects | Vendor master owner | Monthly |
| Process effort and quality trend | Finance process owner | Before pilot and at agreed review checkpoints |
