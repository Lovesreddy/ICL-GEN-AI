# AgriBloom frontend

React and TypeScript frontend for AgriBloom, built with Vite.

## Local development

From this directory, install dependencies, copy `.env.example` to `.env.local`, and start the development server:

```powershell
npm install
Copy-Item .env.example .env.local
npm run dev
```

Set `VITE_API_BASE_URL` in `.env.local` to the backend base URL (for local development, `http://localhost:8000`). The frontend uses the backend for crop and guide content, chat, and photo analysis. Provider keys belong only in the backend environment.

Run `npm run lint` and `npm run build` before deployment. `npm run build` creates the static site in `dist`.
