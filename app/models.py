from pip import List
from sqlmodel import Field, Relationship, Session, SQLModel
from typing import Optional

class BaseEntity(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductBase(BaseEntity):
    name: str = Field(index=True)
    price: float = Field(index=True)
    description: str = Field(index=True)

class Product(ProductBase, table=True):
    name: str = Field(index=True)
    price: float = Field(index=True)
    description: str = Field(index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

class ProductReadDTO(ProductBase):
    id: int 

class ProductCreateDTO(ProductBase):
    category: int

class ProductUpdateDTO(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

class Category(BaseEntity, table=True):
    description: str = Field(index=True)
