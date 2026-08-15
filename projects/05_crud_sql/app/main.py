from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .database import AsyncSessionLocal, init_db
from . import models
from .schemas import ProductCreate, ProductOut, ProductUpdate

app = FastAPI(title="CRUD Productos")


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, session: AsyncSession = Depends(get_session)):
    product = models.Product(**payload.dict())
    session.add(product)
    try:
        await session.commit()
        await session.refresh(product)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Integrity error: %s" % str(e))
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Server error")
    return product


@app.get("/products", response_model=List[ProductOut])
async def list_products(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Product).order_by(models.Product.id))
    products = result.scalars().all()
    return products


@app.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, payload: ProductUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(product, field, value)
    try:
        await session.commit()
        await session.refresh(product)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Could not update product")
    return product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        await session.delete(product)
        await session.commit()
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Could not delete product")
    return None
