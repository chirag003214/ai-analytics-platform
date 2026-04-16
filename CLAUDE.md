# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

Enterprise AI Analytics Platform — uploads a CSV, runs a multi-agent LangGraph pipeline, and produces AI-generated insights, KPIs, an executive summary, and BI-ready exports (SQLite, CSV, PDF).

## Running the App

```bash
# Activate the local venv first (venv/ is committed to the repo root)
source venv/Scripts/activate    # Git Bash on Windows

pip install -r requirements.txt
streamlit run app.py            # opens at http://localhost:8501
```

Requires `GROQ_API_KEY` in `.env`.

## Architecture

The app follows a strict separation across four layers:

**`graph/analytics_graph.py`** — defines the LangGraph `StateGraph` and wires nodes together. This is the single place that controls execution order. All agent nodes receive and return `AnalyticsState` (a `TypedDict`).

**`agents/`** — one file per agent; each agent is a pure function that returns partial state updates:
- `eda_agent.py` — pure Python stats (shape, missing %, top-5 deduplicated correlations); no LLM
- `kpi_agent.py` — strips currency symbols (`₹`, commas) before `pd.to_numeric`, then computes `pct_change()`; no LLM
- `insight_agent.py` — calls Groq (LLaMA 3.1) to produce bullet-point business insights from EDA output
- `executive_agent.py` — calls Groq; receives `kpis.describe().to_string()` so `kpis` must be a numeric DataFrame
- `sql_agent.py` — `nl_to_sql(schema, question)` via Groq; **not wired into the graph**; generates PostgreSQL dialect even though the runtime DB is SQLite — reconcile this before wiring it in

**`core/`** — shared utilities:
- `llm.py` — single `llm(prompt, task)` entry point for all Groq calls; dispatches `max_tokens` by task type (`"insight"` → 400, `"executive"` → 600, `"sql"` → 300)
- `db.py` — `write_table(df, table_name)` writes to `analytics.db` (SQLite) with `if_exists="replace"` — each run overwrites the table
- `pdf.py` — `generate_pdf(summary, path)` auto-creates `exports/reports/` and writes via ReportLab

**`app.py`** — Streamlit UI: file upload → column selection → `analytics_graph.invoke(state)` → display + save outputs (SQLite, `fact_kpis.csv`, PDF download).

### State flow

```
                    ┌── insight node ──┐
CSV upload → EDA ───┤                  ├── executive node → save to DB/CSV/PDF
                    └── kpi node ──────┘
```

After EDA, `insight` and `kpi` nodes fan out (both have edges from `eda`); `executive` waits for both via fan-in before running.

`AnalyticsState` fields: `df`, `date`, `value`, `eda`, `insights`, `kpis`, `summary`.

## LLM Configuration

All LLM calls go through `core/llm.py`. Model is `llama-3.1-8b-instant` via Groq at `temperature=0.2`. To swap models or add a new task type, edit only `core/llm.py`.

## BI Exports

- **SQLite** (`analytics.db`, table `fact_kpis`) — connect directly from Power BI/Tableau
- **CSV** (`fact_kpis.csv`) — flat export of KPI DataFrame
- **PDF** (`exports/reports/report.pdf`) — ReportLab-generated executive report
