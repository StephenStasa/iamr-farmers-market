from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    code: str
    name: Optional[str]

_products = {}
_next_id = 1

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/")
async def all():
    return list(_products.values())

@router.get("/{id}")
async def get(id: int):
    if id not in _products:
        raise HTTPException(status_code=404, detail="Item not found")
    return _products[id]
    
@router.put("/{id}")
async def update(id: int, product: Product):
    if id not in _products:
        raise HTTPException(status_code=404, detail="Item not found")
    _products[id] = product

@router.post("/")
async def create(product: Product):
    global _next_id
    id = _next_id
    _next_id += 1
    _products[id] = product
    return {"id": id}

@router.delete("/{id}")
async def delete(id: int):
    if id not in _products:
        raise HTTPException(status_code=404, detail="Item not found")
    _products.pop(id)
