import fastapi
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI(title="Token Manager API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "Token Manager API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
