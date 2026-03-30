from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import process_sensor_data, generate_ai_response, execute_actions
from typing import Dict, Any

def create_agent_graph():
    """Create the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("process_sensor", process_sensor_data)
    workflow.add_node("generate_response", generate_ai_response)
    workflow.add_node("execute_actions", execute_actions)
    
    # Define edges
    workflow.set_entry_point("process_sensor")
    workflow.add_edge("process_sensor", "generate_response")
    workflow.add_edge("generate_response", "execute_actions")
    workflow.add_edge("execute_actions", END)
    
    return workflow.compile()

agent_graph = create_agent_graph()
