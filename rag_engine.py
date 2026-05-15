import time
from config import Config
from utils import redact_pii,get_cache,set_cache
from cost_calc import calc_single_call_cost
from trace_logger import gen_trace_id,gen_span_id,write_trace_log
from vector_db import search_vector,search_keyword
from sentence_transformers import CrossEncoder

rerank_model = CrossEncoder("BAAI/bge-reranker-base")

# 安全生成+拒答
def generate(query:str,context:str):
    sensitive = ["外网","泄密","公开","密码","竞品","破解"]
    if any(w in query for w in sensitive):
        return "拒绝回答：超出内部知识范围",True,"out_of_scope"
    if not context or len(context)<20:
        return "拒绝回答：未检索到有效知识库信息",True,"no_context"
    return f"根据内部知识库：{context[:200]}",False,"normal"

# 重排序
def rerank(query:str,chunks:list,top_k=3):
    pairs = [(query,c["text"]) for c in chunks]
    scores = rerank_model.predict(pairs).tolist()
    for c,s in zip(chunks,scores):c["rerank_score"]=s
    return sorted(chunks,key=lambda x:x["rerank_score"],reverse=True)[:top_k]

def rag(query:str):
    trace_id = gen_trace_id()
    root_span = gen_span_id()
    parent_id = ""

    # 1.缓存阶段日志
    cache_span = gen_span_id()
    cache_res = get_cache(query)
    write_trace_log(trace_id,cache_span,parent_id,"cache_check",{"user_query":query,"cache_hit_status":bool(cache_res),"timestamp":time.time()})
    if cache_res:
        cost,qt,ct,at = calc_single_call_cost(query,"",cache_res)
        write_trace_log(trace_id,gen_span_id(),cache_span,"finish_cache_reply",{"single_call_cost_cny":cost,"query_token_num":qt,"context_token_num":ct,"answer_token_num":at})
        return {"answer":cache_res,"cache_hit":True,"refused":False}

    t0 = time.time()
    parent_id = cache_span

    # 2.检索阶段
    retrieve_span = gen_span_id()
    if Config.RETRIEVAL_MODE=="hybrid":
        chunks = search_vector(query)+search_keyword(query)
    else:
        chunks = search_vector(query)
    confidence = chunks[0]["score"] if chunks else 0.0
    write_trace_log(trace_id,retrieve_span,parent_id,"knowledge_retrieval",{"retrieval_mode":Config.RETRIEVAL_MODE,"confidence_score":confidence,"use_rerank":Config.ENABLE_RERANK})
    parent_id = retrieve_span

    # 3.重排序
    if Config.ENABLE_RERANK:
        rerank_span = gen_span_id()
        chunks = rerank(query,chunks)
        write_trace_log(trace_id,rerank_span,parent_id,"result_rerank",{})
        parent_id = rerank_span

    context = "\n".join([c["text"] for c in chunks[:3]])
    answer,refused,reason = generate(query,context)
    answer = redact_pii(answer,Config.PII_PATTERNS)

    # 4.成本统计
    single_cost,qt,ct,at = calc_single_call_cost(query,context,answer)
    total_token = qt+ct+at
    latency_ms = round((time.time()-t0)*1000,2)
    compliance = 1.0 if not refused else 0.0

    # 5.结束日志
    finish_span = gen_span_id()
    write_trace_log(trace_id,finish_span,parent_id,"answer_generate_finish",{
        "query_token_num":qt,"context_token_num":ct,"answer_token_num":at,"total_token_num":total_token,
        "single_call_cost_cny":single_cost,"latency_ms":latency_ms,"refuse_status":refused,
        "refuse_reason":reason,"compliance_score":compliance,"pii_redact_status":True
    })
    set_cache(query,answer)
    return {
        "answer":answer,"refused":refused,"latency_ms":latency_ms,
        "cache_hit":False,"compliance":compliance,"single_call_cost_cny":single_cost
    }