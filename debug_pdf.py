from langchain_community.document_loaders import PyPDFLoader

print("Testing PDF readability...")
loader = PyPDFLoader("data.pdf")
pages = loader.load()

# Print the text of the first page
first_page_text = pages[0].page_content
print(f"--- START OF PAGE 1 ---")
print(first_page_text)
print(f"--- END OF PAGE 1 ---")

if len(first_page_text.strip()) == 0:
    print("\n[DIAGNOSIS]: The PDF is an IMAGE. Python cannot read it.")
else:
    print("\n[DIAGNOSIS]: The PDF has text. Something else is wrong.")