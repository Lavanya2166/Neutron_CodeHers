from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_chat_collection
from backend.models.chat import ChatMessage
from backend.routes.auth import get_current_user
from typing import List
from pymongo.collection import Collection

router = APIRouter()

@router.post("/chat/send", response_model=ChatMessage)
async def send_message(
    message: ChatMessage,
    db: Collection = Depends(get_chat_collection),
    user=Depends(get_current_user)
):
    message.sender_id = user["_id"]
    message.tenant_id = user["tenant_id"]
    result = db.insert_one(message.dict(by_alias=True))
    message.id = str(result.inserted_id)
    return message

@router.get("/chat/messages", response_model=List[ChatMessage])
async def get_messages(
    chat_type: str,
    db: Collection = Depends(get_chat_collection),
    user=Depends(get_current_user)
):
    messages = db.find({"chat_type": chat_type, "tenant_id": user["tenant_id"]})
    return [ChatMessage(**msg) for msg in messages]

