import sys
print(f"Using Python: {sys.executable}")

print("\n--- ATTEMPTING IMPORTS ---")

try:
    from langchain.chains import ConversationChain
    print("✅ SUCCESS: langchain.chains found")
except ImportError as e:
    print(f"❌ FAIL: langchain.chains missing ({e})")

try:
    from langchain.memory import ConversationBufferMemory
    print("✅ SUCCESS: langchain.memory found")
except ImportError as e:
    print(f"❌ FAIL: langchain.memory missing ({e})")

print("\n--- DIAGNOSTIC COMPLETE ---")