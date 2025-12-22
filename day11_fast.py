import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
#NEW IMPORT:Window Memory(The short_term memory)
from langchain.memory import ConversationBufferWindowMemory

#1.Load Secrets
load_dotenv()

#2.setup the brain
llm=ChatGroq(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

#3.Setup a OPTIMIZED memory
#k=3 means:"Only remember the last 3 exchanges."
#It forgets anything older than that.this keeps the bot FAST forever.
memory=ConversationBufferWindowMemory(k=3)

#4.Create a Chain
conversation =ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False  # Turn off internal logs so we see our own logs
)

#5.The loop with Token Counting
print("---SPEED-OPTIMIZED BOT---")
print("I only remeber the last 3 things you said.")
print("Type 'exit' to quit.\n")

while True:
    user_input=input("You:")
    if user_input.lower()=="exit":
        break

    #Run the Chain
    response = conversation.invoke(user_input)

    #6.CALCULATE AND PRINT TOKENS(The Engineering part)
    #Note: Groq's raw response object is hidden in LangChain, 
    # so we estimate using simple math or access the raw llm if needed.
    # Here, we will inspect the memory size.
    
    # Get the current history text
    history_buffer = memory.buffer_as_str
    estimated_tokens = len(history_buffer) / 4 # Rough estimate (4 chars ~ 1 token)
    
    print(f"AI: {response['response']}")
    print(f"Stats: Memory contains approx {int(estimated_tokens)} tokens.")
    
    # Demonstration of forgetting
    buffer_len = len(memory.buffer) # Number of messages in memory
    print(f"Stats: Storing last {buffer_len // 2} conversation turns.")
    print("-" * 30)