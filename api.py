from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional

app = FastAPI()

# 啟用 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 金鑰驗證
API_KEY = os.getenv("API_KEY", "your-api-key")  # 請更改為安全的 API 金鑰
api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/api/v1/process_audio")
async def process_audio(
    file: UploadFile = File(...),
    system_prompt: Optional[str] = "",
    x_api_key: str = Header(None)
):
    # 驗證 API 金鑰
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    try:
        # ... (原有的音檔處理邏輯) ...
        
        return {
            "status": "success",
            "data": {
                "transcript": transcript,
                "summary_en": processed_transcript,
                "summary_zh": processed_transcript_ch,
                "key_points": processed_summary,
                "srt_content": srt_content
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"} 