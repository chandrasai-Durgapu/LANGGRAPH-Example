from chains import generation_chain, reflection_chain
from typing import List, Sequence
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END, MessageGraph


graph=MessageGraph()

REFLECT = "reflect"
GENERATE = "generate"
graph = MessageGraph()

def generate_node(state):
    return generation_chain.invoke({
        "messages": state
    })

def reflect_node(messages):
    response = reflection_chain.invoke({
        "messages": messages
    })
    return [HumanMessage(content=response.content)]


graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)


def should_continue(state):
    if (len(state) > 6):
        return END 
    return REFLECT


graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()



#mermaid diagram of graph
print(app.get_graph().draw_mermaid())

#ascii diagram of graph
app.get_graph().print_ascii()


response = app.invoke(HumanMessage(content="AI Agents taking over content creation"))

print(response)
