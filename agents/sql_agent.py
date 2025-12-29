from core.llm import llm

def nl_to_sql(schema: str, question: str) -> str:
    prompt = f"""
You are a senior data analyst.

Rules:
- Generate ONLY SQL
- ONLY SELECT queries
- NO DELETE, UPDATE, INSERT, DROP
- Use only the schema provided
- PostgreSQL dialect

Schema:
{schema}

Question:
{question}
"""
    return llm(prompt)
