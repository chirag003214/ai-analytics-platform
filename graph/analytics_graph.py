from typing import TypedDict
from langgraph.graph import StateGraph

from agents.eda_agent import eda_agent
from agents.insight_agent import insight_agent
from agents.kpi_agent import kpi_agent
from agents.executive_agent import executive_agent

class AnalyticsState(TypedDict):
    df: object
    date: str
    value: str
    eda: dict
    insights: str
    kpis: object
    summary: str

graph = StateGraph(AnalyticsState)

def eda_node(state):
    return {"eda": eda_agent(state["df"])}

def insight_node(state):
    return {"insights": insight_agent(state["eda"])}

def kpi_node(state):
    return {"kpis": kpi_agent(state["df"], state["date"], state["value"])}

def executive_node(state):
    return {"summary": executive_agent(state["insights"], state["kpis"])}

graph.add_node("eda", eda_node)
graph.add_node("insight", insight_node)
graph.add_node("kpi", kpi_node)
graph.add_node("executive", executive_node)

graph.set_entry_point("eda")
graph.add_edge("eda", "insight")
graph.add_edge("eda", "kpi")
graph.add_edge("insight", "executive")
graph.add_edge("kpi", "executive")

analytics_graph = graph.compile()


