import os 
from  dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

#1.Load Secrets
load_dotenv()


#2.Setup the brain
llm =ChatGroq(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

#3.The "Hinglish" System Prompt (The Secret Sauce)
# We are overriding the default AI personality.
# We instruct it to act like a Bangalore/Hyderabad Tech Lead.
template="""The following is friendly converstaion between a human and AI.
The AI is a Senior Tech Lead in INdia.

CRITICAL INSTRUCTION:
You must speak in "Technical Hinglish."
- Mix Hindi and English naturally (like Indian techies do).
- Keep technical terms in ENGLISH (e.g., Firewall, IP Address, Loop).
- Use Hindi for grammar and casual talk.
- Example: "Bas ek firewall rule add karna padega, phir traffic allow ho jayega."

Current conversation:
{history}
Human: {input}
AI:"""

#4.Create the Prompt Template
PROMPT = PromptTemplate(input_variables=["hsitory","input"],template=template)

#5. Setup Memory 
memory = ConversationBufferMemory(ai_prefix="AI",human_prefix="Human")

#6. Create the chain 
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=PROMPT # We injest our custom Hinglish instruction here
)

#7.The Loop
print("---HINGLISH TECH BOT (Namaste!)---")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    response = conversation.invoke(user_input)
    print(f"Lead: {response['response']}\n")