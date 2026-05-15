import logging
import os
import time
import uuid
from config import Config

os.makedirs("logs", exist_ok=True)
trace_logger = logging.getLogger("rag_trace_service")
trace_logger.setLevel(getattr(logging, Config.LOG_LEVEL if hasattr(Config,"LOG_LEVEL") else "INFO"))
trace_logger.handlers.clear()

file_handler = logging.FileHandler("logs/rag_full_trace.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s","%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
trace_logger.addHandler(file_handler)

def gen_trace_id() -> str:
    return str(uuid.uuid4())[:16]
def gen_span_id() -> str:
    return str(uuid.uuid4())[:8]

def write_trace_log(trace_id:str,span_id:str,parent_span_id:str,stage:str,log_content:dict):
    log_data = {
        "trace_id":trace_id,"span_id":span_id,"parent_span_id":parent_span_id,"service_stage":stage,**log_content
    }
    trace_logger.info(f"{log_data}")