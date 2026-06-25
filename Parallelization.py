import os
import sys
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph 
from typing import TypedDict

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="openai/gpt-oss-120b")

class State(TypedDict):
    topic: str
    characters: str
    settings: str

def create_character(state: State):
    try:
        response = llm.invoke(f"Create two characters name and brief traits for a story about {state['topic']}")
        return {"characters": response.content}
    except Exception as e:
        logging.error(f"Error creating characters: {str(e)}")
        return {"error": str(e)}

def create_settings(state: State):
    try:
        response = llm.invoke(f"describe a vivid setting for a story about {state['topic']}")
        return {"settings": response.content}
    except Exception as e:
        logging.error(f"Error creating settings: {str(e)}")
        return {"error": str(e)}

def main(topic: str):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the character and settings generation.")

    graph = StateGraph(State)

    graph.add_node("char", create_character)
    graph.add_node("set", create_settings)

    graph.add_edge(START, "char")
    graph.add_edge(START, "set")
    graph.add_edge("char", END)
    graph.add_edge("set", END)

    builder = graph.compile()

    response = builder.invoke({"topic": topic})

    print("Characters")
    print(response.get("characters", "Error generating characters"))

    print("Settings")
    print(response.get("settings", "Error generating settings"))

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Neural network"
    main(topic)
