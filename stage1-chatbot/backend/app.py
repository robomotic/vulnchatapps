from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import json
import pathlib

app = FastAPI(title="Customer Support Chatbot API")

# Enable CORS for all origins (for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# SYSTEM_PROMPT can be set via environment variable, or loaded from a file in the backend folder, fallback to default if not set
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
if not SYSTEM_PROMPT:
    prompt_path = pathlib.Path(__file__).parent / "system_prompt.txt"
    if prompt_path.exists():
        SYSTEM_PROMPT = prompt_path.read_text(encoding="utf-8")
    else:
        SYSTEM_PROMPT = """
You are a helpful customer support assistant for an online store called 'ShopEasy'.\nYou help customers with product inquiries, order status, return policies, and general shopping assistance.\nKeep responses brief, friendly, and helpful. If you don't know something, admit it and offer to connect the customer with a human agent.\n\nStore information:\n- Name: ShopEasy\n- Products: Electronics, clothing, home goods, toys\n- Return policy: 30-day returns on most items\n- Shipping: Free on orders over $35
"""

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
PROVIDER_MODEL = os.getenv("PROVIDER_MODEL", "tinyllama:1.1b")

# API provider selection and config
API_PROVIDER = os.getenv("API_PROVIDER", "ollama").lower()  # ollama, openai, openrouter, gemini, anthropic
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# LLM common settings
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
LLM_STOP_WORD = os.getenv("LLM_STOP_WORD", "")

# Common LLM settings
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))
LLM_STOP = os.getenv("LLM_STOP", None)
if LLM_STOP:
    try:
        LLM_STOP = json.loads(LLM_STOP)
    except Exception:
        LLM_STOP = [LLM_STOP]

@app.get("/")
def read_root():
    return {"status": "Online", "service": "Customer Support Chatbot"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if API_PROVIDER == "ollama":
            payload = {
                "model": PROVIDER_MODEL,
                "prompt": f"{SYSTEM_PROMPT}\n\nCustomer: {request.message}\n\nAssistant:",
                "stream": False,
                "temperature": LLM_TEMPERATURE,
                "num_predict": LLM_MAX_TOKENS
            }
            if LLM_STOP_WORD:
                payload["stop"] = [LLM_STOP_WORD]
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    OLLAMA_URL,
                    json=payload
                )
        elif API_PROVIDER == "openai":
            payload = {
                "model": PROVIDER_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": request.message}
                ],
                "temperature": LLM_TEMPERATURE,
                "max_tokens": LLM_MAX_TOKENS
            }
            if LLM_STOP_WORD:
                payload["stop"] = [LLM_STOP_WORD]
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
        elif API_PROVIDER == "openrouter":
            payload = {
                "model": PROVIDER_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": request.message}
                ],
                "temperature": LLM_TEMPERATURE,
                "max_tokens": LLM_MAX_TOKENS
            }
            if LLM_STOP_WORD:
                payload["stop"] = [LLM_STOP_WORD]
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
        elif API_PROVIDER == "gemini":
            payload = {
                "contents": [
                    {"role": "user", "parts": [{"text": f"{SYSTEM_PROMPT}\n\n{request.message}"}]}
                ],
                "generationConfig": {
                    "temperature": LLM_TEMPERATURE,
                    "maxOutputTokens": LLM_MAX_TOKENS
                }
            }
            if LLM_STOP_WORD:
                payload["generationConfig"]["stopSequences"] = [LLM_STOP_WORD]
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{PROVIDER_MODEL}:generateContent?key={GEMINI_API_KEY}",
                    headers={"Content-Type": "application/json"},
                    json=payload
                )
        elif API_PROVIDER == "anthropic":
            payload = {
                "model": PROVIDER_MODEL,
                "max_tokens": LLM_MAX_TOKENS,
                "messages": [
                    {"role": "user", "content": f"{SYSTEM_PROMPT}\n\n{request.message}"}
                ],
                "temperature": LLM_TEMPERATURE
            }
            if LLM_STOP_WORD:
                payload["stop_sequences"] = [LLM_STOP_WORD]
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
        else:
            raise HTTPException(status_code=400, detail="Invalid API_PROVIDER specified.")

        if response.status_code != 200:
            if DEBUG:
                print(f"[API Error] Provider: {API_PROVIDER}, Status: {response.status_code}, Body: {response.text}")
            # Try to extract error message from response
            try:
                err = response.json()
                detail = err.get("error") or err.get("detail") or response.text
            except Exception:
                detail = response.text
            raise HTTPException(status_code=500, detail=detail)

        result = response.json()
        # Parse response for each provider
        if API_PROVIDER == "ollama":
            answer = result["response"]
        elif API_PROVIDER in ("openai", "openrouter"):
            answer = result["choices"][0]["message"]["content"]
        elif API_PROVIDER == "gemini":
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
        elif API_PROVIDER == "anthropic":
            answer = result["content"][0]["text"] if "content" in result and result["content"] else result.get("text", "")
        else:
            answer = "[Error: Unknown provider response]"
        return ChatResponse(response=answer)
    except Exception as e:
        if DEBUG:
            import traceback
            print("[Backend Exception]", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
