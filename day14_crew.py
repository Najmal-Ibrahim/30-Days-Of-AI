import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM # <--- Import LLM
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

# 1. Load Secrets
load_dotenv()

# CRITICAL FIX: Set a dummy OpenAI key to bypass the validation bug
os.environ["OPENAI_API_KEY"] = "NA"

# 2. Setup the Brain (The CrewAI Way)
# We use the "groq/" prefix so CrewAI knows which server to call.
my_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY")
)

# 3. DEFINE THE TOOL
class SearchTool(BaseTool):
    name: str = "Internet Search"
    description: str = "Useful to search the internet for current events."

    def _run(self, query: str) -> str:
        print(f"    (Agent is searching for: {query})...")
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
            return str(results)
        except Exception as e:
            return f"Error: {e}"

my_search_tool = SearchTool()

# 4. Define Agents
researcher = Agent(
    role='Senior Tech Researcher',
    goal='Uncover the latest breaking news in AI Cybersecurity',
    backstory="You are a veteran tech journalist. You only care about facts.",
    verbose=True,
    allow_delegation=False,
    tools=[my_search_tool],
    llm=my_llm # <--- Pass the new CrewAI LLM
)

writer = Agent(
    role='Tech Blog Writer',
    goal='Summarize tech news into a compelling LinkedIn post',
    backstory="You are a social media influencer. You use emojis.",
    verbose=True,
    allow_delegation=False,
    llm=my_llm # <--- Pass the new CrewAI LLM
)

# 5. Define Tasks
task1 = Task(
    description="Search for 'latest AI security breaches 2024 2025'. Find 2 specific examples.",
    agent=researcher,
    expected_output="A list of 2 recent AI security incidents with details."
)

task2 = Task(
    description="Write a short LinkedIn post about these breaches. Use bullet points.",
    agent=writer,
    expected_output="A LinkedIn post with emojis."
)

# 6. The Crew
tech_crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=True,
    process=Process.sequential
)

# 7. EXECUTION
print("--- KICKING OFF THE AI CREW ---")
result = tech_crew.kickoff()

print("\n\n########################")
print("## HERE IS THE RESULT ##")
print("########################\n")
print(result)