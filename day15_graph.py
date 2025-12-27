import os
from dotenv import load_dotenv
from typing import TypedDict,Literal
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,END

#1.Load Secrets
load_dotenv()
llm=ChatGroq(api_key=os.environ.get("GROQ_API_KEY"),model="llama-3.3-70b-versatile")

#2.Define The State
#This is the "Shared memory" that gets passed between nodes.
class AgentState(TypedDict):
    question:str
    category:str
    response:str

#3.Define the nodes(The Workers)

def categorize_node(state: AgentState):
        """Analyses the question and decides the category."""
        print("---NODE 1: CATEGORIZING ---")
        question = state ["question"]

        #Ask LLM to classify
        prompt=f"Categorize this request as either 'TECHNICAL' or 'BILLING'.Reply only with the word . Request:{question}"
        category=llm.invoke(prompt).content.strip().upper()

        #Update State
        return{"category":category}

def tech_support_node(state: AgentState):
    """Handles technical issues."""
    print("--- NODE 2: TECH SUPPORT ---")
    question = state["question"]
    response = llm.invoke(f"You are a Tech Support Engineer. Solve this: {question}").content
    return {"response": response}

def billing_node(state: AgentState):
    """Handles billing issues."""
    print("--- NODE 3: BILLING TEAM ---")
    question = state["question"]
    response = llm.invoke(f"You are a Finance Manager. Solve this: {question}").content
    return {"response": response}

# 4. Define the Routing Logic (The Conditional Edge)
def router_logic(state: AgentState) -> Literal["tech", "billing"]:
    category = state["category"]
    print(f"    [Router Logic]: Detected category is {category}")
    if "TECHNICAL" in category:
        return "tech"
    else:
        return "billing"
    
# 5. Build the Graph (The Flowchart)
builder = StateGraph(AgentState)

# Add Nodes
builder.add_node("categorizer", categorize_node)
builder.add_node("tech_support", tech_support_node)
builder.add_node("billing_dept", billing_node)

# Set Entry Point
builder.set_entry_point("categorizer")

# Add Conditional Edges
# "After categorizer, look at 'router_logic'. If it returns 'tech', go to 'tech_support'..."
builder.add_conditional_edges(
    "categorizer", 
    router_logic, 
    {
        "tech": "tech_support",
        "billing": "billing_dept"
    }
)

# Add Final Edges (Going to END)
builder.add_edge("tech_support", END)
builder.add_edge("billing_dept", END)

# Compile (Turn it into a runnable machine)
app = builder.compile()

# Test Case 1: Technical
query1 = "My computer screen turned blue and crashed."
print(f"\nUser: {query1}")
result = app.invoke({"question": query1})
print(f"Final Answer: {result['response']}")

# Test Case 2: Billing
query2 = "I was charged twice for my subscription."
print(f"\nUser: {query2}")
result = app.invoke({"question": query2})
print(f"Final Answer: {result['response']}")