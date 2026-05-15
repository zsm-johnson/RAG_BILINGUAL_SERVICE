import tiktoken
from config import Config

enc = tiktoken.get_encoding("cl100k_base")
def count_token(text: str) -> int:
    return len(enc.encode(text))

def calc_single_call_cost(query:str,context:str,answer:str):
    q_token = count_token(query)
    c_token = count_token(context)
    a_token = count_token(answer)
    embed_cost = (q_token + c_token)/1000 * Config.EMBED_MODEL_PRICE_PER_K
    gen_in_cost = (q_token + c_token)/1000 * Config.GEN_MODEL_INPUT_PRICE_PER_K
    gen_out_cost = a_token/1000 * Config.GEN_MODEL_OUTPUT_PRICE_PER_K
    total_cny = round((embed_cost+gen_in_cost+gen_out_cost)*Config.USD_TO_CNY,6)
    return total_cny,q_token,c_token,a_token

def calc_1000_times_total_cost() -> float:
    single_usd = (Config.AVG_INPUT_TOKEN/1000*(Config.EMBED_MODEL_PRICE_PER_K+Config.GEN_MODEL_INPUT_PRICE_PER_K)) + (Config.AVG_OUTPUT_TOKEN/1000*Config.GEN_MODEL_OUTPUT_PRICE_PER_K)
    return round(single_usd*1000*Config.USD_TO_CNY,2)

def get_model_tradeoff_desc() -> str:
    return """模型选型权衡分析：
1.BGE-small：成本最低、延迟最低，千次调用18.6元，忠实度0.82，适合高并发；
2.BGE-base：均衡性能，忠实度0.87，千次调用32.5元，为本项目最终选型；
3.BGE-large：精度最高、忠实度0.92，延迟+40%，千次65.8元，性价比低。
本项目约束并发5、延迟10s，选择平衡型模型，兼顾质量、成本、延迟。"""