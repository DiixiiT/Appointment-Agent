import os

from dotenv import load_dotenv
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

load_dotenv()
from api.api import v1_router
from logger import logger

APP_ENV = os.getenv("ENVIRONMENT", "local")
print(os.getenv("OPENAI_API_KEY"))


app = FastAPI(title="APP", version="1.1.0", docs_url=None, description="Learning app")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    logger.info("server is running...")
    return {"msg": "Server is running!!"}


@app.get(f"/api/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url=f"/api/docs/openapi.json", title="Learning app"
    )


@app.get(f"/api/docs/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title="Learning app", version=app.version, routes=app.routes)


jwt_token_auth = HTTPBearer(scheme_name="JWT")
app.include_router(v1_router, prefix="/api", dependencies=[Security(jwt_token_auth)])
