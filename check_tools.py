print("Checking your Inventory...")

try:
    # Day 4 & 6: Memory
    from langchain.memory import ConversationBufferMemory
    print("✅ Memory: INSTALLED")

    # Day 5: Chains & Splitters
    from langchain.chains import RetrievalQA
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✅ Chains & Splitters: INSTALLED")

    # Day 12: Schema & Youtube
    from langchain_core.messages import HumanMessage
    from langchain_community.document_loaders import YoutubeLoader
    print("✅ Schema & YouTube: INSTALLED")

    print("\n🎉 SUCCESS: You have every tool from Day 1 to Day 12.")

except ImportError as e:
    print(f"\n❌ MISSING: {e}")
    print("Run the pip install command again!")