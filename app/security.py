from typing import Any
from litestar.contrib.jwt import OAuth2PasswordBearerAuth, Token
from litestar.connection import ASGIConnection
from litestar.repository import NotFoundError
from litestar.exceptions import NotFoundException

from app.models import User
from app.db import db_config
from app.repositories import UserRepository
from app.config import settings

async def retrieve_user_handler(token: Token, _: ASGIConnection[Any,Any,Any,Any]) -> User:
    # This function should be implemented to retrieve the user from the database
    # For example, using SQLAlchemy:
    # return db_session.query(User).filter(User.username == username).first()

    session_maker = db_config.create_session_maker()
    try:
        with session_maker() as session:
            users_repo = UserRepository(session=session)
            return users_repo.get_one(username=token.sub)
    except NotFoundError as e:
        raise NotFoundException(f"User with id {token.sub} not found") from e

oauth2_auth = OAuth2PasswordBearerAuth(
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.secret_key.get_secret_value(),
    token_url="/auth/login",
    exclude=["/auth/login", "/schema"],
)