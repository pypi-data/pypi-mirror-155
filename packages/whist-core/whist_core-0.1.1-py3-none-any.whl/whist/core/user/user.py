"""DTO of user"""

from pydantic import BaseModel


class User(BaseModel):
    """
    Represents a user connected to the server.
    """
    username: str
