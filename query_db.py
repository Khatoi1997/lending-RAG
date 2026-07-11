import chromadb

# 1. Connect to our existing local database folder
chroma_client = chromadb.PersistentClient(path="./lending_vector_db")

# 2. Grab our 'loan_policies' collection
collection = chroma_client.get_collection(name="loan_policies")

# 3. Define the question you want to ask the database
user_query = "What is the maximum DTI ratio allowed for a mortgage?"
print(f"❓ Searching DB for: '{user_query}'\n")

# 4. Query the database for the top 1 closest match (n_results=1)
results = collection.query(
    query_texts=[user_query],
    n_results=1
)

# 5. Print out what the database found
retrieved_text = results['documents'][0][0]
print("🎯 Most Relevant Document Chunk Found:")
print("-" * 40)
print(retrieved_text)
print("-" * 40)