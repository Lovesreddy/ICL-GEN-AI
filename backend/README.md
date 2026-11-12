# AgriBloom backend

## Run on Windows

Open a PowerShell terminal from the project root and run:

```powershell
Set-Location .\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If PowerShell activation is unavailable, run Uvicorn directly:

```powershell
Set-Location .\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The terminal must be in `backend` so Python can import `app`. On the first startup, sample knowledge indexing may load the embedding model; wait for `Application startup complete` before opening the frontend.

Check backend health at <http://localhost:8000/api/health>. The crop, knowledge, fertilizer, and pest endpoints are available under `/api/crops`, `/api/knowledge`, `/api/fertilizers`, and `/api/pests`.

The home page, crop guides, knowledge hub, AI assistant, and photo guide are available without signing in. Administrator and personal-account routes remain protected.

Run the frontend in a second terminal from `frontend` with `npm run dev`. The backend allows Vite's local ports 5173 through 5175.

## Configure the AI assistant

For Groq text chat, set `LLM_PROVIDER=groq`, `GROQ_MODEL=openai/gpt-oss-20b`, and a valid `GROQ_API_KEY` in `backend/.env`.

The photo guide sends the selected image and notes to Groq only after the user checks the consent box and requests analysis. It uses `GROQ_VISION_MODEL=qwen/qwen3.8-27b` and the same server-side `GROQ_API_KEY`; the configured text-chat model is not used for image inputs. Groq currently documents this Qwen vision model as preview with usage-based pricing, so confirm current account access and prices before use. The backend does not save uploaded photos and limits each client IP to eight analysis requests per hour. Restart the backend after changing provider settings or keys.

For xAI/Grok, set `LLM_PROVIDER=grok`, `GROK_MODEL=grok-4.7`, and a valid `GROK_API_KEY` in `backend/.env` (the configuration also accepts `XAI_API_KEY`). The assistant uses xAI's Responses API. If the assistant reports that xAI rejected the key, replace it with a valid key; do not paste API keys into chat or commit them to the project.

If no provider is configured or its key is rejected, the assistant can still show a clearly labeled answer extracted from matching indexed guides. This fallback does not call an AI model and does not require an API key.
