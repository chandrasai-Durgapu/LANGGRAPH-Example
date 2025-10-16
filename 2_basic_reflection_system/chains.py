from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
import os
import logging
from dotenv import load_dotenv

load_dotenv()

generation_prompt=ChatPromptTemplate(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."

            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


logging.basicConfig(
        level=logging.INFO
    )
    
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
GROQ_API_KEY=os.environ["GROQ_API_KEY"]
logging.info("loaded Environment keys")
llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                api_key=GROQ_API_KEY
            )

generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm