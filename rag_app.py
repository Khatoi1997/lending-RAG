import chromadb
import ollama

# 1. Connect to our local vector database
chroma_client = chromadb.PersistentClient(path="./lending_vector_db")
collection = chroma_client.get_collection(name="loan_policies")

# 2. Accept a question from the user
user_query = "What happens if a borrower has a DTI of 45%?"
print(f"❓ User Question: {user_query}")
print("🔍 Searching database for internal policy rules...")

# 3. Retrieve the top relevant document chunk
db_results = collection.query(
    query_texts=[user_query],
    n_results=1
)
context_document = db_results['documents'][0][0]

print("📄 Found matching policy context. Feeding data to local Llama 3.2...")

# 4. Construct a strict prompt template for the AI
# This forces the model to act like a banking compliance underwriter 
# and relies exclusively on the document we retrieved.
prompt = f"""
You are a professional credit risk manager at JP Morgan Chase. 
Answer the user's question accurately using only the internal policy context provided below. 
If the answer cannot be found in the context, say "I cannot find the answer in our official guidelines."

Internal Policy Context:
\"\"\"
{context_document}
\"\"\"

User Question: {user_query}

Helpful Professional Answer:
"""

# 5. Send the compiled prompt to our local Ollama instance
response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

# 6. Display the final answer
print("\n🤖 Final Underwriter AI Response:")
print("=" * 50)
print(response["message"]["content"])
print("=" * 50)