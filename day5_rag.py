import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

#1 Load secrets
load_dotenv()

#2 Setup the LLM
llm=ChatGroq(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

#3 Load the PDF
print("--- 1. LOADING PDF ---")
loader=PyPDFLoader("data.pdf")
documents=loader.load()
print(f"Loaded{len(documents)}pages.")

#4. Split Text (The Chunking)
# We can't feed the whole book to AI. We cut it into small pieces.
print("--- 2. CHUNKING TEXT ---")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, # 1000 characters per chunk
    chunk_overlap=200 # Overlap to keep context between chunks
)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")

# 5. Embeddings (The Translator)
# This turns text into numbers so we can search it.
# We use a free, local model (MiniLM) running on your CPU.
print("--- 3. CREATING VECTOR STORE (This may take 10s) ---")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 6. Vector Store (The Database)
# We store the chunks in FAISS (Facebook AI Similarity Search)
vector_db = FAISS.from_documents(chunks, embeddings)

# 7. The Retrieval Chain (The Orchestrator)
# This connects: User Question -> Search DB -> Send best chunks to LLM -> Answer
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", # "Stuff" means: Stuff all found chunks into the prompt
    retriever=vector_db.as_retriever(),
    return_source_documents=True # Show us WHICH page the answer came from
)

# 8. The Loop
print("\n--- RAG SYSTEM READY ---")
print("Ask questions about your PDF. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    # Run the chain
    response = qa_chain.invoke({"query": user_input})
    
    # Print Answer
    print(f"AI: {response['result']}")
    
    # Print Source (Proof)
    source_page = response['source_documents'][0].metadata['page']
    print(f"[Source: Page {source_page + 1}]\n")