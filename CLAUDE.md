# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

Enterprise AI Analytics Platform — uploads a CSV, runs a multi-agent LangGraph pipeline, and produces AI-generated insights, KPIs, an executive summary, and BI-ready exports (SQLite, CSV, PDF).

## Running the App

```bash
pip install -r requirements.txt
streamlit run app.py          # opens at http://localhost:8501
```

Requires `GROQ_API_KEY` in `.env`.

## Architecture

The app follows a strict separation across four layers:

**`graph/analytics_graph.py`** — defines the LangGraph `StateGraph` and wires nodes together. This is the single place that controls execution order. All agent nodes receive and return `AnalyticsState` (a `TypedDict`).

**`agents/`** — one file per agent; each agent is a pure function `(state: AnalyticsState) -> dict` that returns partial state updates:
- `eda_agent.py` — pure Python stats (shape, missing %, correlations); no LLM
- `kpi_agent.py` — time-series KPIs with `pct_change()`; no LLM
- `insight_agent.py` — calls Groq (LLaMA 3.1) to produce bullet-point business insights from EDA output
- `executive_agent.py` — calls Groq to produce a non-technical 4-6 bullet executive summary from insights + KPIs
- `sql_agent.py` — NL-to-SQL via Groq; **not wired into the graph yet**

**`core/`** — shared utilities:
- `llm.py` — single `llm(prompt, task)` entry point for all Groq calls; dispatches `max_tokens` by task type (`"insight"`, `"executive"`, `"sql"`)
- `db.py` — `write_table(df, table_name)` writes to `analytics.db` (SQLite)
- `pdf.py` — `generate_pdf(summary, path)` writes `exports/reports/report.pdf` via ReportLab

**`app.py`** — Streamlit UI: file upload → column selection → `analytics_graph.invoke(state)` → display + save outputs (SQLite, `fact_kpis.csv`, PDF download).

### State flow

```
                    ┌── Insight node ──┐
CSV upload → EDA ───┤                  ├── Executive node → save to DB/CSV/PDF
                    └── KPI node ──────┘
```

After EDA, `insight` and `kpi` nodes run **in parallel** (both have edges from `eda`); `executive` waits for both before running.

`AnalyticsState` fields: `df`, `date`, `value`, `eda`, `insights`, `kpis`, `summary`.

## LLM Configuration

All LLM calls go through `core/llm.py`. Model is `llama-3.1-8b-instant` via Groq at `temperature=0.2`. To swap models or add a new task type, edit only `core/llm.py`.

## BI Exports

- **SQLite** (`analytics.db`, table `fact_kpis`) — connect directly from Power BI/Tableau
- **CSV** (`fact_kpis.csv`) — flat export of KPI DataFrame
- **PDF** (`exports/reports/report.pdf`) — ReportLab-generated executive report
