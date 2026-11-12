# ICL-GEN-AI — AgriBloom

AgriBloom is an organic-farming guidance platform. It combines crop and farming knowledge with an AI assistant and an optional photo guide to help growers make informed field decisions.

## Features

- Browse crop profiles with growing season, soil, water, and cultivation guidance.
- Search and filter the farming Knowledge Hub.
- Use fertilizer and pest-management resources.
- Ask farming questions through the AI assistant.
- Use the Photo Guide to request image-based advice about crops, soil, or fertilizer. Image analysis is sent to the configured AI provider only after the user gives consent.
- Use the public crop and knowledge pages without signing in.

## Technology

- **Frontend:** React, TypeScript, Vite
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite by default
- **Knowledge retrieval:** low-memory deterministic embeddings by default, with a FAISS vector index; semantic embeddings are optional
- **AI providers:** Groq, Gemini, or xAI/Grok, configured on the backend

## Requirements

- Python 3.12 recommended
- Node.js 22 LTS and npm
- Git

## Run locally on Windows

Clone the repository and open PowerShell in its root folder:

```powershell
git clone https://github.com/Lovesreddy/ICL-GEN-AI.git
Set-Location .\ICL-GEN-AI
```

### 1. Configure and run the backend

Create a virtual environment and install the Python dependencies:

```powershell
Set-Location .\backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend\.env` as needed. Set a private `JWT_SECRET`. To enable AI responses, configure a provider and its key there. **Never put provider keys in frontend environment variables or commit them to GitHub.**

Start the API:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

On its first startup, the backend creates the database, seeds crop profiles, and indexes sample guides. The default deterministic embedding mode indexes the bundled text guides without downloading a model. It uses less memory but provides weaker semantic matching than the optional model in `requirements-ml.txt`.

To run tests, install `requirements-dev.txt` instead of `requirements.txt`. PDF and DOCX uploads are optional and require `requirements-documents.txt`.

To enable full semantic embeddings locally, install `requirements-ml.txt` and set `EMBEDDING_BACKEND=sentence-transformers` in `backend\.env`. This model uses significantly more memory and is not recommended for Render Free.

### 2. Configure and run the frontend

Open a second PowerShell terminal in the project root:

```powershell
Set-Location .\frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open the frontend at <http://localhost:5173>. The default frontend API address is `http://localhost:8000`; it can be changed with `VITE_API_BASE_URL` in `frontend\.env.local`.

## AI and photo guide configuration

For Groq text chat and photo analysis, configure these values in `backend\.env`:

```dotenv
LLM_PROVIDER=groq
GROQ_API_KEY=your-server-side-key
GROQ_MODEL=openai/gpt-oss-20b
GROQ_VISION_MODEL=qwen/qwen3.8-27b
```

The Photo Guide sends the selected image, crop, and notes to the configured vision provider only after consent. AgriBloom does not save the image; the provider may charge for usage. Check model availability and pricing with the provider before enabling it. Keep all API keys on the backend and rotate any key that may have been exposed.

Without a valid provider configuration, the text assistant may still return matching indexed guidance, but image analysis requires a working vision model and key.

## Useful URLs

- Frontend: <http://localhost:5173>
- API health: <http://localhost:8000/api/health>
- Interactive API documentation: <http://localhost:8000/docs>

## Tests and checks

Run backend tests:

```powershell
Set-Location .\backend
pip install -r requirements-dev.txt
python -m pytest
```

Run frontend lint and production build:

```powershell
Set-Location .\frontend
npm run lint
npm run build
```

## Deployment

A simple deployment setup is **Render for the backend** and **Vercel for the frontend**:

1. Deploy the backend from the `backend` directory. Use `pip install -r requirements.txt` as the build command and `uvicorn app.main:app --host 0.0.0.0 --port $PORT` as the start command. Keep `EMBEDDING_BACKEND=deterministic` and `AUTO_INDEX=true` for the low-memory profile.
2. Configure the backend environment variables and set `CORS_ORIGINS` to the exact HTTPS origin of the deployed frontend.
3. If the selected hosting plan supports persistent disks, mount one at `/var/data` and set `DATABASE_URL=sqlite:////var/data/organic_farming.db` and `VECTOR_DIR=/var/data/vector_store`. On Render Free, local data is ephemeral.
4. Deploy the frontend from the `frontend` directory with `npm run build`, output directory `dist`, and `VITE_API_BASE_URL` set to the backend base URL **without** `/api`.
5. Check the backend health endpoint and test the live frontend. If a custom domain is added, update `CORS_ORIGINS` and redeploy the backend.

The deterministic profile improves the chance of starting on Render's 512 MB free instance, but cannot guarantee the service will fit its CPU and memory limits. Render free instances have ephemeral local storage: SQLite data and uploaded files can reset after restarts or redeploys, and `AUTO_INDEX=true` rebuilds the bundled sample index on startup. Persistent storage requires a plan that supports disks. This setup is intended for a single backend instance; scaling to multiple instances requires shared database and vector storage. See [`backend/README.md`](./backend/README.md) for additional backend notes.

## Security

- `backend/.env` and `frontend/.env.local` are local configuration files and should not be committed.
- Use strong, unique secrets for `JWT_SECRET` and any configured administrator credentials.
- Keep AI provider keys in the backend hosting provider's secret environment settings.
- The public GitHub repository contains example environment files only; replace their placeholders locally.
