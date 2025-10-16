import os
import datetime
import logging
from dotenv import load_dotenv

# --- Import Pydantic Schemas ---
from schema import AnswerQuestion, ReviseAnswer, Reflection

# --- LangChain Core ---
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

# --- Groq LLM ---
from langchain_groq import ChatGroq

# --- Load environment variables ---
load_dotenv()
logging.basicConfig(level=logging.INFO)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "Reflexion agents of chain"

if not GROQ_API_KEY:
    logging.error("GROQ_API_KEY environment variable not found.")
    raise ValueError("GROQ_API_KEY must be set.")

logging.info("✅ Environment keys loaded.")

# --- LLM Configuration ---
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

# --- Output Parsers ---
pydantic_parser_answer = PydanticToolsParser(tools=[AnswerQuestion])
pydantic_parser_revise = PydanticToolsParser(tools=[ReviseAnswer])

# --- Prompt Template ---
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1–3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat()
)

# --- First Responder Chain ---
first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer."
)

first_responder_chain = (
    first_responder_prompt_template
    | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion')
    | pydantic_parser_answer
)

# --- Revisor Instructions ---
revise_instructions = """Revise your previous answer using the new information.

- Add missing information based on your previous reflection.
- Remove superfluous content to keep the answer concise.
- Your revised answer must be strictly under 250 words.
- Include numerical citations in the text of the answer (e.g., [1], [2]).
- In the 'references' field, include a list of links that match those citations. You may format them as:
    - '[1] https://example.com'
    - or just 'https://example.com'
- Do not include any new search queries. The 'search_queries' list MUST be empty.
"""

# --- Revisor Chain ---
revisor_chain = (
    actor_prompt_template.partial(first_instruction=revise_instructions)
    | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")
    | pydantic_parser_revise
)

# --- Helper Function ---
def get_first_tool_output(parsed_output, expected_type):
    if isinstance(parsed_output, list):
        for item in parsed_output:
            if isinstance(item, expected_type):
                return item
        raise TypeError(f"No instance of {expected_type.__name__} found in list.")
    elif isinstance(parsed_output, expected_type):
        return parsed_output
    else:
        raise TypeError(f"Expected {expected_type.__name__}, got {type(parsed_output)}")

# --- Main Chain Execution (Runs Immediately) ---
question = "Explain the concept of RAG (Retrieval-Augmented Generation) and its primary benefit over a standard LLM."

try:
    logging.info("-" * 70)
    logging.info(f"INVOKING FIRST RESPONDER for question: '{question[:50]}...'")
    logging.info("-" * 70)

    # Step 1: Initial answer
    first_output = first_responder_chain.invoke({
        "messages": [HumanMessage(content=question)]
    })

    initial_answer_obj = get_first_tool_output(first_output, AnswerQuestion)

    logging.info("\n✅ SUCCESS: First Responder Output (AnswerQuestion)")
    logging.info("-" * 70)
    logging.info(f"ANSWER:\n{initial_answer_obj.answer}\n")
    logging.info(f"REFLECTION - Missing:\n{initial_answer_obj.reflection.missing}")
    logging.info(f"REFLECTION - Superfluous:\n{initial_answer_obj.reflection.superfluous}")
    logging.info(f"SEARCH QUERIES: {initial_answer_obj.search_queries}")
    logging.info("-" * 70)

    # Step 2: Revision
    logging.info(f"\n🔄 INVOKING REVISOR CHAIN for revision...")
    revision_output = revisor_chain.invoke({
        "messages": [HumanMessage(content=question)]
    })

    revised_answer_obj = get_first_tool_output(revision_output, ReviseAnswer)

    logging.info("\n✅ SUCCESS: Revised Answer Output (ReviseAnswer)")
    logging.info("-" * 70)
    logging.info(f"REVISED ANSWER:\n{revised_answer_obj.answer}\n")
    logging.info(f"REFLECTION:\nMissing: {revised_answer_obj.reflection.missing}")
    logging.info(f"Superfluous: {revised_answer_obj.reflection.superfluous}")
    logging.info(f"SEARCH QUERIES (should be empty): {revised_answer_obj.search_queries}")
    logging.info("REFERENCES:\n" + "\n".join(revised_answer_obj.references))
    logging.info("-" * 70)

except Exception as e:
    logging.error(f"\n❌ ERROR during chain invocation:\n{e}", exc_info=True)
