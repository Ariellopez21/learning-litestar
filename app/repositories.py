from advanced_alchemy.repository import SQLAlchemySyncRepository
from app.models import TodoItem
from sqlalchemy.orm import Session

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

async def provide_todoitem_repo(db_session: Session) -> TodoItemRepository:
    """
    Provide a SQLAlchemySyncRepository for TodoItem.
    """
    return TodoItemRepository(session=db_session)