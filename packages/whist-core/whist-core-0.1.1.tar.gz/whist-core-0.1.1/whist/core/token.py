"""Game access token"""
from datetime import timedelta, datetime

from jose import jwt
from pydantic import BaseModel

from whist.core import SECRET_KEY, ALGORITHM
from whist.core.user.player import Player


class Token(BaseModel):
    """
    Handles jwt based token authentication for players during a game.
    """
    username: str

    @staticmethod
    def create(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        """
        Creates a token string.
        :param data: Payload of the token. Must contain 'sub:<username>'.
        :type data: dictionary
        :param expires_delta: The amount of time until the token expires. Default is 15 minutes.
        :type expires_delta: datetime.timedelta
        :return: the token string
        :rtype: string
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    async def get_user(database: dict, token: str) -> Player:
        """
        Asynchron method. Retrieves the user from a given database by token.
        :param database: Where to look for the user.
        :type database: dictionary
        :param token: From which the user will be extracted.
        :type token: string
        :return: A player instance if the user is found. Or raises a KeyError if the no username
        is in the token. Or raises ValueError if the user not in the database.
        :rtype: Player
        """
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise KeyError('No username in token.')
        token = Token(username=username)
        player = Player.get_player(database, token.username)
        if player is None:
            raise ValueError(f'No user with username: {username} found.')
        return player
