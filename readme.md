# DEEPSEEK AI Combinig PydanticAI WITH LangGraph


![alt text](<Screenshot 2025-03-11 233527.png>)



![alt text](<Screenshot 2025-03-11 233551.png>)


## 🚀 Overview
This project integrates **PydanticAI** with **LangGraph** to create a structured AI pipeline that efficiently processes user queries using a graph-based approach. The core workflow ensures seamless execution of AI agents with structured input validation using Pydantic models.

---

## 📌 Key Features
- **Graph-based AI pipeline** using LangGraph.
- **Pydantic validation** for structured input handling.
- **Seamless AI query execution** using `pydantic_agent.run_sync()`.
- **Custom tools integration** for task retrieval.
- **Clear debugging insights** with structured execution flow.

---

## 📜 Code Workflow (Step-by-Step Execution)
The execution follows a structured **step-by-step flow** to ensure clarity in how the data moves through the pipeline.

### 🟩 **Step 1: Script Execution Begins**
```python
if __name__ == "__main__":
    main()
```
✅ This ensures that `main()` is executed when running the script.

---

### 🟩 **Step 2: `main()` Function Execution**
```python
def main():
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
```
✅ Initializes the graph and user session.  
✅ Captures user input and starts the graph execution.

---

### 🟩 **Step 3: Graph Creation (`create_graph()`)**
```python
def create_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("agent", agent)
    graph_builder.add_edge(START, "agent")
    graph_builder.add_edge("agent", END)
    return graph_builder.compile()
```
✅ Defines the flow of execution in a directed graph.  
✅ Starts with the **`START`** node and ends at the **`END`** node.

---

### 🟩 **Step 4: Graph Execution Begins**
```python
for event in graph.stream(initial_state):
```
✅ The execution starts from the `START` node and follows the defined edges.

---

### 🟩 **Step 5: Agent Execution (`agent()`)**
```python
def agent(state: State):
    query = state["messages"][-1].content
    result = pydantic_agent.run_sync(query, deps=MyDeps(userid=state["userid"]))
    return {"messages": [AIMessage(content=result.data)]}
```
✅ Extracts the latest user query.  
✅ Calls the AI model using `pydantic_agent.run_sync()`.  
✅ Returns the AI-generated response wrapped in an `AIMessage` object.

---

### 🟩 **Step 6: AI Model Execution**
```python
pydantic_agent = Agent(
    model=groq_model,
    system_prompt="You are a helpful AI assistant",
    deps_type=MyDeps
)
```
✅ Uses **DeepSeek AI’s groq_model** for processing queries.  
✅ Structures the response using Pydantic.

---

### 🟩 **Step 7: Custom Tool Execution (if needed)**
```python
@pydantic_agent.tool
def get_tasks(ctx: RunContext[MyDeps]) -> str:
    return read_tasks(ctx.deps.userid)
```
✅ Fetches user-specific tasks when required.  
✅ Ensures structured tool execution using `@pydantic_agent.tool` decorator.

---

### 🟩 **Step 8: Displaying the Output**
```python
for key in event:
    print(event[key]["messages"][-1].content)
```
✅ Outputs the AI-generated response in a structured format.

---

## 🔄 **Complete Workflow Diagram**
```
Script Execution
      ↓
main()
      ↓
create_graph()
      ↓
Graph Initialization
      ↓
START → agent() → END
      ↓
agent()
      ↓
pydantic_agent.run_sync()
      ↓
groq_model (deepseek-r1-distill-llama-70b)
      ↓
Model Generates Response
      ↓
agent() Returns Response
      ↓
Response Displayed in Console
```

---

## ✅ Summary
✔ **Graph-based execution** using LangGraph.  
✔ **Pydantic-powered AI agent** for structured data processing.  
✔ **AI model integration** via DeepSeek AI (groq_model).  
✔ **Custom tool execution** for task retrieval.  
✔ **Seamless debugging** with structured workflow.

---

## 🛠 **Debugging Tips**
- Use `print()` statements to trace execution at key points:
  ```python
  print("Checkpoint 1:", data)
  ```
- Ensure files are in the expected locations using:
  ```python
  import os
  print("Looking for:", os.path.abspath("utils/data/YourTechBud.json"))
  ```
- Use PowerShell to locate misplaced files:
  ```powershell
  Get-ChildItem -Path . -Recurse | Select-String "YourTechBud.json"
  ```

---

## 📸 **Final Project Output**
![Final Output](<Screenshot 2025-03-12 111849.png>)

Now that `YourTechBud.json` is correctly placed inside `LangGraph_and_pydanticAi/utils/data/`, the script works as expected! 🎯




Great! Now that you've placed `YourTechBud.json` inside `LangGraph_and_pydanticAi/utils/data/`, your script is able to locate it correctly. 🎯  

### **📌 Key Takeaways**
1. **Folder Structure Matters**:  
   - Initially, you created `data/` outside `LangGraph_and_pydanticAi`, so the script couldn't find it.
   - Moving it inside `utils/data/` resolved the issue.

2. **How to Avoid This Issue in the Future**
   - Always check where your script **expects** files to be.
   - If unsure, print the full file path before reading:
     ```python
     import os
     print("Looking for:", os.path.abspath("utils/data/YourTechBud.json"))
     ```
   - Use `Get-ChildItem -Path . -Recurse | Select-String "YourTechBud.json"` in PowerShell to find misplaced files.

Now that it's working, what's next? Are you adding more functionality? 🚀




