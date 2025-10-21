from fastapi import FastAPI
from . import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="String Analyzer Service")

app.include_router(router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
