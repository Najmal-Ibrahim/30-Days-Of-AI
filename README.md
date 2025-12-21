# 30 Days of AI Engineering

# 🚀 Zero to AI Engineer in 30 Days
**Author:** Najmal Ibrahim
**Focus:** LLMs, RAG, and Multilingual AI Agents (Hindi/English).
**Goal:** Building production-grade AI systems with limited hardware (RTX 1080) by optimizing for efficiency.

This repository documents my intensive journey from beginner to AI Engineer, following a roadmap tailored for LLMs, RAG, and Multilingual Agents.

## Progress
- [x] Day 1: Python Data Engineering & Environment Setup
- [x] Day 2: Math for AI & Transformers
- Training Result: Achieved 0.005 Loss on TensorFlow Spiral dataset using Sine features.
### Day 2: Neural Networks & Math
- **Concept:** Mastered Vector Embeddings and Dot Products.
- **Experiment:** Trained a Neural Network on the TensorFlow Spiral dataset.
- **Result:** Achieved **0.005 Test Loss** using Sine feature engineering.
- **Visual Proof:**
![Spiral Training Result](spiral_result.png)
## 🧠 Key Concepts Learned

### Vector Embeddings
Converting words into lists of numbers (coordinates) so machines can understand their meaning. 
*Example:* `King` and `Man` have similar vector directions, while `King` and `Apple` are far apart.

### The Dot Product
A mathematical calculation to measure similarity between two vectors.
- High Score = High Similarity (e.g., Question & Answer).
- Low Score = No Relation.
- *Application:* This is the core engine behind RAG (Chat with PDF).
- [x] Day 3: API Integration
### Day 3: Building the AI Wrapper (LLM Integration)
**Goal:** Build a Python client interacting with Llama-3-70b via API.

- **Tech Stack:** Python, Groq API, `python-dotenv`.
- **Key Concepts:**
  - **API Engineering:** Connected local Python script to cloud LLM inference.
  - **Prompt Engineering:** Used "System Prompts" to define specific personas (Cybersecurity Mentor).
  - **Security:** Implemented `.env` for safe API key management (preventing credential leaks).
- **Outcome:** A functional CLI Chatbot that explains complex security concepts (SQL Injection, XSS) with code examples.
**Terminal Output:**
![Day 3 Chatbot Demo][day3_bot_output.png]

### Day 4: LangChain Orchestration & Memory
**Goal:** Solved the "Amnesia" problem (statelessness) by implementing short-term memory.

- **Tech Stack:** `LangChain Community`, `ConversationBufferMemory`, `Groq`, Python 3.11.
- **Challenge:** Fixed a critical version conflict (Python 3.14 vs 3.11) by restructuring the Virtual Environment.
- **Outcome:** The AI now retains context across multiple conversation turns.

**Terminal Output (Proof of Memory):**
> *User: "My name is Najmal."*
> *... (conversation continues) ...*
> *User: "What is my name?"*
> *AI: "Your name is Najmal."*

![LangChain Memory Output](day4_memory_output.png)

### Day 5: RAG (Retrieval Augmented Generation) System
**Goal:** Build a system that answers questions based on a specific PDF document (Private Knowledge Base).

- **Tech Stack:** `pypdf` (Loading), `sentence-transformers` (Embeddings), `FAISS` (Vector Database), `Llama-3` (Reasoning).
- **Architecture:** 
  1. Ingest PDF -> Chunk Text (1000 chars).
  2. Embed Chunks -> Store in FAISS.
  3. User Query -> Semantic Search -> Retrieve Top Chunks.
  4. Generate Answer using Llama-3 + Retrieved Context.
- **Outcome:** Successfully queried a Cloud Computing/Cyber Law document with accurate citations.
**Terminal Output (Proof of RAG):**
> *Query: "What is cloud computing"*
> *Response: "According to the text, cloud computing allows computer users to conveniently rent access..."*

![RAG System Output](day5_rag_output.png)

### Day 6: Multilingual "Hinglish" Tech Support Bot
**Goal:** Engineer an LLM to speak naturally in "Hinglish" (Hindi + English) for Indian technical contexts.

- **Tech Stack:** Llama-3-70b, LangChain Prompt Templates.
- **Key Skill:** **Advanced Prompt Engineering** (Persona Injection).
- **Outcome:** The bot successfully mixes Hindi grammar with English technical terminology (e.g., "SQL Injection", "Infinite Loop") to simulate a native Indian Tech Lead.

**Terminal Output:**
> *User: "Sir, mere code mein infinite loop aa raha hai..."*
> *AI: "Arre, infinite loop ka issue hai toh pehle humein uss loop ki condition check karni padegi..."*

![Hinglish Bot Output][day6_hinglish_output.png]

### Day 7: Multimodal Voice Assistant
**Goal:** Build a "Jarvis-like" voice interface that listens and speaks.

- **Tech Stack:** 
  - **Ears:** `SpeechRecognition` + Google STT API.
  - **Brain:** Llama-3-70b (Groq).
  - **Mouth:** `gTTS` (Google Text-to-Speech) with Indian English accent.
- **Outcome:** A hands-free voice assistant that processes speech input and responds with synthesized audio.

**Terminal Output:**
> *Microphone: "Who created Python?"*
> *AI (Audio): "Python was created by Guido van Rossum in 1991."*

![Voice AI Log](day7_voice_output.png)

### Day 8: Autonomous AI Agent (ReAct Pattern)
**Goal:** Build an agent that can use external tools (Web Search) to answer real-time questions.

- **Tech Stack:** LangChain `AgentExecutor`, `DuckDuckGoSearchRun`, Llama-3-70b.
- **Key Concept:** **ReAct (Reason + Act)**. The AI autonomously decided to search again when the first query failed.
- **Outcome:** The Agent successfully retrieved the live Bitcoin price ($86,843) by self-correcting its search strategy.

**Terminal Output (Showing Reasoning Trace):**
> *Thought: "The search results didn't provide the current price... I should try again."*
> *Action: Search "bitcoin price today"*
> *Observation: "$86,843.18 USD"*

![Agent ReAct Log](day8_agent_output.png)

### Day 9: "DocuChat" - Full Stack RAG Application
**Goal:** Build a production-grade Web UI for the RAG system to replace the terminal interface.

- **Tech Stack:** `Streamlit` (Frontend), `LangChain` (Logic), `FAISS` (Vector Store).
- **Features:** 
  - Drag-and-drop PDF upload.
  - Real-time caching (Vector DB builds only once per file).
  - Session State management for chat history.
- **Outcome:** A functional web app where users can chat with technical documents (Cloud Computing / Cyber Law) in a browser.

**Web Interface Demo:**
![Streamlit App](day9_ui_demo.png)

### 🚀 Day 10: Cloud Deployment
**Goal:** Deploy the RAG application to the public web using CI/CD principles.

- **Platform:** Hugging Face Spaces (Cloud).
- **Tech:** Docker/Streamlit configuration, Dependency Management (requirements.txt).
- **Outcome:** The app is live and accessible globally.

🔴 **LIVE DEMO:** [Click here to use DocuChat AI](https://huggingface.co/spaces/Najmalibrahim/docuchat-ai)


## Tech Stack
- **Languages:** Python
- **Libraries:** PyTorch, LangChain, Hugging Face
- **Hardware:** Local RTX 1080 + Cloud Compute


