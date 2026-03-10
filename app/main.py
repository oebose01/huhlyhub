from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import stripe
from dotenv import load_dotenv
from supabase import create_client, Client
from app.contract import register_content_on_chain, verify_content_on_chain
import sentry_sdk

load_dotenv()

# Initialize Sentry
sentry_sdk.init(
    dsn="https://a22e274863735aa929a7c6f1da2c80e3@o4511010150809600.ingest.us.sentry.io/4511010156511232",
    send_default_pii=True,
    traces_sample_rate=1.0,
)

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

# Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class ContentRegisterRequest(BaseModel):
    content_hash: str
    user_id: str


class ContentVerifyRequest(BaseModel):
    content_hash: str


class CreateCheckoutSessionRequest(BaseModel):
    price_id: str
    user_id: str
    success_url: str
    cancel_url: str


@app.post("/api/register-content")
async def register_content(req: ContentRegisterRequest):
    try:
        # Try blockchain registration if available
        chain_result = None
        if "register_content_on_chain" in globals():
            chain_result = register_content_on_chain(req.content_hash)
        # Always store in Supabase as backup
        data = (
            supabase.table("content_registry")
            .insert(
                {
                    "content_hash": req.content_hash,
                    "user_id": req.user_id,
                    "tx_hash": chain_result.get("tx_hash") if chain_result else None,
                    "block_number": chain_result.get("block_number")
                    if chain_result
                    else None,
                    "created_at": "now()",
                }
            )
            .execute()
        )
        return {"success": True, "data": data.data, "blockchain": bool(chain_result)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/verify-content")
async def verify_content(req: ContentVerifyRequest):
    try:
        # First try blockchain
        chain_result = None
        if "verify_content_on_chain" in globals():
            chain_result = verify_content_on_chain(req.content_hash)
        if chain_result and chain_result.get("exists"):
            return {
                "success": True,
                "owner": chain_result["owner"],
                "timestamp": chain_result["timestamp"],
                "source": "blockchain",
            }
        # Fallback to Supabase
        result = (
            supabase.table("content_registry")
            .select("*")
            .eq("content_hash", req.content_hash)
            .execute()
        )
        if result.data:
            return {"success": True, "data": result.data[0], "source": "database"}
        return {"success": False, "message": "Content not found"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/create-checkout-session")
async def create_checkout_session(req: CreateCheckoutSessionRequest):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": req.price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=req.success_url,
            cancel_url=req.cancel_url,
            metadata={"user_id": req.user_id},
        )
        return {"sessionId": checkout_session.id, "url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]
        # Update user's subscription status in Supabase
        supabase.table("users").update({"subscription_status": "active"}).eq(
            "id", user_id
        ).execute()

    return {"received": True}


@app.get("/api/sentry-debug")
async def sentry_debug():
    1 / 0  # This raises ZeroDivisionError without returning anything


# Optional debug route for testing Sentry – remove after confirming
@app.get("/api/sentry-debug")
async def sentry_debug():
    division_by_zero = 1 / 0
