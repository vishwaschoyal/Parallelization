import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph 
from typing import TypedDict

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="openai/gpt-oss-120b")

class State(TypedDict):
    topic:str
    characters:str
    settings:str

def create_character(state:State):
    response = llm.invoke(f"Create two characters name and brief traits for a story about {state['topic']}")
    return {"characters" : response.content}

def create_settings(state:State):
    response = llm.invoke(f"describe a vivid setting for a story about {state['topic']}")
    return {"settings" : response.content}    


graph = StateGraph(State)

graph.add_node("char",create_character)
graph.add_node("set",create_settings)

graph.add_edge(START,"char")
graph.add_edge(START,"set")
graph.add_edge("char",END)
graph.add_edge("set",END)

builder = graph.compile()

response = builder.invoke({"topic":"Neural network"})

print("Characters")
print(response["characters"])

print("Settings")
print(response["settings"])
