import sqlite3

import pandas as pd
import streamlit as st

from agents.sql_agent import nl_to_sql
from core.db import write_table
from core.pdf import generate_pdf
from core.sql_safety import validate_select_only
from graph.analytics_graph import analytics_graph

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
        state = analytics_graph.invoke({
            "df": df.sort_values(by=date_col),
            "date": date_col,
            "value": value_col
        })
        st.session_state["analytics_state"] = state

        st.subheader("Insights")
        st.write(state["insights"])

        st.subheader("Executive Summary")
        st.write(state["summary"])

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

    if "analytics_state" in st.session_state:
        kpis_df = st.session_state["analytics_state"]["kpis"]

        st.divider()
        st.subheader("Query your data with SQL")

        question = st.text_input("Ask a natural-language question about your data")

        if st.button("Submit", key="sql_submit") and question:
            schema_lines = ["Table: fact_kpis", "Columns:"]
            for col, dtype in kpis_df.dtypes.items():
                schema_lines.append(f"  - {col} ({dtype})")
            schema = "\n".join(schema_lines)

            sql = nl_to_sql(schema, question)
            st.code(sql, language="sql")

            ok, reason = validate_select_only(sql)
            if not ok:
                st.error(f"Query rejected: {reason}")
            else:
                try:
                    conn = sqlite3.connect("analytics.db")
                    result = pd.read_sql_query(sql, conn)
                    conn.close()
                    st.dataframe(result)
                except Exception as e:
                    st.error(f"Query failed: {e}")

