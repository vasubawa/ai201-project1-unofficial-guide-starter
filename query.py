import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="unofficial_guide")

def retrieve_chunks(query, top_k=3):
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    documents = results.get('documents')
    metadatas = results.get('metadatas')
    distances = results.get('distances')
    
    if documents is None or len(documents) == 0 or documents[0] is None:
        return []

    chunks = documents[0]
    chunk_metadatas = metadatas[0] if metadatas is not None and len(metadatas) > 0 else []
    chunk_distances = distances[0] if distances is not None and len(distances) > 0 else []
    
    retrieved_data = []
    for i in range(len(chunks)):
        source = "Unknown"
        if i < len(chunk_metadatas) and chunk_metadatas[i] is not None:
            source = chunk_metadatas[i].get('source', 'Unknown')
            
        dist = chunk_distances[i] if i < len(chunk_distances) else 0.0
        
        retrieved_data.append({
            "text": chunks[i],
            "source": source,
            "distance": dist
        })
        
    return retrieved_data

def ask(question):
    retrieved_data = retrieve_chunks(question, top_k=3) 
    
    # Handle empty retrieval
    if not retrieved_data:
        return {
            "answer": "I don't have enough information on that in the provided documents.",
            "sources": []
        }

    context_texts = []
    sources = set()
    
    for item in retrieved_data:
        context_texts.append(f"Source: {item['source']}\nContent: {item['text']}")
        sources.add(item['source'])

    context_block = "\n\n---\n\n".join(context_texts)

    # Prompt
    prompt = f"""You are a helpful assistant for the UCF Foundation Exam Study Companion. 
    Answer the user's question using ONLY the information in the provided context below.
    If the documents do not contain enough information to answer the question, explicitly state "I don't have enough information on that."
    Do NOT use your general knowledge. Include source citations in your response (e.g., "According to [Source Name]...").

    Context:
    {context_block}

    Question: {question}
    Answer:"""

    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a strict RAG bot that only answers using the provided documents."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.1 
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": list(sources)
    }
    
if __name__ == "__main__":
    
    q1 = "What is the official passing mark for the Foundation Exam?"
    print(f"User: {q1}")
    res1 = ask(q1)
    print(f"Answer:\n{res1['answer']}\n")
    print(f"Sources: {res1['sources']}\n")
    print("-" * 50)
    
    q2 = "What is the best place to get pizza near the UCF campus?"
    print(f"User: {q2}")
    res2 = ask(q2)
    print(f"Answer:\n{res2['answer']}\n")
    print(f"Sources: {res2['sources']}\n")