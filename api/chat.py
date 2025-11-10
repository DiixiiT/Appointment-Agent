from fastapi import APIRouter
from pydantic import BaseModel

from agent.scheduling_agent import agentchat

router = APIRouter()


class Chat(BaseModel):
    message: str


@router.post("/")
async def chat(chat_in: Chat):
    return await agentchat(123, chat_in.message)
