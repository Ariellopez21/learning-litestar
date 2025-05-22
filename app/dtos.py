from advanced_alchemy.extensions.litestar import SQLAlchemyDTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from app.models import TodoItem, User, Tag

'''
DataTransferObjects (DTOs): Son clases que se utilizan para definir la estructura de los datos que se envían y reciben en las peticiones HTTP.

Es para manipular entradas y salidas

En estos casos se utiliza para esconder el campo id, ya que no es necesario que el cliente lo envíe al crear un nuevo elemento.

'''
class TodoItemReadDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"user"})

class TodoItemReadFullDTO(SQLAlchemyDTO[TodoItem]):
    pass
class TodoItemCreateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"id", "user", "user_id"}, partial=True)

class TodoItemUpdateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"id", "user","user_id"}, partial=True,)

class UserReadDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"items", "password"})

class UserLoginDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(include={"username", "password"})

class UserReadFullDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password"})

class UserCreateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"items", "id"})

class TagReadDTO(SQLAlchemyDTO[Tag]):
    pass