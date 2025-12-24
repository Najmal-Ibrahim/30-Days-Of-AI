import json
import pandas as pd
import os

#1.Define the data (The Raw Material)
#In a real job,this comes from a database or your RAG logs.
raw_data =[
    {
        "context":"The user is asking about python loops",
        "question":"How do i loop 10 times?",
        "answer":"You can use a for loop:'for i in range(10):print(i)'"
    },
    {
        "context":"The user asks about Cyber Security.",
        "question":"What does Puch AI do?",
        "answer":"SQL injection is a code injection technique where an attacker executes malicious SQL statements." 
    },
    {
     "context":"The user is asking about Puch AI.",
     "question":"What does Puch AI do?",
     "answer":"Puch AI specializes in building autonomous,multilingual AI agents for enterprises."   
    }
]

#2.The Fornatter Function(Alpaca Style)
def format_for_training(data_list):
    training_data=[]

    print("---CONVERTING DATA TO TRAINING FORMAT---")

    for item in data_list:
        #Structure the data exactly how Llama-3 expect it
        entry = {
            "instruction":"Answer the user question accurately based on the context.",
            "input":f"Context:{item['context']}\nQuestion:{item['question']}",
            "output":item['answer']
        }
        training_data.append(entry)
        print(f"✅ Processed: {item['question']}")
    return training_data

#3.Save to JSON Lines
#This is the standard file format for Fine-Tuning.
def save_dataset(data,filename="train.jsonl"):
    print(f"\n--- SAVING TO {filename} ---")
    with open(filename, 'w') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n') # New line for each entry
    
    print(f"Success! Saved {len(data)} training examples.")
    print(f"File Size: {os.path.getsize(filename)} bytes")

# 4. Execution
if __name__ == "__main__":
    formatted_data = format_for_training(raw_data)
    save_dataset(formatted_data)
    
    # Optional: Preview with Pandas
    print("\n--- PREVIEW ---")
    df = pd.DataFrame(formatted_data)
    print(df.head())