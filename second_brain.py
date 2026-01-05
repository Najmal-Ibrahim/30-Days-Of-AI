import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# 1. Setup
load_dotenv()
DB_PATH = "chroma_db"

# 2. Load the Brain from Disk
print("--- LOADING SECOND BRAIN ---")
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_db = Chroma(
    persist_directory=DB_PATH, 
    embedding_function=embedding_function
)
print("✅ Brain Loaded.")

# 3. Setup LLM
llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# 4. Chat Loop
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_db.as_retriever(search_kwargs={"k": 3}), # Find top 3 matches
    return_source_documents=True
)

print("\n🤖 I have read your 'my_knowledge' folder. Ask me anything!")
print("Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
        
    result = qa_chain.invoke({"query": query})
    print(f"AI: {result['result']}")
    
    # Show sources (Proves it read your specific files)
    source = result['source_documents'][0].metadata['source']
    print(f"[Source: {source}]\n")