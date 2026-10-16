import numpy as np
import pandas as pd
import pytest

from src import anomaly
from src import clean
from src import quality_checks as qc


def _df(records):
    return pd.DataFrame(records)


def test_completeness_flags_missing():
    frame = _df([
        {"transaction_id": "T1", "vendor_id": "V1", "txn_date": pd.Timestamp("2024-01-01"), "amount": 10.0},
        {"transaction_id": "T2", "vendor_id": None, "txn_date": pd.Timestamp("2024-01-02"), "amount": 20.0},
    ])
    result = qc.check_completeness(frame)
    assert not result["passed"]
    assert result["n_flagged"] == 1
    assert result["rows"]["__issue"].eq("missing_critical_field").all()


def test_uniqueness_flags_all_rows_in_duplicate_group():
    frame = _df([
        {"transaction_id": "T1", "vendor_id": "V1", "txn_date": pd.Timestamp("2024-01-01"), "amount": 10.0},
        {"transaction_id": "T1", "vendor_id": "V1", "txn_date": pd.Timestamp("2024-01-03"), "amount": 11.0},
        {"transaction_id": None, "vendor_id": "V2", "txn_date": pd.Timestamp("2024-01-03"), "amount": 11.0},
    ])
    assert qc.check_uniqueness(frame)["n_flagged"] == 2


def test_referential_integrity_flags_orphan_vendor():
    transactions = _df([
        {"transaction_id": "T1", "vendor_id": "V1", "amount": 10.0},
        {"transaction_id": "T2", "vendor_id": "V9", "amount": 10.0},
    ])
    vendors = _df([{"vendor_id": "V1", "vendor_name": "Acme"}])
    result = qc.check_referential_integrity(transactions, vendors)
    assert result["n_flagged"] == 1
    assert result["rows"].iloc[0]["vendor_id"] == "V9"


def test_reconciliation_detects_variance():
    transactions = _df([
        {"gl_account": "6000", "amount": 100.0},
        {"gl_account": "6000", "amount": 50.0},
    ])
    control = _df([{"gl_account": "6000", "control_total": 200.0}])
    result = qc.check_reconciliation(transactions, control)
    assert not result["passed"]
    assert result["n_breaks"] == 1
    assert result["detail"].iloc[0]["variance"] == -50.0


def test_reconciliation_includes_control_only_and_ledger_only_accounts():
    transactions = _df([
        {"gl_account": "6000", "amount": 100.0},
        {"gl_account": "6100", "amount": 15.0},
    ])
    control = _df([
        {"gl_account": "6000", "control_total": 100.0},
        {"gl_account": "6200", "control_total": 10.0},
    ])
    result = qc.check_reconciliation(transactions, control)
    detail = result["detail"].set_index("gl_account")
    assert set(detail.index) == {"6000", "6100", "6200"}
    assert bool(detail.loc["6000", "reconciled"])
    assert not bool(detail.loc["6100", "reconciled"])
    assert not bool(detail.loc["6200", "reconciled"])


def test_money_parser_handles_currency_and_parentheses():
    assert clean._parse_amount("£1,234.50") == pytest.approx(1234.50)
    assert clean._parse_amount("(£25.00)") == pytest.approx(-25.00)
    assert np.isnan(clean._parse_amount("not-a-number"))
    assert np.isnan(clean._parse_amount(""))


def test_clean_transactions_standardises_and_drops_exact_rows():
    frame = _df([
        {"transaction_id": " T1 ", "vendor_id": " V1 ", "txn_date": "01/02/2024", "amount": "£15.00", "gl_account": "6000"},
        {"transaction_id": " T1 ", "vendor_id": " V1 ", "txn_date": "01/02/2024", "amount": "£15.00", "gl_account": "6000"},
    ])
    cleaned, summary = clean.clean_transactions(frame)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["transaction_id"] == "T1"
    assert cleaned.iloc[0]["vendor_id"] == "V1"
    assert cleaned.iloc[0]["amount"] == pytest.approx(15.0)
    assert summary["exact_duplicates_removed"] == 1


def test_duplicate_payment_screening_flags_candidate_pair():
    frame = _df([
        {"transaction_id": "T1", "vendor_id": "V1", "invoice_number": "INV-1", "amount": 50.0},
        {"transaction_id": "T2", "vendor_id": "V1", "invoice_number": "INV-1", "amount": 50.0},
        {"transaction_id": "T3", "vendor_id": "V1", "invoice_number": "INV-2", "amount": 50.0},
    ])
    result = anomaly.detect_duplicate_payments(frame)
    assert result["n_flagged"] == 2
    assert result["rows"]["__issue"].eq("duplicate_payment_candidate").all()


def test_benford_runs_and_sums_to_one():
    result = anomaly.benford_test(pd.Series(np.random.default_rng(42).lognormal(6, 1.1, 2000)))
    assert set(result["table"]["digit"]) == set(range(1, 10))
    assert result["table"]["observed_freq"].sum() == pytest.approx(1.0, abs=0.01)


def test_benford_requires_nonzero_amount():
    with pytest.raises(ValueError):
        anomaly.benford_test(pd.Series([0, 0, np.nan]))
