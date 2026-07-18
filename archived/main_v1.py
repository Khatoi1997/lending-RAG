# To pass multiple prompts or ask multiple questions at once

import chromadb
import ollama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# 1. Initialize our FastAPI Application
app = FastAPI(
    title="JPMC Lending RAG API - Batch Enabled",
    description="A local backend server to query loan policies with single or batch questions.",
    version="1.1"
)

# 2. Connect to our existing local vector database
chroma_client = chromadb.PersistentClient(path="./lending_vector_db")
collection = chroma_client.get_collection(name="loan_policies")

# --- Request Data Structures ---
class QuestionRequest(BaseModel):
    question: str

# New Pydantic structure to validate an array of questions
class BatchQuestionRequest(BaseModel):
    questions: List[str]


# --- API Endpoints ---

# 3. Existing Single Question Endpoint
@app.post("/ask")
def query_rag(request: QuestionRequest):
    user_query = request.question
    try:
        db_results = collection.query(query_texts=[user_query], n_results=1)
        if not db_results['documents'] or not db_results['documents'][0]:
            raise HTTPException(status_code=404, detail="No matching policy context found.")
            
        context_document = db_results['documents'][0][0]
        
        prompt = f"""You are a professional credit risk manager at JP Morgan Chase. 
Use the following policy rule to answer the question exactly.

Policy Rule:
{context_document}

Question: {user_query}

Answer:"""
        
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        
        return {
            "status": "success",
            "question": user_query,
            "answer": response["message"]["content"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 4. NEW: Scenario A Batch Processing Endpoint
@app.post("/ask-batch")
def query_rag_batch(request: BatchQuestionRequest):
    batch_results = []
    
    try:
        # Loop through each question in the array sequentially
        for idx, user_query in enumerate(request.questions):
            print(f"🔄 Processing batch item {idx + 1}/{len(request.questions)}: '{user_query}'")
            
            # Step A: Query database for this specific question
            db_results = collection.query(query_texts=[user_query], n_results=1)
            
            if not db_results['documents'] or not db_results['documents'][0]:
                context_document = "No policy context found for this query."
                answer = "I cannot find relevant guidelines to answer this query."
            else:
                context_document = db_results['documents'][0][0]
                
                # Step B: Build targeted prompt
                prompt = f"""You are a professional credit risk manager at JP Morgan Chase. 
Use the following policy rule to answer the question exactly.

Policy Rule:
{context_document}

Question: {user_query}

Answer:"""
                
                # Step C: Get response from local Llama
                response = ollama.chat(
                    model="llama3.2",
                    messages=[{"role": "user", "content": prompt}],
                )
                answer = response["message"]["content"]
            
            # Step D: Append the individual result to our array
            batch_results.append({
                "item_number": idx + 1,
                "question": user_query,
                "answer": answer,
                "retrieved_context": context_document
            })
            
        return {
            "status": "success",
            "total_processed": len(request.questions),
            "results": batch_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"status": "online", "message": "Batch RAG engine is ready."}