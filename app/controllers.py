from litestar import get, post, Controller, patch, delete 
#from dataclasses import dataclass
#from litestar import put, delete, patch, Router

from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.filters import ComparisonFilter, CollectionFilter

from typing import Sequence

from app.models import TodoItem 
from app.dtos import TodoItemReadDTO, TodoItemCreateDTO, TodoItemUpdateDTO
from app.repositories import TodoItemRepository, provide_todoitem_repo

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
    dependencies = {
        "todoitem_repo": Provide(provide_todoitem_repo)
    }
    @get("/")
    async def list_items(self, todoitem_repo: TodoItemRepository, done: bool | None = None) -> Sequence[TodoItem]:
        #return todoitem_repo.list(CollectionFilter("done", [done]))
        if done is None:
            return todoitem_repo.list()
        return todoitem_repo.list(ComparisonFilter("done", "eq", done))

    @post("/", dto=TodoItemCreateDTO)
    async def add_todo(self, db_session: Session, data: TodoItem) -> Sequence[TodoItem]:
        with db_session.begin():
            db_session.add(data)
        return db_session.execute(select(TodoItem)).scalars().all()
    
    @get("/{item_id:int}")
    async def get_item(self, item_id: int, todoitem_repo: TodoItemRepository) -> TodoItem:
        try:
            return todoitem_repo.get(item_id)
        except NotFoundError:
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

    @delete("/{item_id:int}")
    async def delete_item(self, item_id: int, todoitem_repo: TodoItemRepository) -> None:
        todoitem_repo.delete(item_id)
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