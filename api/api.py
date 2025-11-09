from fastapi import APIRouter

from api import calendly_integration, chat

v1_router = APIRouter()
v1_router.include_router(
    calendly_integration.router, prefix="/caledly", tags=["Caledly"]
)
v1_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
