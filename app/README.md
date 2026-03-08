# Backend API

## Setup

1. Create a Supabase project and get your URL and anon key.
2. Create a table `content_registry` with columns:
   - `id` (uuid, primary key, default: uuid_generate_v4())
   - `content_hash` (text, unique)
   - `user_id` (text)
   - `created_at` (timestamp with time zone, default: now())
3. Copy `.env.example` to `.env` and fill in your keys.
4. Run the server: `uvicorn app.main:app --reload`
