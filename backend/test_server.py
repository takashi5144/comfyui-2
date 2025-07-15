"""
シンプルなテストサーバー - 接続確認用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Test server is running", "status": "ok"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "API is working"}

@app.post("/api/generate")
async def test_generate(data: dict):
    return {
        "success": True,
        "message": "This is a test response",
        "received_data": data
    }

@app.get("/api/models")
async def test_models():
    return {
        "models": [
            {"name": "test-model-1.safetensors", "type": "checkpoint"},
            {"name": "test-model-2.safetensors", "type": "checkpoint"}
        ]
    }

@app.get("/api/samplers")
async def test_samplers():
    return {
        "samplers": ["euler", "euler_ancestral", "dpm_2", "dpm_2_ancestral"]
    }

@app.get("/api/schedulers")
async def test_schedulers():
    return {
        "schedulers": ["normal", "karras", "exponential", "simple"]
    }

if __name__ == "__main__":
    print("Starting test server on http://127.0.0.1:8000")
    print("Press Ctrl+C to stop")
    uvicorn.run(app, host="127.0.0.1", port=8000)