import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode
from typing_extensions import TypedDict

from utils.tasks import read_tasks

load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Define our state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    userid: str

# Define our tool
@tool
def retrieve_tasks(userid: str) -> str:
    """
    Returns all the tasks for the user.
    """
    print(f"Retrieving tasks for userid: {userid}")  # Debug print
    tasks = read_tasks(userid)
    print(f"Tasks retrieved: {tasks}")  # Debug print
    return tasks

tools = [retrieve_tasks]

tool_node = ToolNode(tools)

# Define our agent node
def agent(state: State):
    llm = ChatGroq(api_key=GROK_API_KEY, model_name="deepseek-r1-distill-llama-70b").bind_tools(tools)
    system_message = SystemMessage(
        f"You are a helpful AI assistant. The user's id is {state['userid']}"
    )
    messages = [system_message] + state["messages"]
    return {"messages": [llm.invoke(messages)]}

# Define our graph
def create_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("agent", agent)
    graph_builder.add_node("executor", tool_node)
    graph_builder.add_edge(START, "agent")
    graph_builder.add_edge("agent", "executor")
    graph_builder.add_edge("executor", END)
    return graph_builder.compile()

# Our main function
def main():
    print(f"Current working directory: {os.getcwd()}")  # Debug print
    graph = create_graph()
    userid = "YourTechBud"
    query = input("Your query: ")
    initial_state = {"messages": [HumanMessage(content=query)], "userid": userid}
    for event in graph.stream(initial_state):
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["messages"][-1].content)

if __name__ == "__main__":
    main()