# 🚀 Deploy Kakehashi (free)

Two pieces: the **FastAPI backend** (Render) and the **Next.js frontend** (Vercel). Both free.

## 1) Backend → Render
1. Push this repo to GitHub (done).
2. Go to [render.com](https://render.com) → **New +** → **Web Service** → connect your `Far_Away_Hackthon` repo.
3. Render reads `render.yaml` automatically. (If asked manually: Runtime **Python**, Build `pip install -r requirements.txt`, Start `uvicorn api.main:app --host 0.0.0.0 --port $PORT`.)
4. In **Environment**, add your secrets:
   - `GROQ_API_KEY`, `JSEARCH_API_KEY`, `ESTAT_APP_ID`
   - (`LLM_MODEL=openai/gpt-oss-120b` is already in render.yaml)
5. Deploy → you get a URL like `https://kakehashi-api.onrender.com`. Test `…/health`.
   *(Free tier sleeps when idle — first request after idle takes ~30s to wake.)*

## 2) Frontend → Vercel
1. Go to [vercel.com](https://vercel.com) → **Add New → Project** → import the same repo.
2. **Root Directory:** set to `frontend`.
3. **Environment Variables:** add `NEXT_PUBLIC_API_URL` = your Render URL (e.g. `https://kakehashi-api.onrender.com`).
4. Deploy → you get `https://kakehashi.vercel.app`. **That public URL is your Round 1 demo link.**

## Notes
- The backend already allows cross-origin requests (CORS open) — fine for the demo; restrict later.
- Keys live only in the host dashboards / local `.env`, never in the repo.
