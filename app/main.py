from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


class ContentRegisterRequest(BaseModel):
    content_hash: str
    user_id: str


class ContentVerifyRequest(BaseModel):
    content_hash: str


@app.post("/api/register-content")
async def register_content(req: ContentRegisterRequest):
    try:
        data = (
            supabase.table("content_registry")
            .insert(
                {
                    "content_hash": req.content_hash,
                    "user_id": req.user_id,
                    "created_at": "now()",
                }
            )
            .execute()
        )
        return {"success": True, "data": data.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/verify-content")
async def verify_content(req: ContentVerifyRequest):
    result = (
        supabase.table("content_registry")
        .select("*")
        .eq("content_hash", req.content_hash)
        .execute()
    )
    if result.data:
        return {"success": True, "data": result.data[0]}
    return {"success": False, "message": "Content not found"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
