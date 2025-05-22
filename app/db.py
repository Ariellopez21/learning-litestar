# TOdo lo que solicitemos, estará incluido en la URL como cuando buscas algo en google y miras la URL.
# CUando se hace un post, se envía la información como de manera implicita.
# EndPoint: funciones con metodo, retorno  y ruta

from app.models import Base
from app.config import settings

from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig


db_config = SQLAlchemySyncConfig(
    connection_string=settings.database_url, create_all=True, metadata=Base.metadata
)
sqla_plugin = SQLAlchemyPlugin(config=db_config)