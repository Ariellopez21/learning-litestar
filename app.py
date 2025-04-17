# Litestar es la base con la que se levanta la aplicacion
from http.client import HTTPException
from typing import Sequence
from dataclasses import dataclass
from litestar import Litestar, get, post, put, delete, patch, Controller, Router
from litestar.exceptions import HTTPException
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from litestar.plugins.sqlalchemy import SQLAlchemySyncConfig, SQLAlchemyPlugin
from sqlalchemy import select, String
from sqlalchemy.exc import NoResultFound

class Base(DeclarativeBase):
    pass

class TodoItem(Base):
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(primary_key=True) 
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool]    
    
'''
@dataclass
class TodoItem:
    id: int
    title: str
    done: bool

@dataclass
class TodoItemUpdate:
    title: str | None = None
    done: bool | None = None


TODO_LIST: list[TodoItem] = [
    TodoItem(id=1, title="Aprender Python", done=True),
    TodoItem(id=2,title="Aprender SQLAlchemy", done=True),
    TodoItem(id=3,title="Aprender Litestar", done=False),
]
'''
class TodoController(Controller):
    path = '/items'

    @get("/")
    async def list_items(self, db_session: Session, done: bool | None = None) -> Sequence[TodoItem]:
        stmt = select(TodoItem)
        if done is not None:
            stmt = stmt.filter(TodoItem.done == done)
        return db_session.execute(stmt).scalars().all()

    @post("/")
    async def add_todo(self, db_session: Session, data: TodoItem) -> Sequence[TodoItem]:
        with db_session.begin():
            db_session.add(data)
        return db_session.execute(select(TodoItem)).scalars().all()
    
    @get("/{item_id:int}")
    async def get_item(self, item_id: int, db_session: Session) -> TodoItem:

        try:
            stmt = select(TodoItem).where(TodoItem.id == item_id)

            return db_session.execute(stmt).scalar_one()
        
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"El item con id={item_id} no existe.")
'''
    @put("/{item_id: int}")
    async def update_item(self, item_id: int, data: TodoItem) -> list[TodoItem]:
        for t in TODO_LIST:
            if t.id == item_id:
                t.title = data.title
                t.done = data.done
        return TODO_LIST

    @patch("/{item_id: int}")
    async def patch_item(self, item_id: int, data: TodoItemUpdate) -> list[TodoItem]:
        for t in TODO_LIST:
            if t.id == item_id:
                if data.title is not None:
                    t.title = data.title
                if data.done is not None:
                    t.done = data.done
                break
        return TODO_LIST


    @delete("/{item_id: int}") 
    async def delete_item(self, item_id: int) -> None:
        for t in TODO_LIST:
            if t.id == item_id:
                TODO_LIST.remove(t)
        

'''
'''
todo_router = Router(
    path="/items/",
    route_handlers=[get_list, add_todo, update_item, patch_item, delete_item]
)
app = Litestar(route_handlers=[hello_world, todo_router])
'''

# TOdo lo que solicitemos, estará incluido en la URL como cuando buscas algo en google y miras la URL.
# CUando se hace un post, se envía la información como de manera implicita.
# EndPoint: funciones con metodo, retorno  y ruta
@get("/")
async def hello_world() -> str:
    return "Hello, world!"

db_config = SQLAlchemySyncConfig(
    connection_string="sqlite:///db.sqlite3", create_all=True, metadata=Base.metadata
)

sqla_plugin = SQLAlchemyPlugin(config=db_config)

# Una lista de funciones para recibir información de la API
app = Litestar(
    route_handlers=[hello_world, TodoController], 
    plugins=[sqla_plugin],
    debug=True)