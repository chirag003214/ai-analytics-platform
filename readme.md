# Enterprise AI Analytics Platform

An end-to-end AI-powered analytics system that transforms raw datasets into
actionable insights and executive-ready dashboards.

## 🚀 Features

- Automated Exploratory Data Analysis (EDA)
- AI-assisted insight generation (Groq + LLaMA)
- KPI computation with growth metrics
- Multi-agent orchestration using LangGraph
- Executive summary generation
- Export to CSV / SQLite for BI tools
- Power BI & Tableau dashboard integration
- Streamlit interactive UI

## 🧠 Architecture

Data → EDA Agent → Insight Agent → KPI Agent → Executive Agent
↓
CSV / SQLite Output
↓
Power BI / Tableau

markdown
Copy code

## 🛠️ Tech Stack

- Python, Pandas, NumPy
- Streamlit
- LangGraph (multi-agent orchestration)
- Groq API (LLaMA 3.1 models)
- SQLite / CSV (BI-ready outputs)
- Power BI / Tableau

## 📊 Dashboards

The system exports analytics-ready tables (`fact_kpis.csv`) that can be
directly connected to Power BI or Tableau for executive dashboards.

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py