import fastapi
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from api.usage import router as usage_router
from api.history import router as history_router

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

# Include API routes
app.include_router(usage_router)
app.include_router(history_router)
