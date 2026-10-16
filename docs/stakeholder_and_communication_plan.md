# Stakeholder & Communication Plan — Transaction Data Quality

> **Illustrative plan only:** Stakeholders are hypothetical roles in a finance-operations case study. No actual stakeholder consultation has occurred.

## Stakeholder map

| Stakeholder role | Interest / influence | Information needed | Proposed engagement |
|---|---|---|---|
| AP analyst | High / high | Exception rows, source fields, matching rationale | Walkthrough of queue and sample exceptions |
| AP manager | High / high | Exception volume by type, prioritisation, aging (future enhancement) | Weekly review of priorities and blockers |
| Financial controller | High / high | GL variance, tolerance, evidence of resolution | Reconciliation review and sign-off rules |
| Vendor master-data owner | Medium / medium | Orphan IDs, duplicate vendor concerns, valid master references | Exception handoff with owner and due date |
| Data / IT support | Medium / high | File layouts, refresh errors, source lineage | Source mapping and failure triage |
| Internal audit / controls reviewer | High / medium | Control definitions, scope, evidence trail, limitations | Review control design and sampling approach |

Influence/interest classifications are working assumptions and should be validated with a real team.

## Communication principles

1. Separate the **population summary** from individual exceptions.
2. State the control definition, source, cut-off, and tolerance with every reconciliation result.
3. Use neutral wording such as “candidate,” “missing field,” or “variance”; do not label a row fraudulent without investigation evidence.
4. Include severity, evidence required, proposed owner, status, and next action in a production exception register.
5. Document decisions, changes to thresholds, and unresolved assumptions.

## Suggested communication cadence

| Touchpoint | Audience | Content | Decision expected |
|---|---|---|---|
| Source-readiness review | AP analyst + data/IT | Schema, completeness, currency, date conventions, source lineage | Approve test population or request corrections |
| Exception triage | AP analyst + AP manager | High-risk candidates, missing values, orphan keys | Assign investigation owners |
| Reconciliation review | Controller + AP | Account variances and supporting evidence | Accept, investigate, or correct with an audit trail |
| Periodic control review | Finance + controls | Repeat exceptions, recurring source defects, threshold changes | Prioritise root-cause remediation |

## Escalation principles

- Escalate an unexplained GL variance according to a finance-approved materiality / tolerance policy.
- Escalate repeated interface or master-data failures to the accountable process owner.
- Do not block payments or change source records based only on this portfolio prototype.
- Retain unresolved issues and their rationale instead of silently dropping them.

## RACI proposal

| Activity | AP analyst | AP manager | Controller | Data/IT | Vendor master owner |
|---|---|---|---|---|---|
| Confirm input data and file mappings | R | A | C | R | C |
| Investigate individual exceptions | R | A | C | C | R for vendor keys |
| Review GL reconciliation | R | C | A | C | I |
| Fix source/interface defects | C | I | C | A/R | C |
| Approve control policy / tolerance | C | C | A/R | I | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed. This is a draft governance model, not an agreed organisational RACI.
