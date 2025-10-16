from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain.agents import initialize_agent, tool
from langchain_community.tools import TavilySearchResults
import datetime
import logging


try:
    logging.basicConfig(
        level=logging.INFO
    )
    load_dotenv()
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
    GROQ_API_KEY=os.environ["GROQ_API_KEY"]
    logging.info("loaded Environment keys")
    llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                api_key=GROQ_API_KEY
            )
    

    @tool
    def get_current_time(format:str="%Y-%m-%d")->str:
        """returns the current time and curent date in specified format"""
        try:
            logging.info("fetching current date and time")
            current_time=datetime.datetime.now()
            formatted_time=current_time.strftime(format)
            logging.info(f"sent the current date and time : {formatted_time}")
            return formatted_time
        except Exception as e:
            #print(e)
            logging.error("error occured",e)
            return ""
    search_tool=TavilySearchResults(search_depth="basic")
    tool=[search_tool,get_current_time]
    agent= initialize_agent(tools=tool,llm=llm, agent="zero-shot-react-description", verbose=True)
    agent.invoke("When was the last launch of ISRO rocket and how many days completed till now")
    #already executed agent.invoke() about weather
    #agent.invoke("Give me the serious tweet about weather in Hyderabad city")
    #basic step of creation with chain and invoke
    #result=llm.invoke("Give me information about Linkedin Chandra Sai Durgapu")

    #print(result.content)
    

except Exception as e:
    logging.error(e)    
