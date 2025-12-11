import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

#1. Load Secrets
load_dotenv()

#2. set up the brain
#Notice we are using LAngChain's wrapper now ,not the raw groq client
llm=ChatGroq(
    groq_api_key=os.environ.get("GROQ API KEY"),
     model_name="llama-3.3-70b-versatile"
)

#3. Setup the Memory
#this is the RAW buffer that stores the caht history
memory = ConversationBufferMemory()

#4. Create the "Chain" (Orchestartor)
#The Chain connects the Brain + the Memory

conversation=ConversationChain(
    llm=llm,
    memory=memory
)  

#5. Loop
print("--- CYBER-MENTOR WITH MEMORY ---")
print("I will remember what you said.")
print("Type 'exit' to quit.\n")

while True:
    user_input=input("You:")

    if user_input.lower()=="exit":
        break

    #Run the Chain
    #The chain handles all the context automatically
    response = conversation.invoke(user_input)

    #Print the result
    print(f"Ai:{response['response']}\n")