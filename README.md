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
## Tech Stack
- **Languages:** Python
- **Libraries:** PyTorch, LangChain, Hugging Face
- **Hardware:** Local RTX 1080 + Cloud Compute

[def]: day3_bot_output.png