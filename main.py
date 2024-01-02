import os
import logging
from fastapi import FastAPI, HTTPException
import httpx

# 配置日志
logging.basicConfig(level=logging.INFO)

# 服务器配置
B_SERVER_URL = os.getenv('B_SERVER_URL', 'http://192.168.0.94:9090/query/')
C_SERVER_URL = os.getenv('C_SERVER_URL', 'http://192.168.1.206:7861/chat/knowledge_base_chat')
TIMEOUT = 15  # 调整超时时间

app = FastAPI()


# 异步获取B服务器响应
async def get_b_server_response(query_string):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(B_SERVER_URL + query_string, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, Exception) as exc:
            logging.exception(f"请求B服务器失败: {exc}")
            return None


# 异步获取C服务器响应
async def get_c_server_response(query_string):
    c_server_payload = {
        "query": query_string,
        "knowledge_base_name": "samples",
        "top_k": 3,
        "score_threshold": 0.4,
        "history": [],
        "stream": False,
        "model_name": "baichuan2-7b",
        "temperature": 0.7,
        "max_tokens": 4096,
        "prompt_name": "default"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(C_SERVER_URL, json=c_server_payload, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, Exception) as exc:
            logging.exception("请求C服务器失败")
            return None


# 路由
@app.get('/forward/{query_string}')
async def forward_query(query_string: str):
    b_response = await get_b_server_response(query_string)
    if b_response is None:
        raise HTTPException(status_code=500, detail="B服务器未能提供响应")

    # 从 B 服务器返回的答案中提取纯文本
    answer_b = b_response.get("data", {}).get("answer", "")

    if b_response.get("data", {}).get("ratio", 0) < 55.0:
        c_response = await get_c_server_response(query_string)
        if c_response is None:
            if answer_b:
                return answer_b
            else:
                raise HTTPException(status_code=502, detail="C服务器未能提供响应，且B服务器没有有效答案")

        # 从 C 服务器返回的答案中提取纯文本
        answer_c = c_response.get("answer", "")
        return answer_c

    return answer_b


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")