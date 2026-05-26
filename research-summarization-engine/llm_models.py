from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv() #A
openai_api_key = os.getenv("OPENAI_API_KEY") #B

def get_llm(): #C
    return ChatOpenAI(model_name="gpt-5-nano")