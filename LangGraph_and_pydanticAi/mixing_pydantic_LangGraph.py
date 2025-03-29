import operator
import os
from typing import Annotated
import json

import yaml
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic_ai.models.groq import GroqModel
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from typing_extensions import TypedDict

from agents.task_manager import TaskManagementDeps, task_management_agent

load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Define our overall state
class OverallState(TypedDict):
    # Confidential stuff
    userid: str

    # Other stuff
    query: str
    tasks: list[str]
    enriched_tasks: Annotated[list, operator.add]
    output: str


# Define our task enrichment state
class TaskEnrichmentState(TypedDict):
    task: str


import re  # For regex-based extraction

def task_manager(state: OverallState):
    result = task_management_agent.run_sync(
        state["query"], deps=TaskManagementDeps(userid=state["userid"])
    )
    print("Raw result data:", result.data)

    def parse_markdown_tasks(data):
        # Extract task details using regex
        pattern = r"- \*\*Title:\*\* (.+?)\n\s+\*\*Due Date:\*\* (.+?)\n\s+\*\*Priority:\*\* (.+)"
        matches = re.findall(pattern, data)

        # Convert matched data into task format
        tasks = [{"title": title, "due_date": due, "priority": priority} for title, due, priority in matches]
        return tasks

    try:
        tasks_raw = parse_markdown_tasks(result.data)
        tasks = [task["title"] for task in tasks_raw]
    except Exception as e:
        print(f"Error parsing tasks: {e}")
        tasks = []  # Default to empty list if parsing fails

    print("Tasks:")
    print(tasks)

    return {"tasks": tasks}



# Define our task enrichment node
def task_enricher(state: TaskEnrichmentState):
    # Create a langchain model
    llm=ChatGroq(api_key=GROK_API_KEY, model_name="deepseek-r1-distill-llama-70b")

    # Define a system message
    system_message = SystemMessage(
        "You are a helpful AI assistant. You are given a task and you need to enrich it with helpful quotes to motivate the user to complete it. Keep it short and concise."
    )

    # Define the messages
    messages = [
        system_message,
        HumanMessage(content=(f"Here's the task: {state['task']}")),
    ]

    # Invoke the model
    result = llm.invoke(messages).content
    print("Enriched task:")
    print(result)
    return {"enriched_tasks": [result]}


# Define our task formatter node
def task_formatter(state: OverallState):
    llm=ChatGroq(api_key=GROK_API_KEY, model_name="deepseek-r1-distill-llama-70b")

    # Define a system message
    system_message = SystemMessage(
        "You are a helpful AI assistant. You are given a list of tasks and you need to return a well formatted list."
    )

    # Create a string of the tasks
    tasks_str = "---\n".join(state["enriched_tasks"])

    # Define the messages
    messages = [
        system_message,
        HumanMessage(content=f"Here's the list of tasks:\n{tasks_str}"),
    ]

    result = llm.invoke(messages).content
    print("Formatted tasks:")
    print(result)
    return {"output": result}


# Here we define the logic to map out each task to an enricher
# This will be an edge in the graph
def map_tasks_to_enricher(state: OverallState):
    # We will return a list of `Send` objects
    # Each `Send` object will have a `node` and `state`
    # The `node` will be the node to send the message to
    # The `state` will be the state to send to the node
    return [
        Send(node="task_enricher", arg=TaskEnrichmentState(task=task))
        for task in state["tasks"]
    ]


# Define our graph
def create_graph():
    graph_builder = StateGraph(OverallState)

    # Add all the nodes
    graph_builder.add_node("task_manager", task_manager)
    graph_builder.add_node("task_enricher", task_enricher)
    graph_builder.add_node("task_formatter", task_formatter)

    # Add the edges
    graph_builder.add_edge(START, "task_manager")
    graph_builder.add_conditional_edges(
        "task_manager", map_tasks_to_enricher, ["task_enricher"]
    )
    graph_builder.add_edge("task_enricher", "task_formatter")
    graph_builder.add_edge("task_formatter", END)

    return graph_builder.compile()


# Our main function
def main():
    graph = create_graph()

    # Confidential stuff
    userid = "YourTechBud"

    query = input("Your query: ")

    initial_state = {"query": query, "userid": userid}

    for event in graph.stream(initial_state):
        for key in event:
            print("-----------------------------------")
            print("Done with " + key)
            print("\n*******************************************\n")


if __name__ == "__main__":
    main()