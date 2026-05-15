from fastapi import FastAPI
from rag_engine import rag
from file_initializer import init_knowledge_base
from vector_db import load_vector_db

app = FastAPI(title="RAG + Generative AI Service",version="3.0")

@app.on_event("startup")
def startup():
    load_vector_db()
    init_knowledge_base()

@app.get("/qa")
def qa(query:str):
    return rag(query)

@app.get("/health")
def health():
    return {"status":"ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)