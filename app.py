import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
 
#1.Page Setup 
st.set_page_config(page_title="DocuChat AI",page_icon="📄")
st.title("📄 DocuChat: Chat with your PDF")

#2.Load Secrets
load_dotenv()
groq_api_key=os.environ.get("GROQ_API_KEY")

#3.Sidebar - Settings and Upload
with st.sidebar:
    st.header("Upload Document")
    uploaded_file=st.file_uploader("Upload a PDF",type="pdf")

    st.markdown("---")
    st.write("Powered by **Llama-3** and **Groq**")

#4.Initialize Session State(Memory fro the web app)
if "message" not in st.session_state:
    st.session_state.messages =[]#Store chat history
if "vector_db" not in st.session_state:
    st.session_state.vector_db=None#Store the brain

#5.The Logic (Cached to run fast)
@st.cache_resource
def setup_vector_db(file_path):
    #this runs only when a new file is uploaded
    st.write("⚙️ Processing Document...")

    #Load
    loader=PyPDFLoader(file_path)
    docs=loader.load()

    #Split
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    splits=text_splitter.split_documents(docs)

    #Embed
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
    vector_db =FAISS.from_documents(splits,embeddings)
    return vector_db

# 6. Handle File Upload
if uploaded_file is not None:
    # Save file temporarily so PyPDFLoader can read it
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Build Database (Only once)
    if st.session_state.vector_db is None:
        with st.spinner("Analyzing PDF..."):
            st.session_state.vector_db = setup_vector_db("temp.pdf")
        st.success("PDF Loaded! Ask away.")

# 7. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Handle User Input
prompt = st.chat_input("Ask a question about your PDF...")

if prompt:
    # A. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Generate AI Response
    if st.session_state.vector_db is not None:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Setup LLM
                llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
                
                # Setup Chain
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=st.session_state.vector_db.as_retriever()
                )
                
                # Get Answer
                response = qa_chain.invoke({"query": prompt})
                answer = response['result']
                
                st.markdown(answer)
        
        # Save AI Message
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        st.error("Please upload a PDF first!")