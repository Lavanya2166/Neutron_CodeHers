from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CaptionEntry(BaseModel):
    user_id: str
    theme: str
    tone: str
    caption: str
    vibe: Optional[str]
    object: Optional[str]
    created_at: Optional[datetime] = None
