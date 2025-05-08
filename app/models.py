
from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class TodoItem(Base):
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(primary_key=True) 
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    user: Mapped[Optional["User"]] = relationship(back_populates="items")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str] 

    items: Mapped[list["TodoItem"]] = relationship(back_populates="user")
