import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import load_tools,initialize_agent,AgentType
from langchain_community.tools import DuckDuckGoSearchRun

#1.Load Secreats
load_dotenv()

#2.Setup the brain(LLM)
#We use temprature of 0 because we need facts ,not creativity
llm=ChatGroq(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# 3. Setup the Tools (The "Hands")
# We give the AI a search engine.
search_tool = DuckDuckGoSearchRun()

# We wrap it in a list of tools
tools = [
    # We define a custom tool wrapper manually to ensure clarity
    search_tool
]

#4.Create the agent
#ZERO_SHOT_DESCRIPTION means:
#"Look at the tool descriptions and decide which one to use based on the questions"
print("---INITIALIZING AGENT 007---")
agent=initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,#CRITICAL:This lets us see the AI's "THOUGHTS"
    handle_parsing_errors=True
)

#5.Loop
print("---AGENT READY(I can search the web!)---")
print("Ask about the current events(e.g,'Price of Bitcoin','Who won the match yesterday').")
print("Type 'exit' to quit.\n")

while True:
    user_input=input("You:")
    if user_input.lower()=="exit":
        break

    #Run the agent
    try:
        response=agent.run(user_input)
        print(f"Agent:{response}\n")
    except Exception as e:
         print(f"Error:{e}")
