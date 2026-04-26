# llmwiki Frontend

React SPA for llmwiki.

## Scripts

```bash
npm install
npm run dev
npm run build
npm run lint
```

## Notes

- The app expects the FastAPI backend on `http://localhost:8080`.
- Production builds output to `frontend/dist/`.
- Current routes: `/`, `/graph`, `/page/:title`, `/query`, `/ingest`, `/lint`, `/log`, `/stats`, `/raw`.
