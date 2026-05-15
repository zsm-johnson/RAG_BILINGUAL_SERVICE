class Config:
    # 检索控制
    RETRIEVAL_MODE = "hybrid"   # vector_only / hybrid
    ENABLE_RERANK = True
    TOP_K = 10
    RERANK_TOP_K = 5
    CONFIDENCE_THRESHOLD = 0.6

    # 安全隐私
    PII_PATTERNS = [r"1[3-9]\d{9}", r"\w+@\w+\.\w+", r"\d{17}[\dXx]"]

    # 性能约束
    MAX_LATENCY = 10
    CONCURRENCY = 5

    # 成本计价（美元/千token）
    EMBED_MODEL_PRICE_PER_K = 0.0001
    GEN_MODEL_INPUT_PRICE_PER_K = 0.0005
    GEN_MODEL_OUTPUT_PRICE_PER_K = 0.0015
    USD_TO_CNY = 7.2
    AVG_INPUT_TOKEN = 120
    AVG_OUTPUT_TOKEN = 80

    # 链路追踪日志字段字典（交付文档直接复用）
    LOG_FIELDS = [
        "trace_id","span_id","parent_span_id","timestamp","log_level","service_stage",
        "user_query","query_token_num","context_token_num","answer_token_num","total_token_num",
        "single_call_cost_cny","retrieval_mode","use_rerank","confidence_score",
        "cache_hit_status","refuse_status","refuse_reason","latency_ms","compliance_score","pii_redact_status"
    ]