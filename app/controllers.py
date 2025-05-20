from enum import auto
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

from app.models import TodoItem, User, Tag
from app.dtos import TodoItemReadDTO, TodoItemCreateDTO, TodoItemUpdateDTO, UserReadDTO, UserReadFullDTO, TodoItemReadFullDTO, TagReadDTO, UserCreateDTO
from app.repositories import TodoItemRepository, provide_todoitem_repo, UserRepository, provide_user_repo, TagRepository, provide_tag_repo

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
    tags = ["items"]
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
    @post("/", dto=TodoItemCreateDTO, dependencies={"tags_repo": Provide(provide_tag_repo)})
    async def add_todo(self, todoitem_repo: TodoItemRepository, tags_repo: TagRepository, data: TodoItem) -> TodoItem:
        return todoitem_repo.add_with_tags(data, tags_repo, auto_commit=True)
       
    @get("/{item_id:int}")
    async def get_item(self, item_id: int, todoitem_repo: TodoItemRepository) -> TodoItem:
        try:
            return todoitem_repo.get(item_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"El item con id={item_id} no existe.")
    
    @get("/{item_id:int}/full", return_dto=TodoItemReadFullDTO)
    async def get_item_full(self, todoitem_repo: TodoItemRepository, item_id: int) -> TodoItem:
        try:
            return todoitem_repo.get(item_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"El user con id={item_id} no existe.")
            

    @patch("/{item_id:int}", dto=TodoItemUpdateDTO)
    async def update_item(self, todoitem_repo: TodoItemRepository, item_id: int, data: DTOData[TodoItem]) -> TodoItem | None:
        item, _ = todoitem_repo.get_and_update(match_fields="id", id=item_id, **data.as_builtins(), auto_commit=True)       
        return item

    @delete("/{item_id:int}")
    async def delete_item(self, item_id: int, todoitem_repo: TodoItemRepository) -> None:
        todoitem_repo.delete(item_id, auto_commit=True)

class UserController(Controller):
    path = '/users'
    tags = ["users"]
    return_dto = UserReadDTO
    dependencies = {
        "user_repo": Provide(provide_user_repo)
    }
    @get("/")
    async def list_users(self, user_repo: UserRepository) -> Sequence[User]:
        return user_repo.list()
    @get("/{user_id:int}")
    async def get_user(self, user_repo: UserRepository, user_id: int) -> User:
        try:
            return user_repo.get(user_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"El user con id={user_id} no existe.")
    @get("/{user_id:int}/full", return_dto=UserReadFullDTO)
    async def get_user_full(self, user_repo: UserRepository, user_id: int) -> User:
        try:
            return user_repo.get(user_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"El user con id={user_id} no existe.")
    @post("/", dto=UserCreateDTO)
    async def add_user(self, user_repo: UserRepository, data: User) -> User:
        return user_repo.add_with_password_hash(data, auto_commit=True)
class TagController(Controller):
    path = '/tags'
    tags = ["tags"]
    return_dto = TagReadDTO
    dependencies = {
        "tag_repo": Provide(provide_tag_repo)
    }
    @get("/")
    async def list_tags(self, tag_repo: TagRepository) -> Sequence[Tag]:
        return tag_repo.list()
    @get("/{tag_id:int}")
    async def get_tag(self, tag_repo: TagRepository, tag_id: int) -> Tag:
        try:
            return tag_repo.get(tag_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"El tag con id={tag_id} no existe.")
        

class AuthController(Controller):
    path = "/auth"
    tags = ["auth"]

    @post("/login", dependencies={"user_repo": Provide(provide_user_repo)})
    async def login(self, username: str, password: str, user_repo: UserRepository) -> dict:
        password_valid = user_repo.check_password(username,password)

        return {"valid": password_valid}