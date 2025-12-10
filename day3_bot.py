import os
from dotenv import load_dotenv
from groq import Groq

#1. Load the secret password
load_dotenv()

#2. Setup the Client(the phone)

client=Groq(api_key=os.environ.get("GROQ_API_KEY"),)

#3. Conversation Loop

print("--- STARTING NEURAL LINK ---")
print("Model=Llama-3-8b(via Groq)")
print("Type 'Exit' to quit.\n")

while True:
    #A. Get the input from the user.
    user_input=input("You: ")

    # Check for exit
    if user_input.lower()=="exit":
        print("Disconnecting")
        break
    #B .Send to the brain(The API call)
    # This is the most important part of the code.
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a sarcastic AI assistant. You give short, funny answers."
            },
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama-3.3-70b-versatile", # The specific brain we are using
    )

    # C. Extract the Answer
    # The API returns a big messy JSON object. We just want the text.
    bot_reply = chat_completion.choices[0].message.content
    
    # D. Print it
    print(f"AI:  {bot_reply}\n")