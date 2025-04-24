from typing import Sequence
#from dataclasses import dataclass
#from litestar import put, delete, patch, Router
from litestar import get, post, Controller, patch

from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.models import TodoItem 
from app.dtos import TodoItemReadDTO, TodoItemCreateDTO, TodoItemUpdateDTO

'''
Bases:
GET: Para obtener resultados
POST: Para enviar resultados
PUT: Para actualizar
PATCH: Para actualizar parcialmente
DELETE: Para eliminar
DATA: Siempre incluir este parametro en las funciones para que se pueda utilizar el json del Litestar
DataTransferObjects (DTOs): Son clases que se utilizan para definir la estructura de los datos que se envían y reciben en las peticiones HTTP.
En vez de utilizar un return por cada función. se puede añadir como atributo de la clase.
En la función post usamos dto para entrada de datos y en la función get usamos return_dto para salida de datos.
'''

class TodoController(Controller):
    path = '/items'
    return_dto=TodoItemReadDTO

    @get("/")
    async def list_items(self, db_session: Session, done: bool | None = None) -> Sequence[TodoItem]:
        stmt = select(TodoItem)
        if done is not None:
            stmt = stmt.filter(TodoItem.done == done)
        return db_session.execute(stmt).scalars().all()

    @post("/", dto=TodoItemCreateDTO)
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
    
    @patch("/{item_id:int}", dto=TodoItemUpdateDTO)
    async def update_item(self, item_id: int, data: DTOData[TodoItem], db_session: Session) -> TodoItem | None:
        data_dict = data.as_builtins()
        item = db_session.execute(select(TodoItem).where(TodoItem.id == item_id)).scalar_one_or_none()
        for field in ("title", "done"):
            if field in data_dict is not None:
                setattr(item, field, data_dict[field])
        db_session.commit()

        return item

'''
    @put("/{item_id:int}")
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