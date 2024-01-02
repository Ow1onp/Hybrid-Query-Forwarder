import os
import logging
from fastapi import FastAPI, HTTPException
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)

# Server configuration
B_SERVER_URL = os.getenv('B_SERVER_URL', 'http://[B_SERVER_IP]:[B_SERVER_PORT]/query/')
C_SERVER_URL = os.getenv('C_SERVER_URL', 'http://[C_SERVER_IP]:[C_SERVER_PORT]/chat/knowledge_base_chat')
TIMEOUT = 15  # Set timeout duration

app = FastAPI()

# Asynchronously get response from B server
async def get_b_server_response(query_string):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(B_SERVER_URL + query_string, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, Exception) as exc:
            logging.exception(f"Failed to request B server: {exc}")
            return None

# Asynchronously get response from C server
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
            logging.exception("Failed to request C server")
            return None

# Route
@app.get('/forward/{query_string}')
async def forward_query(query_string: str):
    b_response = await get_b_server_response(query_string)
    if b_response is None:
        raise HTTPException(status_code=500, detail="B server did not provide a response")

    # Extract plain text from the answer returned by B server
    answer_b = b_response.get("data", {}).get("answer", "")

    if b_response.get("data", {}).get("ratio", 0) < 55.0:
        c_response = await get_c_server_response(query_string)
        if c_response is None:
            if answer_b:
                return answer_b
            else:
                raise HTTPException(status_code=502, detail="C server did not provide a response, and B server has no valid answer")

        # Extract plain text from the answer returned by C server
        answer_c = c_response.get("answer", "")
        return answer_c

    return answer_b

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
