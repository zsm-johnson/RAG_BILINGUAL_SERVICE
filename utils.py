import re
import time
import os

# PII脱敏
def redact_pii(text: str, patterns: list) -> str:
    for pat in patterns:
        text = re.sub(pat, "[***PII***]", text)
    return text

# 内存缓存（可无缝替换为Redis）
CACHE = {}
def get_cache(key: str):
    return CACHE.get(key)
def set_cache(key: str, value, expire=3600):
    CACHE[key] = {"value": value, "expire": time.time() + expire}