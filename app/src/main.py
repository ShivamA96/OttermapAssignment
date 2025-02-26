from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.main import create_db_and_tables

from api.routes.user_router import user_router
from api.routes.auth_router import auth_router
from api.routes.shops_router import shops_router
from api.routes.geo_router import geo_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("booting up vendor and shape management api server")

    create_db_and_tables()

    print("Created Tables Succesfully")
    yield


app = FastAPI(title="Vendor and Shop Management API",
              version="0.1", root_path="api/v1", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/api/v1")
def health_check():
    return {"msg": "API is working 👍"}


app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(auth_router, prefix="/api/v1",  tags=["auth"])
app.include_router(shops_router, prefix="/api/v1", tags=["shops"])
app.include_router(geo_router, prefix="/api/v1", tags=["geo", "search"])
