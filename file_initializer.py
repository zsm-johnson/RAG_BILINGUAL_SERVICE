import os
from document_parser import extract_pdf_text,extract_image_text
from vector_db import add_document,load_vector_db,save_vector_db

KNOWLEDGE_FOLDER = "knowledge_files"
SUPPORTED_EXTS = [".pdf",".png",".jpg",".jpeg"]

def chunk_text(text:str,chunk_size=512,overlap=50):
    chunks=[]
    start=0
    while start<len(text):
        end = start+chunk_size
        chunks.append(text[start:end])
        start = end-overlap
    return chunks

def init_knowledge_base():
    print("🔄 初始化知识库：扫描文件夹+OCR+向量化入库")
    if not os.path.exists(KNOWLEDGE_FOLDER):
        os.makedirs(KNOWLEDGE_FOLDER)
        print("📁 已生成knowledge_files，放入PDF/图片重启即可入库")
        return
    load_vector_db()
    for filename in os.listdir(KNOWLEDGE_FOLDER):
        path = os.path.join(KNOWLEDGE_FOLDER,filename)
        ext = os.path.splitext(filename)[-1].lower()
        if ext not in SUPPORTED_EXTS:continue
        print(f"处理文件：{filename}")
        try:
            if ext==".pdf":
                text = extract_pdf_text(path)
            else:
                text = extract_image_text(path)
            chunks = chunk_text(text)
            for c in chunks:
                add_document(c,filename)
            print(f"✅ {filename} 入库成功")
        except Exception as e:
            print(f"❌ {filename} 失败：{str(e)}")
    save_vector_db()
    print("✅ 全部文件初始化入库完成")