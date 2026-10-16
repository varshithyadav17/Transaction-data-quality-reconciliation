"""Interactive audit-analytics view over the latest pipeline outputs."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
st.set_page_config(page_title="Transaction Quality & Reconciliation", page_icon="📊", layout="wide")


@st.cache_data
def load_outputs():
    required = {
        "kpis": OUT / "kpis.csv",
        "exceptions": OUT / "exceptions_report.csv",
        "reconciliation": OUT / "reconciliation.csv",
        "benford": OUT / "benford.csv",
    }
    missing = [str(path.relative_to(ROOT)) for path in required.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing pipeline outputs. Run python -m src.run_pipeline first: " + ", ".join(missing))
    return {name: pd.read_csv(path) for name, path in required.items()}


data = load_outputs()
kpis, exceptions = data["kpis"], data["exceptions"]
reconciliation, benford = data["reconciliation"], data["benford"]
st.title("Transaction Data Quality & Reconciliation")
st.caption("Synthetic portfolio dataset • exceptions are investigation leads, not proof of error or fraud")
row = kpis.iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", f"{int(row['total_transactions']):,}")
c2.metric("Distinct vendors", f"{int(row['distinct_vendors']):,}")
c3.metric("Missing critical fields", f"{int(row['missing_field_rows']):,}")
c4.metric("Duplicate candidates", f"{int(row['duplicate_payment_candidates']):,}")

left, right = st.columns([1, 1])
with left:
    st.subheader("Reconciliation by GL account")
    recon = reconciliation.copy()
    recon["variance"] = pd.to_numeric(recon["variance"], errors="coerce")
    fig = px.bar(recon, x="gl_account", y="variance", color="reconciled",
                 title="Actual total minus control total",
                 labels={"variance": "Variance (£)", "gl_account": "GL account"})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(reconciliation, use_container_width=True, hide_index=True)
with right:
    st.subheader("Exception volume by check")
    if "__check" in exceptions.columns and not exceptions.empty:
        counts = exceptions["__check"].fillna("unclassified").value_counts().rename_axis("check").reset_index(name="rows")
        fig = px.bar(counts, x="check", y="rows", title="Flagged rows by screen")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(counts, use_container_width=True, hide_index=True)
    else:
        st.info("No exception rows are present in the latest output.")

st.subheader("Benford first-digit screen")
b1, b2 = st.columns([2, 1])
with b1:
    fig = px.bar(benford, x="digit", y=["observed_freq", "expected_freq"], barmode="group",
                 title="Observed versus expected first-digit frequency",
                 labels={"value": "Frequency", "digit": "First digit", "variable": "Series"})
    st.plotly_chart(fig, use_container_width=True)
with b2:
    st.write("Use this plot to prioritise review only where the population is suitable. A deviation is not proof of fraud.")
    st.dataframe(benford, use_container_width=True, hide_index=True)

st.subheader("Investigate transaction-level exceptions")
if "__check" in exceptions.columns and not exceptions.empty:
    choices = sorted(exceptions["__check"].dropna().astype(str).unique().tolist())
    selected = st.multiselect("Filter by check", choices, default=choices)
    view = exceptions[exceptions["__check"].astype(str).isin(selected)]
    st.caption(f"{len(view):,} rows shown. Counts across checks may overlap.")
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.download_button("Download filtered exceptions (CSV)", view.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_exceptions.csv", mime="text/csv")
else:
    st.info("Run the pipeline to generate exception details.")
st.divider()
st.caption("Demonstration-only analysis. Verify exceptions using source documents and business context before drawing conclusions.")
