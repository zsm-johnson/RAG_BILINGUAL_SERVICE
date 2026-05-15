import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer

VECTOR_STORE_PATH = "vector_store.npy"
METADATA_STORE_PATH = "metadata.json"
embed_model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
vectors = []
metadata = []

def load_vector_db():
    global vectors,metadata
    if os.path.exists(VECTOR_STORE_PATH):
        vectors = np.load(VECTOR_STORE_PATH,allow_pickle=True).tolist()
    if os.path.exists(METADATA_STORE_PATH):
        with open(METADATA_STORE_PATH,"r",encoding="utf-8") as f:
            metadata = json.load(f)

def save_vector_db():
    np.save(VECTOR_STORE_PATH,np.array(vectors))
    with open(METADATA_STORE_PATH,"w",encoding="utf-8") as f:
        json.dump(metadata,f,ensure_ascii=False,indent=2)

def add_document(text:str,source:str):
    if len(text.strip())<10:return
    vec = embed_model.encode(text,normalize_embeddings=True).tolist()
    vectors.append(vec)
    metadata.append({"content":text,"source":source})

def search_vector(query:str,top_k=5):
    if len(vectors)==0:return []
    qv = embed_model.encode(query,normalize_embeddings=True)
    scores = np.dot(vectors,qv)
    idx = np.argsort(scores)[::-1][:top_k]
    return [{"text":metadata[i]["content"],"score":float(scores[i]),"source":metadata[i]["source"]} for i in idx]

def search_keyword(query:str,top_k=5):
    res = []
    for item in metadata:
        if query in item["content"]:
            res.append({"text":item["content"],"score":0.7})
    return res[:top_k]