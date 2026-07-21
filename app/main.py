from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from routers.hr_routes import app as hr_app
from routers.candidate_routes import app as candidate_app
from routers.login_route import app as login_app

app = FastAPI()

app.include_router(login_app)
app.include_router(hr_app)
app.include_router(candidate_app)
