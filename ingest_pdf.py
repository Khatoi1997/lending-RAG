import os
import chromadb
from pypdf import PdfReader

# 1. Initialize the local persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./lending_vector_db")

# Get or create our loan policies collection
# We use get_or_create_collection so it doesn't crash if it already exists
collection = chroma_client.get_or_create_collection(name="loan_policies")

def extract_and_chunk_pdf(pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Reads a PDF, extracts text page by page, splits it into chunks with overlap,
    and uploads those chunks into ChromaDB.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found at {pdf_path}")
        return

    print(f"📖 Reading PDF: {pdf_path}...")
    reader = PdfReader(pdf_path)
    full_text = ""
    
    # Extract text from each page
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n[Page {page_num + 1}]\n" + text

    print(f"✂️ Splitting text into chunks (Size: {chunk_size}, Overlap: {chunk_overlap})...")
    
    # Simple semantic/character chunking strategy
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunks.append(full_text[start:end])
        start += chunk_size - chunk_overlap  # Move forward while keeping an overlap buffer

    print(f"📦 Uploading {len(chunks)} text chunks to ChromaDB...")
    
    # Prepare data arrays for ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for idx, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({"source": os.path.basename(pdf_path), "chunk_index": idx})
        ids.append(f"pdf_chunk_{idx}")
        
    # Upsert data into the database
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("✅ Ingestion complete! The database has been updated with the PDF content.")

if __name__ == "__main__":
    # Replace this with the actual name or path of your 10-page PDF file
    PDF_FILE_NAME = "loan_policy_document.pdf" 
    extract_and_chunk_pdf(PDF_FILE_NAME)