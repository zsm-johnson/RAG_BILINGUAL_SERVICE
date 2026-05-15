from config import Config
from rag_engine import rag
from cost_calc import calc_1000_times_total_cost,get_model_tradeoff_desc
import csv

TEST_QUERIES = [
    "考勤时间是什么？",
    "数据安全要求是什么？",
    "What is working time policy?",
    "可以把资料传到外网吗？",
    "公司架构分为几层？"
]

def run_eval(mode,rerank):
    Config.RETRIEVAL_MODE = mode
    Config.ENABLE_RERANK = rerank
    latencies = []
    refusals = 0
    compliance = 0
    total = len(TEST_QUERIES)
    total_cost = 0.0
    for q in TEST_QUERIES:
        res = rag(q)
        latencies.append(res["latency_ms"])
        total_cost += res["single_call_cost_cny"]
        if res["refused"]:refusals+=1
        if res["compliance"]>0.8:compliance+=1
    lat = sorted(latencies)
    p50 = lat[int(total*0.5)]
    p95 = lat[-1]
    return {
        "retrieval_mode":mode,"rerank_enable":rerank,"p50_latency_ms":p50,"p95_latency_ms":p95,
        "refuse_rate":round(refusals/total,2),"compliance_rate":round(compliance/total,2),
        "avg_single_cost_cny":round(total_cost/total,6)
    }

def full_report():
    results = [run_eval("vector_only",False),run_eval("hybrid",False),run_eval("hybrid",True)]
    thousand_cost = calc_1000_times_total_cost()
    trade = get_model_tradeoff_desc()
    with open("full_evaluation_report.csv","w",encoding="utf-8-sig",newline="") as f:
        w = csv.DictWriter(f,fieldnames=results[0].keys())
        w.writeheader()
        w.writerows(results)
        f.write(f"\n千次调用总成本(元):{thousand_cost}\n")
        f.write(f"\n模型选型权衡:\n{trade}")
    print("✅ 最终测评报告生成完成 full_evaluation_report.csv")
    for r in results:print(r)

if __name__ == "__main__":
    full_report()