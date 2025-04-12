from backend.database import db

def get_tenant_collection(tenant_id: str, base_name: str):
    return db[f"{tenant_id}_{base_name}"]
