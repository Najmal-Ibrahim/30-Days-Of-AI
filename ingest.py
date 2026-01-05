import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Setup
load_dotenv()
DATA_PATH = "my_knowledge"
DB_PATH = "chroma_db"

def create_knowledge_base():
    print(f"--- INGESTING DATA FROM: {DATA_PATH} ---")
    
    # 2. Define Loaders with UTF-8 Encoding (THE FIX)
    # This prevents the crash when reading Emojis in your python files
    
    # PDF Loader
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    
    # Text/Code Loaders (Must use utf-8)
    txt_loader = DirectoryLoader(
        DATA_PATH, 
        glob="*.txt", 
        loader_cls=TextLoader, 
        loader_kwargs={"encoding": "utf-8"} 
    )
    
    py_loader = DirectoryLoader(
        DATA_PATH, 
        glob="*.py", 
        loader_cls=TextLoader, 
        loader_kwargs={"encoding": "utf-8"}
    )
    
    print("⏳ Loading files...")
    docs = []
    
    # Safe Loading: If one fails, it won't crash the whole script
    try:
        docs.extend(pdf_loader.load())
        print(f"   - PDFs loaded.")
    except Exception as e:
        print(f"   ⚠️ Could not load PDFs: {e}")

    try:
        docs.extend(txt_loader.load())
        print(f"   - Text files loaded.")
    except Exception as e:
        print(f"   ⚠️ Could not load Text files: {e}")

    try:
        docs.extend(py_loader.load())
        print(f"   - Python files loaded.")
    except Exception as e:
        print(f"   ⚠️ Could not load Python files: {e}")

    print(f"✅ Total Documents Loaded: {len(docs)}")

    if len(docs) == 0:
        print("❌ No documents found! Check your 'my_knowledge' folder.")
        return

    # 3. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    print(f"🧩 Split into {len(chunks)} chunks.")

    # 4. Save to Disk (ChromaDB)
    print("💾 Saving to Persistent Database (This may take a minute)...")
    
    # Delete old DB to avoid duplicates
    if os.path.exists(DB_PATH):
        import shutil
        try:
            shutil.rmtree(DB_PATH)
            print("   - Cleared old database.")
        except:
            print("   - Could not clear old DB (might be in use). Continuing...")

    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_function, 
        persist_directory=DB_PATH
    )
    
    print(f"🎉 SUCCESS! Brain saved to '{DB_PATH}'.")

if __name__ == "__main__":
    create_knowledge_base()