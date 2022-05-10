from unicodedata import category
from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Product, ProductReadDTO, Category, ProductUpdateDTO
from app.models import ProductCreateDTO, ProductReadDTO

app = FastAPI()

@app.get("/products", response_model=list[ProductReadDTO])
async def get_products(session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(Product))
    products = query.scalars()
    return [ProductReadDTO(name = p.name, price = p.price, description = p.description, id=p.id) for p in products]

@app.post("/products", response_model=ProductReadDTO)
async def create_product(product: ProductCreateDTO, session: AsyncSession = Depends(get_session)):
    cat = await session.execute(select(Category).where(Category.id == product.category))
    to_create = Product(name = product.name, description = product.description, price = product.price, category_id = cat.id)
    session.add(to_create)
    await session.commit()
    await session.refresh(to_create)
    return ProductReadDTO(name = to_create.name, description = to_create.description, id = to_create.id, price = to_create.price)

@app.put("/products/{product_id}", response_model=ProductReadDTO)
async def update_product(product_id: int, product: ProductUpdateDTO, session: AsyncSession = Depends(get_session)):
    to_update = session.execute(select(Product).where(Product.id == product_id))
    to_update.description = product.description
    to_update.price = product.price
    to_update.name = product.name
    session.add(to_update)
    await session.commit()
    await session.refresh(to_update)
    return ProductReadDTO(name = to_update.name, description = to_update.description, id = to_update.id, price = to_update.price)

@app.delete("/products/{product_id}", response_model=ProductReadDTO)
async def delete_product(product_id: int , session: AsyncSession = Depends(get_session)):
    to_delete = session.execute(select(Product).where(Product.id == product_id))
    session.delete(to_delete)
    await session.commit()
    return ProductReadDTO(name = to_delete, description = to_delete.description, id = to_delete.id, price = to_delete.price)

    

