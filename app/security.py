from typing import Any
from litestar.contrib.jwt import OAuth2PasswordBearerAuth, Token
from litestar.connection import ASGIConnection

from app.models import User

async def retrieve_user_handler(token: Token, _: ASGIConnection[Any,Any,Any,Any]) -> User:
    # This function should be implemented to retrieve the user from the database
    # For example, using SQLAlchemy:
    # return db_session.query(User).filter(User.username == username).first()
    return User(id=0,username="test")

oauth2_auth = OAuth2PasswordBearerAuth(
    retrieve_user_handler=retrieve_user_handler,
    token_secret="supersecret",
    token_url="/auth/login",
    exclude=["/auth/login", "/schema"],
)