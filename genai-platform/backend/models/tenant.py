from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class Tenant(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    description: str | None = None
    created_by: str  # user ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
