from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

from routers import product
from routers import inventory

description = """
Stephen Stasa's demo application for a simulated Farmer's Market

### Implemented
* **Products** CRUD operations
* **Inventory** CRUD and adjustment operations


"""

tags_metadata = [
    {
        "name": "products",
        "description": "Operations with products.",
    },
    {
        "name": "inventory",
        "description": "Manage item inventory. Includes operations to add products to locations and adjust for replenishment and sales",
    },
]

app = FastAPI(description=description,
    openapi_tags=tags_metadata)

app.include_router(product.router)
app.include_router(inventory.router)

@app.get("/", response_class=RedirectResponse)
async def redirect_fastapi():
    return "/docs"