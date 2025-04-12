from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from bson import ObjectId

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: EmailStr
    password: str
    name: str
    tenant_id: str  # NEW: to associate user with a tenant
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    tenant_id: str