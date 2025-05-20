from advanced_alchemy.repository import SQLAlchemySyncRepository
from app.models import TodoItem, User, Tag
from sqlalchemy.orm import Session
from litestar.dto import DTOData
from advanced_alchemy.filters import CollectionFilter
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


'''
Qué son las CRUD operations:
    CRUD es un acrónimo que se refiere a las operaciones básicas que se pueden realizar en una base de datos. 
    Estas operaciones son: Crear (Create), Leer (Read), Actualizar (Update) y Eliminar (Delete).
    Estas operaciones son fundamentales para la gestión de datos en aplicaciones web y sistemas de bases de datos.
SQLAlchemySyncRepository implementa las operaciones CRUD de manera sencilla y eficiente.
docs.advanced-alchemy.litestar.dev/reference/repository.html
'''
class TodoItemRepository(SQLAlchemySyncRepository[TodoItem]):
    model_type = TodoItem
    def add_with_tags(self, todo_item: TodoItem, tags_repo: "TagRepository",**kwargs) -> TodoItem :
        todo_item.tags = tags_repo.list(
        CollectionFilter("id", [t.id for t in todo_item.tags])
            )
            
        return self.add(todo_item, **kwargs)

async def provide_todoitem_repo(db_session: Session) -> TodoItemRepository:
    """
    Provide a SQLAlchemySyncRepository for TodoItem.
    """
    return TodoItemRepository(session=db_session)

class UserRepository(SQLAlchemySyncRepository[User]):
    model_type = User

    def add_with_password_hash(self, user: User, **kwargs) -> User:
        user.password = password_hasher.hash(user.password)
        return self.add(user, **kwargs)

    def check_password(self, username: str, password: str) -> bool:
        user = self.get(username, id_attribute="username")
        return password_hasher.verify(password, user.password)

async def provide_user_repo(db_session: Session) -> UserRepository:
    return UserRepository(session=db_session)

class TagRepository(SQLAlchemySyncRepository[Tag]):
    model_type = Tag

async def provide_tag_repo(db_session: Session) -> TagRepository:
    return TagRepository(session=db_session)