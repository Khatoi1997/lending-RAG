import chromadb
import ollama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(
    title="JPMC Lending RAG API - Full Suite",
    description="A local backend server supporting single, batch, and conversational chat memory.",
    version="1.2"
)

chroma_client = chromadb.PersistentClient(path="./lending_vector_db")
collection = chroma_client.get_collection(name="loan_policies")

# In-memory chat history tracker
chat_histories: Dict[str, List[Dict[str, str]]] = {}

# --- Request Structures ---
class QuestionRequest(BaseModel):
    question: str

class BatchQuestionRequest(BaseModel):
    questions: List[str]

class ChatRequest(BaseModel):
    session_id: str
    question: str

# --- 1. Scenario B: Conversational Chat Endpoint ---
@app.post("/chat")
def conversational_chat(request: ChatRequest):
    session_id = request.session_id
    user_query = request.question
    
    if session_id not in chat_histories:
        chat_histories[session_id] = []
        
    try:
        db_results = collection.query(query_texts=[user_query], n_results=1)
        context_document = db_results['documents'][0][0] if db_results['documents'] and db_results['documents'][0] else "No explicit policy guidelines found."
            
        system_instruction = f"You are a professional credit risk manager at JP Morgan Chase. Answer the user's latest question accurately using only the internal policy rule provided below. If the answer cannot be found in the context or history, say 'I cannot find the answer in our official guidelines.'\n\nInternal Policy Rule:\n{context_document}"

        messages = [{"role": "system", "content": system_instruction}]
        messages.extend(chat_histories[session_id][-6:])
        messages.append({"role": "user", "content": user_query})
        
        response = ollama.chat(model="llama3.2", messages=messages)
        ai_answer = response["message"]["content"]
        
        chat_histories[session_id].append({"role": "user", "content": user_query})
        chat_histories[session_id].append({"role": "assistant", "content": ai_answer})
        
        return {
            "status": "success",
            "session_id": session_id,
            "answer": ai_answer,
            "retrieved_context": context_document
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 2. Single Question Endpoint ---
@app.post("/ask")
def query_rag(request: QuestionRequest):
    user_query = request.question
    try:
        db_results = collection.query(query_texts=[user_query], n_results=1)
        context_document = db_results['documents'][0][0]
        prompt = f"You are a professional credit risk manager at JP Morgan Chase. Use the following policy rule to answer the question exactly.\n\nPolicy Rule:\n{context_document}\n\nQuestion: {user_query}\n\nAnswer:"
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        return {"status": "success", "question": user_query, "answer": response["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. Scenario A: Batch Processing Endpoint ---
@app.post("/ask-batch")
def query_rag_batch(request: BatchQuestionRequest):
    batch_results = []
    try:
        for idx, user_query in enumerate(request.questions):
            db_results = collection.query(query_texts=[user_query], n_results=1)
            if not db_results['documents'] or not db_results['documents'][0]:
                context_document, answer = "No policy context found.", "I cannot find relevant guidelines."
            else:
                context_document = db_results['documents'][0][0]
                prompt = f"You are a professional credit risk manager at JP Morgan Chase. Use the following policy rule to answer the question exactly.\n\nPolicy Rule:\n{context_document}\n\nQuestion: {user_query}\n\nAnswer:"
                response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
                answer = response["message"]["content"]
            
            batch_results.append({"item_number": idx + 1, "question": user_query, "answer": answer, "retrieved_context": context_document})
        return {"status": "success", "total_processed": len(request.questions), "results": batch_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "online", "message": "All RAG engine modes are active."}