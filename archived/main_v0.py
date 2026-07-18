# first main.py to check if the rag application is working or not.

import chromadb
import ollama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. Initialize our FastAPI Application
app = FastAPI(
    title="JPMC Lending RAG API",
    description="A local backend server to query loan policies using AI.",
    version="1.0"
)

# 2. Connect to our existing local vector database once when the server starts
chroma_client = chromadb.PersistentClient(path="./lending_vector_db")
collection = chroma_client.get_collection(name="loan_policies")

# 3. Define the structure of the incoming request using Pydantic
# This ensures that whoever calls our API sends a valid text string
class QuestionRequest(BaseModel):
    question: str

# 4. Create our POST endpoint for querying the RAG application
@app.post("/ask")
def query_rag(request: QuestionRequest):
    user_query = request.question
    
    try:
        # Step A: Search the local database for matching rules
        db_results = collection.query(
            query_texts=[user_query],
            n_results=1
        )
        
        # Verify that we actually found data in the vector database
        if not db_results['documents'] or not db_results['documents'][0]:
            raise HTTPException(status_code=404, detail="No matching policy context found.")
            
        context_document = db_results['documents'][0][0]
        
        # Step B: Construct our strict prompt template
        prompt = f"""You are a professional credit risk manager at JP Morgan Chase. 
        Use the following policy rule to answer the question exactly.

        Policy Rule:
        {context_document}

        Question: {user_query}

        Answer:
        """
        
        # Step C: Generate the answer using our local Llama 3.2 engine
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Step D: Return a clean, structured JSON response
        return {
            "status": "success",
            "question": user_query,
            "answer": response["message"]["content"],
            "retrieved_context": context_document
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Root endpoint just to verify the server is alive
@app.get("/")
def read_root():
    return {"status": "online", "message": "JPMC Lending RAG backend is running."}