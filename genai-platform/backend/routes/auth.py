from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from backend.auth import hash_password, verify_password, create_access_token, decode_token
from backend.models.user import User
from backend.database import db
from backend.database import get_user_collection
from backend.models.user import UserCreate
router = APIRouter()

from fastapi.security import OAuth2PasswordBearer

# This is the URL where your frontend/client will send the login request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    tenant_id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/auth/register")
async def register(user: UserCreate, db=Depends(get_user_collection)):
    existing_user = await db.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    user_data = user.dict()
    user_data["password"] = hashed_pw
    user_data["tenant_id"] = user.tenant_id  # ⬅️ Added here
    user_data["created_at"] = datetime.utcnow()

    result = await db.insert_one(user_data)
    return {"id": str(result.inserted_id), "email": user.email}

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_user_collection)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "tenant_id": user.get("tenant_id")  # ⬅️ Include tenant_id
    }

@router.post("/auth/login")
def login_user(request: LoginRequest):
    user = db["users"].find_one({"email": request.email})
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["email"],
        "role": user["role"],
        "tenant_id": user["tenant_id"]
    })

    return {"access_token": token, "token_type": "bearer"}

@router.get("/auth/me")
def get_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"email": payload["sub"], "role": payload["role"]}
