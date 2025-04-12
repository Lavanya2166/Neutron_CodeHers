from fastapi import APIRouter, Depends, HTTPException
from backend.database import db
from backend.auth import get_current_user
from backend.models.tenant import Tenant

router = APIRouter()

@router.post("/tenant/create")
async def create_tenant(data: dict, current_user=Depends(get_current_user)):
    name = data.get("name")
    desc = data.get("description", "")
    if not name:
        raise HTTPException(status_code=400, detail="Tenant name is required")

    tenant = Tenant(name=name, description=desc, created_by=current_user["id"])
    await db["tenants"].insert_one(tenant.dict(by_alias=True))

    # Update current user with tenant_id
    await db["users"].update_one(
        {"_id": current_user["id"]},
        {"$set": {"tenant_id": tenant.id}}
    )
    return {"message": "Tenant created", "tenant_id": tenant.id}

@router.get("/tenant/mine")
async def get_my_tenant(current_user=Depends(get_current_user)):
    tenant = await db["tenants"].find_one({"_id": current_user["tenant_id"]})
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant["_id"] = str(tenant["_id"])
    return tenant
