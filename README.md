User Guide: Bilingual Enterprise-Grade RAG Generative AI Service
1. Introduction
This user guide provides step-by-step instructions for installing, configuring, and using the Bilingual Enterprise-Grade RAG Generative AI Service. This service is designed to facilitate efficient querying of enterprise internal knowledge bases (including PDFs, images, and scanned documents) with bilingual support (Chinese/English), ensuring compliance with performance, security, and cost constraints.
Before starting, ensure your environment meets the prerequisites and you have read through the key notes to avoid common errors.
2. Prerequisites
2.1 System Requirements
- Operating System: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- Python Version: 3.8 or higher (Python 3.9-3.11 is recommended for better compatibility)
- Disk Space: At least 500MB (for dependencies, vector database, and logs)
- Network: Stable internet connection (for installing dependencies and downloading models)
2.2 Dependency Installation
Install all required dependencies using the following command. The command uses the Baidu PyPI mirror for faster downloads; if parsing fails, replace it with the official PyPI source.
# Install dependencies (Baidu mirror)
pip install fastapi uvicorn sentence-transformers numpy pymupdf paddleocr paddlepaddle tiktoken -i https://mirror.baidu.com/pypi/simple

# If the Baidu mirror fails (error: "Failed to parse the webpage, possibly an unsupported webpage type"), use the official source:
pip install fastapi uvicorn sentence-transformers numpy pymupdf paddleocr paddlepaddle tiktoken -i https://pypi.org/simple/
3. Quick Setup & Startup
3.1 Prepare Knowledge Base Files
1. In the root directory of the project, create a folder named knowledge_files (case-sensitive).
2. Place your knowledge base files into this folder. Supported file types include:
        
  - PDF files (both editable and scanned PDFs are supported; scanned PDFs will be processed via OCR)
  - Image files: PNG, JPG, JPEG (will be processed via OCR to extract text)
3. Note: Avoid placing non-supported file types (e.g., TXT, DOCX) in this folder, as they will be skipped during initialization.
3.2 Start the Service
Run the following command in the project root directory to start the service. The service will automatically initialize the knowledge base (OCR parsing, text chunking, vectorization, and persistent storage) on startup.
python main.py
After successful startup, you will see the following prompts (indicating the service is running):
🔄 初始化知识库：扫描文件夹+OCR+向量化入库
📁 已生成knowledge_files，放入PDF/图片重启即可入库 (if the folder was just created)
✅ 全部文件初始化入库完成
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
Note: If you see the error "Failed to parse the webpage, possibly an unsupported webpage type" during startup, it is likely due to a failure in downloading dependencies via the Baidu mirror. Reinstall dependencies using the official PyPI source (see Section 2.2).
4. Service Usage
4.1 Check Service Health
To verify if the service is running normally, open a browser or use a tool like Postman to access the health check interface:
http://127.0.0.1:8000/health
If the service is healthy, you will receive the response: {"status":"ok"}.
Note: If you see the error "The URL may be misspelled, please check", ensure the URL is correctly typed (no extra spaces, correct port number, and no typos).
4.2 Query the Knowledge Base
Use the QA interface to query the knowledge base. The interface supports both Chinese and English queries. The URL format is:
http://127.0.0.1:8000/qa?query=your_query
### Examples:
- Chinese query: http://127.0.0.1:8000/qa?query=考勤时间是什么？
- English query: http://127.0.0.1:8000/qa?query=What is the working time policy?
### Key Notes for Queries:
- Do not omit thequery parameter (e.g., http://127.0.0.1:8000/qa will trigger the error "The URL may be misspelled, please check").
- Keep queries clear and specific to improve retrieval accuracy (e.g., avoid overly short queries like http://127.0.0.1:8000/qa?query=What, which may return low-confidence results or refusal to answer).
- Sensitive queries (e.g., "leak data", "external network", "password") will be refused, with the response: "拒绝回答：超出内部知识范围".
4.3 Run One-Click Evaluation
To evaluate the service performance, retrieval accuracy, and cost, run the one-click evaluation script. This script will test three retrieval modes and generate a detailed report.
python evaluator.py
After evaluation, a report file full_evaluation_report.csv will be generated in the root directory. The report includes:
    Comparison of three retrieval modes: vector_only, hybrid, hybrid+rerankQuantitative indicators: P50/P95 latency, refusal rate, compliance rateCost statistics: Average single-call cost, total cost for 1000 callsModel selection trade-off analysis5. Common Error HandlingThis section addresses the most common errors encountered during installation and usage, based on actual system error messages.
Error 1: "Failed to parse the webpage, possibly an unsupported webpage type. Please check the webpage or try again later."
- Occurrence Scenario: Usually appears when installing dependencies via the Baidu PyPI mirror (https://mirror.baidu.com/pypi/simple), or when accessing the service address http://0.0.0.0:8000 directly in some browsers.
- Solution:
        
  - For dependency installation: Replace the Baidu mirror with the official PyPI source (see Section 2.2).
  - For service access: Use http://127.0.0.1:8000 instead of http://0.0.0.0:8000 when accessing the service via a browser.
Error 2: "The URL may be misspelled, please check."
- Occurrence Scenario: Appears when accessing the QA interface (http://127.0.0.1:8000/qa), health check interface (http://127.0.0.1:8000/health), or other service interfaces with incorrect URLs.
- Common Causes & Solutions:
        
  - Missing query parameter in the QA interface (e.g., http://127.0.0.1:8000/qa → add ?query=your_query).
  - Typos in the URL (e.g., http://127.0.0.1:8080/qa → correct the port to 8000).
  - Extra spaces in the URL (e.g., http://127.0.0.1:8000/ qa?query=test → remove spaces).
  - Overly short query (e.g., http://127.0.0.1:8000/qa?query=What → use a more specific query).
6. Configuration Adjustment
All service configurations are stored in config.py. You can adjust the following parameters without modifying any business code:
- RETRIEVAL_MODE: Set the retrieval mode (vector_only for vector-only retrieval, hybrid for vector + keyword hybrid retrieval).
- ENABLE_RERANK: Toggle the re-ranking function (True to enable, False to disable).
- TOP_K/RERANK_TOP_K: Adjust the number of retrieved results (default: 10) and re-ranked results (default: 5).
- PII_PATTERNS: Add or modify PII desensitization rules (e.g., phone numbers, emails, ID cards).
- Cost-related parameters: Adjust model pricing, USD-CNY exchange rate, and average Token count per query to match actual usage scenarios.
Note: After modifying config.py, restart the service for the changes to take effect.
7. Key Notes
- The knowledge_files folder is the only directory for knowledge base files; do not rename or move it.
- Scanned PDFs and images may take a few seconds to process during service startup (depending on file size and quantity).
- The service uses an in-memory cache by default; for production environments, replace it with Redis for better scalability.
- Full-link logs are stored in the logs/ directory, which can be used for troubleshooting and performance analysis.
- All generated answers are strictly based on the retrieved knowledge base context; no external information is used.
8. Troubleshooting
If you encounter errors not covered in Section 5, follow these steps:
1. Check the service logs in logs/rag_full_trace.log for detailed error information.
2. Verify that all dependencies are installed correctly (reinstall dependencies if necessary).
3. Ensure the knowledge_files folder contains only supported file types and no corrupted files.
4. Restart the service and try again (some temporary network or initialization issues can be resolved by restarting).
