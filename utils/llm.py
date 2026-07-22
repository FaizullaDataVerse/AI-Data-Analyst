import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-2506",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.2,
)

def invoke_llm(prompt: str):
    response = llm.invoke(prompt)
    return response.content