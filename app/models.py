
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
    tags: Mapped[list["Tag"]] = relationship(back_populates="items", secondary="todo_items_tags")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str] 

    items: Mapped[list["TodoItem"]] = relationship(back_populates="user")

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 

    items: Mapped[list["TodoItem"]] = relationship(back_populates="tags", secondary="todo_items_tags")

class TodoItemTag(Base):
    __tablename__ = "todo_items_tags"

    items: Mapped[int] = mapped_column(ForeignKey("todo_items.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)

    #todo_item: Mapped["TodoItem"] = relationship(back_populates="tags")
    #tag: Mapped["Tag"] = relationship(back_populates="items")