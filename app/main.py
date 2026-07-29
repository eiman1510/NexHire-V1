import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from middlewares.request_time import log_request_time

load_dotenv()

from routers.hr_routes import app as hr_app
from routers.candidate_routes import app as candidate_app
from routers.login_route import app as login_app
from features.admin.admin_handler import router as admin_router

app = FastAPI()

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
app.middleware("http")(log_request_time)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_app)
app.include_router(hr_app)
app.include_router(candidate_app)
app.include_router(admin_router)
