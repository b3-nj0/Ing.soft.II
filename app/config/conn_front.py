from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings_env import settings_objeto

def setup_cors(app: FastAPI):
    
    origins = settings_objeto.FRONTEND_ORIGINS.split(",") if settings_objeto.ENV == "development" else ["https://tusitio.com"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )