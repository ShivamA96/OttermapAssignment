from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db.main import create_db_and_tables
app = FastAPI(title="Vendor and Shop Management API",
              version="0.1", root_path="api/v1", )

app.add_middleware(CORSMiddleware, allow_origins=True,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables
    yield
