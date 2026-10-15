# Backend on Render and frontend on Netlify

1. Connect Render and create a Blueprint from https://github.com/Monkh0305/NPL_NWES.
2. Render reads `render.yaml`. Set `YOUTUBE_API_KEY` and `GEMINI_API_KEY` using the hosting dashboard. Never commit keys.
3. Set Render `CORS_ORIGINS` to a JSON array containing the exact Netlify origin, for example `["https://your-site.netlify.app"]` (no trailing slash).
4. Once Render is healthy, set Netlify `VITE_API_BASE_URL` to `https://YOUR-RENDER-HOST/api` and trigger a new production build.
5. Check Render `/` returns `status: ok`, then load the Netlify dashboard and check videos load.

The free configuration uses local SQLite: cached analysis results can disappear after a restart or redeploy. For durable storage, use a persistent database or a paid disk before relying on saved results. API keys remain in Render environment variables.
