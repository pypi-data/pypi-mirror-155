"""
Data wrapper of player stati.
"""

# Wrapper class
# pylint: disable=too-few-public-methods
from pydantic import BaseModel


class Status(BaseModel):
    """
    Player status a table.
    """
    ready: bool = False
    team: int = None
