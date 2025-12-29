import streamlit as st
import pandas as pd

from graph.analytics_graph import analytics_graph
from core.db import write_table
from core.pdf import generate_pdf

st.title("Enterprise AI Analytics Platform")

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

file = st.file_uploader("Upload CSV")

if file is not None:
    df = load_data(file)
    st.subheader("Data Preview")
    st.dataframe(df.head())

    date_col = st.selectbox("Select date column", list(df.columns))
    numeric_cols = list(df.select_dtypes(include="number").columns)

    if not numeric_cols:
        st.error("No numeric columns found.")
        st.stop()

    value_col = st.selectbox("Select metric column", numeric_cols)

    if st.button("Run Analysis", type="primary"):
        # ✅ state is CREATED HERE
        state = analytics_graph.invoke({
            "df": df.sort_values(by=date_col),
            "date": date_col,
            "value": value_col
        })

        st.subheader("Insights")
        st.write(state["insights"])

        st.subheader("Executive Summary")
        st.write(state["summary"])

        # ✅ Save outputs ONLY after state exists
        write_table(state["kpis"], "fact_kpis")
        state["kpis"].to_csv("fact_kpis.csv", index=False)

        st.success("KPIs saved to SQLite DB and CSV!")

        pdf_path = generate_pdf(state["summary"])
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF Report",
                f,
                file_name="report.pdf",
                mime="application/pdf"
            )

