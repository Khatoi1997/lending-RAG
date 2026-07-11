import chromadb
from langchain_text_splitters import CharacterTextSplitter

print("📖 Reading the loan policy document...")

# 1. Load the text file
with open("sample_loan_policy.txt", "r") as file:
    document_text = file.read()

# 2. Split the text into chunks
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=200,
    chunk_overlap=50
)
chunks = text_splitter.split_text(document_text)
print(f"✂️ Split document into {len(chunks)} chunks.")

# 3. Initialize ChromaDB (Persistent local storage)
# This will automatically create a folder named 'lending_vector_db' in your project directory
chroma_client = chromadb.PersistentClient(path="./lending_vector_db")

# 4. Create a database "collection" (similar to a table in standard databases)
# If it already exists, get it; otherwise, create a new one.
collection = chroma_client.get_or_create_collection(name="loan_policies")

# 5. Add the chunks to our database
# ChromaDB requires a unique ID string for each entry, and the text data
ids = [f"policy_chunk_{i}" for i in range(len(chunks))]

print("⚙️ Generatating mathematical embeddings and saving to ChromaDB...")
collection.add(
    documents=chunks,
    ids=ids
)

print("🎉 Success! Your chunks are permanently stored in your local Vector DB.")