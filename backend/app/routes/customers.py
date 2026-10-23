"""Customers router — langganan/pelanggan."""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("")
async def list_customers():
    # TODO: query MariaDB (customers table)
    return {"ok": True, "message": "customers endpoint ready"}

@router.post("")
async def create_customer():
    return {"ok": True, "message": "create_customer ready"}
