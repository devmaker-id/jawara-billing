"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from .config import HOST, PORT, LOG_LEVEL
from .routes import health, customers, invoices

# ---------------------------------------------------------------------------
# Lifespan — startup/shutdown hooks (DB pool, FreeRADIUS probe, etc.)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    app.state.name = "jawara-billing"
    yield
    # shutdown
    pass

app = FastAPI(
    title="jawara-billing",
    description="ISP Billing System (Sendi) — web panel port 793",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router, tags=["health"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])

# ---------------------------------------------------------------------------
# Static web panel (port 793)
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>jawara-billing</title>
<style>
  :root { --bg:#0f172a; --card:#1e293b; --txt:#e2e8f0; --acc:#22d3ee; --ok:#34d399; }
  body { margin:0; font-family:'JetBrains Mono',monospace; background:var(--bg); color:var(--txt); }
  .wrap { max-width:1100px; margin:0 auto; padding:2rem; }
  .card { background:var(--card); border:1px solid #334155; border-radius:12px; padding:2rem; }
  h1 { margin:0 0 .5rem; font-size:1.5rem; color:#ffffff; }
  p { color:#94a3b8; margin:0 0 1.25rem; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:1rem; margin-top:1rem; }
  .stat { background:rgba(15,23,42,.6); border-radius:8px; padding:1rem; }
  .stat .num { font-size:1.6rem; font-weight:700; color:var(--acc); }
  .stat .lbl { font-size:.85rem; color:#94a3b8; }
  .btn { background:var(--acc); color:#020617; border:none; padding:.6rem 1.2rem; border-radius:6px; cursor:pointer; font-family:inherit; }
  .btn:hover { filter:brightness(1.1); }
  .link { color:var(--acc); cursor:pointer; text-decoration:underline; }
  code { background:#1e293b; padding:.15rem .4rem; border-radius:4px; color:#93c5fd; }
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>jawara-billing <span style="font-size:.75rem;color:#94a3b8;">v0.1.0 — ISP Billing Sendi</span></h1>
      <p>Web admin panel berjalan di <code>:793</code>. Akses semua role: admin / operator / resseler.</p>
      <div class="grid">
        <div class="stat"><div class="num">—</div><div class="lbl">Langganan aktif</div></div>
        <div class="stat"><div class="num">—</div><div class="lbl">Tagihan</th></div>
        <div class="stat"><div class="num">—</div><div class="lbl">FreeRADIUS clients</div></div>
        <div class="stat"><div class="num">—</div><div class="lbl">MikroTik :1998</div></div>
      </div>
      <div style="margin-top:1.25rem;">
        <span class="link" id="api">GET /api/health → JSON</span>
      </div>
    </div>
  </div>
<script>
  fetch('/api/health')
    .then(r => r.json())
    .then(d => { document.getElementById('api').textContent = 'GET /api/health → ' + JSON.stringify(d, null, 2); })
    .catch(e => { document.getElementById('api').textContent = 'error: ' + e; });
</script>
</body>
</html>
"""

@app.get("/", include_in_schema=False)
async def index() -> HTMLResponse:
    return HTMLResponse(content=HTML, status_code=200)

@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "service": "jawara-billing",
            "version": "0.1.0",
            "status": "ok",
            "port": PORT,
            "host": HOST,
        },
    )
