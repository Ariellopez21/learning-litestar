from advanced_alchemy.extensions.litestar import SQLAlchemyDTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from app.models import TodoItem

'''
DataTransferObjects (DTOs): Son clases que se utilizan para definir la estructura de los datos que se envían y reciben en las peticiones HTTP.

Es para manipular entradas y salidas
'''
class TodoItemReadDTO(SQLAlchemyDTO[TodoItem]):
    #config = SQLAlchemyDTOConfig(exclude={"id"})
    pass

class TodoItemCreateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"id"})

class TodoItemUpdateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"id"}, partial=True,)


'''
Es para manipular entradas y salidas
'''