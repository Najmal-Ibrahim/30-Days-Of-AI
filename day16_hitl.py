import os
from dotenv import load_dotenv
from typing import TypedDict,Literal
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,END

#1.Load Secrets
load_dotenv()
llm=ChatGroq(api_key=os.environ.get("GROQ_API_KEY"),model="llama-3.3-70b-versatile")

#2.Define State
class FinanceState(TypedDict):
    request:str 
    amount:int
    status:str
    reason:str

# 3. Define Nodes

def analyze_request(state: FinanceState):
    """Extracts the amount from the text."""
    print("--- NODE 1: ANALYZING REQUEST ---")
    request = state["request"]
    
    # We ask LLM to extract the number
    prompt = f"Extract the dollar amount from this text: '{request}'. Return ONLY the number (integer). No text."
    try:
        amount_str = llm.invoke(prompt).content.strip()
        # Clean up string to ensure it's a number
        amount = int(''.join(filter(str.isdigit, amount_str)))
    except:
        amount = 0 # Default if fails
        
    print(f"    [Analysis]: User wants to spend ${amount}")
    return {"amount": amount}

def human_approval_node(state: FinanceState):
    """The Human Guardrail. This pauses execution."""
    print("--- NODE 2: HUMAN REVIEW REQUIRED ---")
    amount = state["amount"]
    print(f"    ⚠️  ALERT: High value transaction detected (${amount}).")
    
    # Simulate the pause/input mechanism
    decision = input("    [HUMAN]: Approve this transaction? (yes/no): ").lower()
    
    if "yes" in decision:
        return {"status": "approved"}
    else:
        return {"status": "rejected"}

def execute_transaction(state: FinanceState):
    """Actually moves the money."""
    print("--- NODE 3: EXECUTING ---")
    return {"reason": "Transaction processed successfully."}

def reject_transaction(state: FinanceState):
    """Cancels the deal."""
    print("--- NODE 3: REJECTING ---")
    return {"reason": "Transaction blocked by Human Supervisor."}

# 4. Logic Gates (Conditional Edges)

def check_risk_level(state: FinanceState) -> Literal["safe", "risky"]:
    amount = state["amount"]
    if amount > 50:
        return "risky" # Go to Human
    else:
        return "safe"  # Go to Auto-Execute

def check_human_decision(state: FinanceState) -> Literal["proceed", "cancel"]:
    status = state["status"]
    if status == "approved":
        return "proceed"
    else:
        return "cancel"

# 5. Build the Graph
builder = StateGraph(FinanceState)

builder.add_node("analyst", analyze_request)
builder.add_node("human_supervisor", human_approval_node)
builder.add_node("execute", execute_transaction)
builder.add_node("reject", reject_transaction)

builder.set_entry_point("analyst")

# Logic A: After Analysis, check if it's risky
builder.add_conditional_edges(
    "analyst",
    check_risk_level,
    {
        "safe": "execute",
        "risky": "human_supervisor"
    }
)

# Logic B: After Human Review, check what they said
builder.add_conditional_edges(
    "human_supervisor",
    check_human_decision,
    {
        "proceed": "execute",
        "cancel": "reject"
    }
)

builder.add_edge("execute", END)
builder.add_edge("reject", END)

app = builder.compile()

# 6. Execution Loop
print("--- FINANCE BOT ONLINE ---")
print("Policy: Amounts over $50 require approval.\n")

while True:
    user_input = input("\nRequest (e.g., 'Buy a mouse for $20'): ")
    if user_input.lower() == "exit":
        break
        
    result = app.invoke({"request": user_input})
    print(f"FINAL RESULT: {result.get('reason', 'Done')}")