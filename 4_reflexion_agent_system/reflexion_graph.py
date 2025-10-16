from typing import List
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langgraph.graph import END, MessageGraph
import json
import os

from chains import revisor_chain, first_responder_chain
from execute_tools import execute_tools

# ✅ FIXED: Properly handle tool output (which is a list)
def wrap_as_ai_message(pydantic_obj):
    if isinstance(pydantic_obj, list):
        if not pydantic_obj:
            raise ValueError("Tool output list is empty.")
        pydantic_obj = pydantic_obj[0]
    return [AIMessage(content=json.dumps(pydantic_obj.model_dump()))]

# Init
os.environ["LANGCHAIN_PROJECT"] = "Reflexion graph"
graph = MessageGraph()
MAX_ITERATIONS = 2

# Nodes
graph.add_node("draft", lambda state: wrap_as_ai_message(first_responder_chain.invoke({"messages": state})))
graph.add_node("execute_tools", execute_tools)
graph.add_node("revisor", lambda state: wrap_as_ai_message(revisor_chain.invoke({"messages": state})))

# Edges
graph.add_edge("draft", "execute_tools")
graph.add_edge("execute_tools", "revisor")

# Loop controller
def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    return END if count_tool_visits > MAX_ITERATIONS else "execute_tools"

graph.add_conditional_edges("revisor", event_loop)
graph.set_entry_point("draft")

# Compile
app = graph.compile()
print(app.get_graph().draw_mermaid())

# Run
response = app.invoke("Write about how small business can leverage AI to grow")

# Parse final output
if isinstance(response[-1], AIMessage):
    data = json.loads(response[-1].content)
    print("\n✅ Final Answer:")
    print(data.get("answer", "No answer found"))
else:
    print("❌ Final output not AIMessage:", type(response[-1]))
