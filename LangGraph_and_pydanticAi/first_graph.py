import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

load_dotenv()
GROK_API_KEY=os.getenv("GROK_API_KEY")



# Define our state
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


# Define our first node
def first_node(state: State):
    # Create a langchain model
    llm = ChatGroq(api_key=GROK_API_KEY, model_name="Gemma2-9b-It")

    # Define a system message
    system_message = SystemMessage("You are a helpful AI assistant.")

    # Define the messages
    messages = [system_message] + state["messages"]

    # Invoke the model
    return {"messages": [llm.invoke(messages)]}


# Define our graph
def create_graph():
    graph_builder = StateGraph(State)

    # Add all the nodes
    graph_builder.add_node("first_node", first_node)

    # Add the edges
    graph_builder.add_edge(START, "first_node")
    graph_builder.add_edge("first_node", END)

    return graph_builder.compile()


# Our main function
def main():
    graph = create_graph()

    query = input("Your query: ")

    initial_state = {"messages": [HumanMessage(content=query)]}

    for event in graph.stream(initial_state):
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["messages"][-1].content)


if __name__ == "__main__":
    main()