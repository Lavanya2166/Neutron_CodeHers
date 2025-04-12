from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    sender_id: str
    message: str
    chat_type: str  # "admin" or "public"
    tenant_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
