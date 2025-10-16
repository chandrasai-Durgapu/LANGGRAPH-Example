from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import logging

load_dotenv()
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

class Country(BaseModel):
    """Information about country"""
    name: str=Field(description="name of the country")
    language: str=Field(description="language of the country")
    capital: str=Field(description="capital of the country")

structured_llm=llm.with_structured_output(Country)
response= structured_llm.invoke("Tell me about France")
print(response)
