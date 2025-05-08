from litestar import Litestar
from litestar.plugins.sqlalchemy import SQLAlchemySyncConfig, SQLAlchemyPlugin

from app.controllers import TodoController, UserController
from app.models import Base

# TOdo lo que solicitemos, estará incluido en la URL como cuando buscas algo en google y miras la URL.
# CUando se hace un post, se envía la información como de manera implicita.
# EndPoint: funciones con metodo, retorno  y ruta

db_config = SQLAlchemySyncConfig(
    connection_string="sqlite:///db.sqlite3", create_all=True, metadata=Base.metadata
)

sqla_plugin = SQLAlchemyPlugin(config=db_config)

# Una lista de funciones para recibir información de la API
app = Litestar(
    route_handlers=[TodoController, UserController], 
    plugins=[sqla_plugin],
    debug=True)