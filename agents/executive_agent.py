from core.llm import llm

def executive_agent(insights, kpis):
    prompt = f"""
Create an executive summary for leadership.

Guidelines:
- Non-technical
- Actionable
- 4–6 bullet points

Insights:
{insights}

KPI Snapshot:
{kpis.describe().to_string()}
"""
    return llm(prompt, task="executive")

