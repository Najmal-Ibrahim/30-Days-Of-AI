import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage

# 1. Load Secrets
load_dotenv()

# 2. Setup the Brain with STREAMING enabled
# 'streaming=True' tells Groq to send data in pieces.
# 'callbacks=[...]' tells Python what to do with those pieces (print them immediately).
chat = ChatGroq(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.7
)

# 3. The Test
print("--- STREAMING DEMO ---")
print("Ask a question that requires a LONG answer (e.g., 'Write a poem about rust').")
print("Notice how the text appears immediately.\n")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break
    
    print("AI: ", end="", flush=True)
    
    # 4. Invoke
    # We don't need 'print(response)' because the CallbackHandler 
    # is already printing directly to the terminal!
    chat.invoke([HumanMessage(content=user_input)])
    print("") # Newline after finishing