# logic/routes/bill_route.py
from fastapi import APIRouter, Depends,Request
from logic.handlers.bill_handler import (
    write_bill_handler,
    read_bill_handler,
    update_bill_handler,
    delete_bill_handler,
    read_all_bills_by_status_handler,
    list_customer_bills_handler,
    list_own_bills_handler,
    list_all_bills_handler,
    list_biller_bills_handler,
    read_report_handler,
)
from middleware.auth import get_current_user

bill_routes = APIRouter(
    prefix="/api/v0.1/bills",
    tags=["Bills"]
)

# Protected endpoints for bill operations
@bill_routes.post("/")
async def write_bill_route(request: Request, user=Depends(get_current_user)):
    return await write_bill_handler(request, user)

@bill_routes.get("/{bill_id}")
async def read_bill_route(request: Request, bill_id: str, user=Depends(get_current_user)):
    return await read_bill_handler(request, bill_id, user)

@bill_routes.put("/{bill_id}")
async def update_bill_route(request: Request, bill_id: str, user=Depends(get_current_user)):
    return await update_bill_handler(request, bill_id, user)

@bill_routes.delete("/{bill_id}")
async def delete_bill_route(request: Request, bill_id: str, user=Depends(get_current_user)):
    return await delete_bill_handler(request, bill_id, user)

# Listing and filtering
@bill_routes.get("/status/{status}")
async def read_bills_by_status_route(status: str, user=Depends(get_current_user)):
    return await read_all_bills_by_status_handler(status, user)

@bill_routes.get("/customer/{customer_id}")
async def list_customer_bills_route(customer_id: str, user=Depends(get_current_user)):
    return await list_customer_bills_handler(customer_id, user)

@bill_routes.get("/my-bills")
async def list_own_bills_route(user=Depends(get_current_user)):
    return await list_own_bills_handler(user)

@bill_routes.get("/all")
async def list_all_bills_route(user=Depends(get_current_user)):
    return await list_all_bills_handler(user)

@bill_routes.get("/biller/{biller_id}")
async def list_biller_bills_route(biller_id: str, user=Depends(get_current_user)):
    return await list_biller_bills_handler(biller_id, user)

@bill_routes.get("/report")
async def read_report_route(user=Depends(get_current_user)):
    return await read_report_handler(user)