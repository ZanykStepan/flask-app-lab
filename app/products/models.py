from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, func, DateTime, Boolean
import sqlalchemy as sa
from typing import List, Optional
from datetime import datetime

class Category(db.Model):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="select"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=sa.true()
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('categories.id', name='fk_products_category_id_categories')
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name} ${self.price}>"