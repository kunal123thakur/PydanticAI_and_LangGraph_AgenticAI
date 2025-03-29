# DEEPSEEK AI Combinig PydanticAI WITH LangGraph


![alt text](<Screenshot 2025-03-11 233527.png>)



![alt text](<Screenshot 2025-03-11 233551.png>)

### 🚀 **Code Workflow (Dry Run) — Step-by-Step Pipeline with Flow Diagram**

Let's walk through the entire code flow **step-by-step**, like a **debugger**, to understand **kaunsa block pehle chalega**, **kaunsa baad mein**, and how the **data flow** happens.

---

## 🟩 **Step 1: Script Execution Starts**
**Code Block:**
```python
if __name__ == "__main__":
    main()
```

### 🔎 **Explanation:**
- Jab aap `python .\Basic_read_pydantic_03.py` run karte ho, sabse pehle `if __name__ == "__main__":` execute hota hai.
- Yeh `main()` function ko call karega.

---

## 🟩 **Step 2: `main()` Function Execution**
**Code Block:**
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

### 🔎 **Explanation:**
✅ `create_graph()` call hota hai → Graph ka structure banega  
✅ `userid = "YourTechBud"` set hota hai  
✅ `query = input("Your query: ")` user se input leta hai  
✅ `initial_state` banega jo `messages` aur `userid` ko store karega  
✅ `graph.stream(initial_state)` run hoga jo graph ko flow start karne ka signal deta hai  

---

## 🟩 **Step 3: `create_graph()` Function Execution**
**Code Block:**
```python
def create_graph():
    graph_builder = StateGraph(State)

    # Add all the nodes
    graph_builder.add_node("agent", agent)
    # Add the edges
    graph_builder.add_edge(START, "agent")
    graph_builder.add_edge("agent", END)

    return graph_builder.compile()
```

### 🔎 **Explanation:**
✅ `StateGraph(State)` — Graph ka base structure banata hai  
✅ `"agent"` node ko add karta hai  
✅ `graph_builder.add_edge(START, "agent")` se flow start hota hai  
✅ `graph_builder.add_edge("agent", END)` se flow khatam hota hai  
✅ `graph_builder.compile()` se graph ready ho jata hai  

---

## 🟩 **Step 4: Graph Execution Begins**
**Code Block:**
```python
for event in graph.stream(initial_state):
```

### 🔎 **Explanation:**
✅ Graph ka **START** node activate hota hai  
✅ Control `"agent"` node pe jata hai  

---

## 🟩 **Step 5: `agent()` Function Execution**
**Code Block:**
```python
def agent(state: State):
    query = state["messages"][-1].content

    # Invoke the model
    result = pydantic_agent.run_sync(query, deps=MyDeps(userid=state["userid"]))
    return {"messages": [AIMessage(content=result.data)]}
```

### 🔎 **Explanation:**
✅ `state["messages"][-1].content` se user ka input (query) nikalta hai  
✅ `pydantic_agent.run_sync()` ko query pass hoti hai  
✅ `MyDeps(userid=state["userid"])` se user ID bhi pass hota hai  
✅ AI model response ko **`AIMessage`** format mein wrap karta hai  
✅ Yeh response `"messages"` field mein return hota hai  

---

## 🟩 **Step 6: `pydantic_agent.run_sync()` Execution**
**Code Block:**
```python
pydantic_agent = Agent(
    model=groq_model,
    system_prompt="You are a helpful AI assistant",
    deps_type=MyDeps
)
```

### 🔎 **Explanation:**
✅ `groq_model` ka instance AI model ko invoke karega  
✅ AI model ka response format hoke `result.data` mein store hoga  
✅ Yeh response `AIMessage` ke format mein `agent()` function ko return hoga  

---

## 🟩 **Step 7: Custom Tool Execution (if needed)**
**Code Block:**
```python
@pydantic_agent.tool
def get_tasks(ctx: RunContext[MyDeps]) -> str:
    return read_tasks(ctx.deps.userid)
```

### 🔎 **Explanation:**
✅ Agar AI assistant ko `get_tasks()` tool call karne ka instruction milega toh yeh function execute hoga  
✅ `read_tasks()` function se user ke tasks retrieve honge  

---

## 🟩 **Step 8: Output Display**
**Code Block:**
```python
for key in event:
    print(event[key]["messages"][-1].content)
```

### 🔎 **Explanation:**
✅ AI assistant ka response screen pe print hota hai  
✅ Har response ek separate block ke form mein display hota hai  

---

## 🔄 **Complete Workflow with Arrow Diagram**
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

## 🔥 **Summary of Code Flow**
✅ **`main()`** function se execution start hota hai  
✅ Graph ka structure banake `"agent"` node pe control jata hai  
✅ `agent()` function se AI model ko query bheji jaati hai  
✅ AI model ka response `"messages"` ke format mein wapas aata hai  
✅ Agar `get_tasks()` tool ka call hota hai toh yeh user ke tasks retrieve karta hai  
✅ Final response console pe print hota hai  

---

## 🤖 **Key Takeaways for Debugging**
✔️ Dry-run karte waqt **print statements** ka use karo taaki har step pe data ka flow track ho  
✔️ `print("Checkpoint 1:", data)` jaise prints se data ko debug karna easy ho jata hai  
✔️ Pipeline ka flow follow karte waqt **function call hierarchy** pe dhyan do  

Agar kisi part mein confusion ho toh bata dena, I'll break it down further. 😊


# Final project output
![alt text](<Screenshot 2025-03-12 111849.png>)


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




