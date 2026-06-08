import os
import pdfplumber
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Initialize Embedding Model 
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="unofficial_guide")

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()

def process_documents(docs_dir="documents"):
    print("Starting document ingestion...")
    
    # Chunking 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=["\n\n", "\n", " ", ""]
    )

    all_chunks = []
    all_metadatas = []
    all_ids = []
    chunk_id_counter = 0

    if not os.path.exists(docs_dir):
        print(f"Error: Directory '{docs_dir}' not found. Create it and add your files.")
        return

    for filename in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, filename)
        raw_text = ""
        
        if filename.endswith(".pdf"):
            raw_text = extract_text_from_pdf(file_path)
        elif filename.endswith(".txt"):
            raw_text = extract_text_from_txt(file_path)
        else:
            continue # Skip non text/pdf files

        if not raw_text.strip():
            continue

        # Clean text (normalize whitespace)
        clean_text = " ".join(raw_text.split())

        chunks = text_splitter.split_text(clean_text)
        
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadatas.append({"source": filename})
            all_ids.append(f"chunk_{chunk_id_counter}")
            chunk_id_counter += 1

    print(f"Created {len(all_chunks)} chunks. Embedding and storing in ChromaDB...")
    
    # Store in Vector Database
    if all_chunks:
        embeddings = embedding_model.encode(all_chunks).tolist()
        collection.add(
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas,
            ids=all_ids
        )
        print("Vector database populated successfully!")
    else:
        print("No chunks generated. Check your documents directory.")

if __name__ == "__main__":
    process_documents()