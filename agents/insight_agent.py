from core.llm import llm
import json

def insight_agent(eda_report):
    stats = json.dumps(eda_report, indent=2)

    prompt = f"""
Generate concise business insights.
Rules:
- Use ONLY provided statistics
- No hallucination
- Bullet points only
- Max 6 bullets

Statistics:
{stats}
"""
    return llm(prompt, task="insight")


