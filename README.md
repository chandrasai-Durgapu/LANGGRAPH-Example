# LANGNGRAPH-Example
# 🤖 LangGraph-Example: Reflective AI Agent Workflows with LangGraph

This project showcases how to build **modular, intelligent, and reflective agent systems** using [LangGraph](https://github.com/langchain-ai/langgraph). It includes working examples of **multi-step reasoning**, **structured outputs**, and **feedback loops**, all within a graph-based programming paradigm tailored for large language models (LLMs).

> 🔍 Designed to demonstrate advanced agent-based architecture using LangGraph and LangChain for AI experimentation, reasoning, and control.

---

## 📌 Why This Project?

Modern LLM agents need more than a single prompt—they need to **reflect**, **retry**, and **reason across steps**. LangGraph enables this by letting you define logic as a **stateful computation graph** with support for branching, memory, and looping.

This repo:
- Demonstrates **hands-on patterns** like reflexion agents, feedback cycles, and modular graph design.
- Is built to be a **learning-friendly playground** for AI agents and graph-based workflows.



---
## 🛠️ Tech Stack

🧠 LangGraph
 – graph-based LLM workflows

🔗 LangChain
 – LLM orchestration framework

🐍 Python 3.10+

📦 Pydantic, dotenv, other Python ecosystem tools
---
## 🧠 Key Features

### 🧩 Modular Design with LangGraph
- Graph-based agent logic for composability
- Custom nodes and edges for agent control flow
- Reflection-enabled subgraphs for improved reasoning

### 🔁 Reflexion Agents
- Implements agents that can **self-evaluate**, **re-plan**, and **retry**
- Inspired by research on LLM self-correction and feedback loops

### 📝 Structured Outputs
- Uses `pydantic`, `langchain.output_parsers`, etc. for schema-constrained outputs
- Teaches LLMs to output well-structured JSON or Python objects

### 🔍 Interactive Workflows
- Step-by-step flow in Jupyter / Python scripts
- Logs and prints at each step to observe reasoning and flow

### 📚 Learning-Friendly
- Each sub-folder is self-contained and well-commented
- Easy to run and extend even for LangGraph beginners

---


## 🚀 Installation & Setup
Clone the repo:
   ```bash
   git clone https://github.com/chandrasai-Durgapu/LANGGRAPH-Example.git
   cd LANGGRAPH-Example
   ```
## Create Virtual Environment
```bash
python -m venv py-001
```

## Activate Virtual Environment
```bash
py-001\Scripts\activate
```

## Install Dependencies
```bash
pip install -r requirements.txt
```
---
## 🧠 Key Concepts Explained

This section introduces the advanced agent concepts used throughout the LangGraph-Example project. These ideas power the modular, intelligent, and self-correcting workflows implemented using LangGraph.

## 🔄 React Agent (Reasoning + Acting)

A React Agent is an LLM-based agent that combines reasoning and acting in a loop:

Thinks step-by-step through a problem

Chooses actions or tools based on intermediate results

Repeats until a final answer is produced

This mirrors how humans might ask a question, use tools (e.g., search), and build toward an answer.

🧠 Example: Think → Search → Think → Calculate → Answer

LangGraph lets you define this as a graph, where nodes represent reasoning and tool use.

...run the react_agent_basic
```bash
python 1_Introduction/react_agent_basic.py
```
 ---
## 🪞 Reflection Agent (Reflection Chain System)

A Reflection Agent is an LLM agent that evaluates its own output and decides whether to retry, revise, or continue. This is part of a broader Reflection Chain System, where:

The agent generates an answer

Then it reflects: “Was this good?”

Based on feedback, it may:

Accept the output

Retry with improvements

Rewrite the input or strategy

🧪 Inspired by academic work like "ReAct meets Reflexion" and self-evaluation loops

LangGraph supports this by allowing feedback loops in the graph. This turns your agent from a "one-shot" generator into a self-improving loop.

....run the basic reflection chain system
```bash
python 2_basic_reflection_system/basic.py
```
---
## 📦 Structured Output in LangGraph

By default, LLMs return freeform text. But in real-world apps, we often need structured data (e.g., JSON, key-value pairs, or schemas). LangGraph supports structured outputs by:

Using tools like pydantic or LangChain's OutputParser

Validating that LLM responses conform to a schema

Handling parsing or fallback logic if structure fails

🔧 Example: Extracting country info like {"name": "name of the country", "language": "language of the country", "capital": "capital of the country"} from unstructured input..... and the expected output is {"name": India, "language": "hindi", "capital": "delhi"}

Structured output is critical for:

Interfacing with APIs

Feeding data into databases

Ensuring predictable downstream processing

...run the structure output with country types content 
```bash
python 3_structured_outputs/country_types.py
```
---


...run the reflexion agent of chains
```bash
python 4_reflexion_agent_system/chains.py
```
---
## 🧠 Reflexion Agent

The Reflexion Agent extends the Reflection Agent by introducing memory and longer-term learning.

Tracks past attempts and learns what worked

Improves performance over multiple runs

Can be used in multi-turn problem solving or simulations

🧠 “Don’t just fix this answer — learn how to avoid the mistake next time.”

In this project, the Reflexion Agent uses LangGraph to track:

What actions were taken

How the output was rated

What should be done differently next time
---
## 🔁 Reflexion Graph

A Reflexion Graph is a LangGraph-powered agent system that combines:

Reasoning

Acting

Reflection

Retry logic

Memory

...into a graph-based execution model.

Rather than using a simple sequence of prompts, it uses nodes and edges to dynamically decide:

Which node to visit next

Whether to retry, revise, or move on

How to remember past performance

This lets you build resilient and intelligent AI agents that learn from their mistakes and adapt in real-time.

...run the reflexion graph
```bash
python 4_reflexion_agent_system/reflexion_graph.py
```
---



