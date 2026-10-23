"""Invoices router — tagihan."""
from fastapi import APIRouter

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.get("")
async def list_invoices():
    return {"ok": True, "message": "invoices endpoint ready"}

@router.post("")
async def create_invoice():
    return {"ok": True, "message": "create_invoice ready"}

@router.get("/{invoice_id}")
async def get_invoice(invoice_id: int):
    return {"ok": True, "invoice_id": invoice_id}

@router.post("/{invoice_id}/pay")
async def pay_invoice(invoice_id: int):
    return {"ok": True, "message": f"mark invoice {invoice_id} as paid"}
