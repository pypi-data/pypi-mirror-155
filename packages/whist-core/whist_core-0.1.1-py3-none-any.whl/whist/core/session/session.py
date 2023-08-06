"""DTO of a game room"""
from pydantic import BaseModel

from whist.core.session.userlist import UserList


class Session(BaseModel):
    """
    User can join to play a game of Whist.
    """
    name: str
    users: UserList = UserList()
