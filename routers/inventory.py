from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

class BaseInventory(BaseModel):
    product_id: int
    location_id: int

class InventoryState(BaseInventory):
    quantity: int

class InventoryAdjustment(BaseInventory):
    adjust: int

_inventory = {}

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not Found"}},
)

def GetKey(location_id: int, product_id: int):
    key = f'{location_id}_{product_id}'
    print('Key='+key)
    return key

def VerifyInventoryExists(location_id: int, product_id: int):
    key = GetKey(location_id, product_id)
    if key not in _inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return key

@router.get("/", response_model=InventoryState)
async def get(location_id: int, product_id: int):
    print(_inventory)
    key = VerifyInventoryExists(location_id, product_id)
    return _inventory[key]
    
@router.put("/")
async def update(inventory: InventoryState):
    key = VerifyInventoryExists(inventory.location_id, inventory.product_id)
    inventory[key] = inventory

@router.post("/")
async def create(inventory: InventoryState):
    """
    Creates a new inventory record for the specified product at the specified location 

    - **product_id**: The Product's ID that is being stored
    - **location_id**: The location's ID where the product will be stored
    - **quantity**:  the initial quantity for this inventory record
    """
    _inventory[GetKey(inventory.location_id, inventory.product_id)] = inventory

@router.delete("/")
async def delete(inventory: BaseInventory):
    key = VerifyInventoryExists(inventory.location_id, inventory.product_id)
    _inventory.pop(key)

@router.put("/adjustment", 
    summary="Adjusts inventory for a product in a location", 
    description="For replishment use a positive __adjust__ value; for sales it should be negative",
    responses={403: {"description": "Cannot remove more stock than is available"}},)
async def adjustment(adjustment: InventoryAdjustment):
    key = VerifyInventoryExists(adjustment.location_id, adjustment.product_id)
    inventory: InventoryState = _inventory[key]
    if adjustment.adjust < 0 and inventory.quantity < -adjustment.adjust:
        raise HTTPException(status_code=403, detail="Invalid stock")

    return _inventory[key]
