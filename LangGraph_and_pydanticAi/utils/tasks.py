import json
import os
from dataclasses import asdict, dataclass
import yaml

@dataclass
class Task:
    title: str
    isDone: bool = False

def get_data_file_path(userid: str) -> str:
    """Returns the absolute file path for the user's task data."""
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    data_dir = os.path.join(base_dir, "data")  # Ensure data directory is within the script directory
    os.makedirs(data_dir, exist_ok=True)  # Create data directory if not exists
    return os.path.join(data_dir, f"{userid}.json")  # Return absolute file path

def read_tasks(userid: str) -> str:
    """
    Reads all tasks from a JSON file and returns the result as a YAML string.

    Args:
        userid (str): The user ID whose tasks should be read.

    Returns:
        str: A YAML-formatted string of the tasks.
    """
    file_path = get_data_file_path(userid)
    print(f"Reading tasks from: {file_path}")  # Debug print

    if not os.path.exists(file_path):
        print("No tasks found")  # Debug print
        return "No tasks found"

    with open(file_path, "r") as file:
        tasks = json.load(file)
        print(f"Tasks loaded: {tasks}")  # Debug print

    return yaml.dump(tasks, sort_keys=False)

def mark_task_as_done(userid: str, title: str) -> str:
    """
    Marks a task as done by title and updates the JSON file.

    Args:
        userid (str): The user ID whose tasks should be updated.
        title (str): The title of the task to mark as done.

    Returns:
        str: A message indicating the task was successfully updated.

    Raises:
        FileNotFoundError: If the user's task file does not exist.
        ValueError: If no task with the given title is found.
    """
    file_path = get_data_file_path(userid)
    if not os.path.exists(file_path):
        raise FileNotFoundError("Task file not found.")

    with open(file_path, "r") as file:
        tasks = json.load(file)

    task_found = False
    for task in tasks:
        if task["title"] == title:
            task["isDone"] = True
            task_found = True
            break

    if not task_found:
        raise ValueError("Task with the given title not found.")

    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=2)

    return "Successfully updated task"

def add_task(userid: str, title: str) -> str:
    """
    Appends a new task to the task list and updates the JSON file.

    Args:
        userid (str): The user ID whose task list should be updated.
        title (str): The title of the new task to add.

    Returns:
        str: A message indicating the task was successfully added.

    Raises:
        ValueError: If a task with the same title already exists.
    """
    file_path = get_data_file_path(userid)
    tasks = []

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            tasks = json.load(file)

    for task in tasks:
        if task["title"] == title:
            raise ValueError("Task with the same title already exists.")

    new_task = Task(title=title)
    tasks.append(asdict(new_task))

    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=2)

    return "Successfully added task"
