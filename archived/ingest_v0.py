from langchain_text_splitters import CharacterTextSplitter

print("📖 Reading the loan policy document...")

# 1. Load the text file we just created
with open("sample_loan_policy.txt", "r") as file:
    document_text = file.read()

# 2. Define our chunking strategy
# We want chunks of around 200 characters, with a small 50-character overlap 
# so sentences don't get awkwardly cut in half at the boundaries.
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=200,
    chunk_overlap=50
)

# 3. Perform the split
chunks = text_splitter.split_text(document_text)

# 4. Print out our processed chunks to see how the backend structured them
print(f"✅ Document successfully split into {len(chunks)} chunks!\n")

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
    print("-" * 20)


