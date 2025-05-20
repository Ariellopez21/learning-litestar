from turtle import title
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin, ScalarRenderPlugin
from litestar.plugins.sqlalchemy import SQLAlchemySyncConfig, SQLAlchemyPlugin

from app.controllers import TagController, TodoController, UserController, TagController, AuthController
from app.models import Base

# TOdo lo que solicitemos, estará incluido en la URL como cuando buscas algo en google y miras la URL.
# CUando se hace un post, se envía la información como de manera implicita.
# EndPoint: funciones con metodo, retorno  y ruta

db_config = SQLAlchemySyncConfig(
    connection_string="sqlite:///db.sqlite3", create_all=True, metadata=Base.metadata
)

sqla_plugin = SQLAlchemyPlugin(config=db_config)

openapi_config = OpenAPIConfig(
    title="Todo API",
    version="0.9.9",
    render_plugins=[SwaggerRenderPlugin(),ScalarRenderPlugin()])

# Una lista de funciones para recibir información de la API
app = Litestar(
    route_handlers=[TodoController, UserController, TagController, AuthController], 
    openapi_config=openapi_config,
    plugins=[sqla_plugin],
    debug=True)