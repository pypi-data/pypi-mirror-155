"""DAO of user."""
from typing import Optional

from whist.core.user.user import User


class Player(User):
    """
    This is the server side class of an user.
    """
    games: int = 0
    rating: int

    def __str__(self):
        return self.username

    def __hash__(self):
        return hash(self.username)

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return other.username == self.username

    @staticmethod
    def get_player(database: dict, username: str) -> Optional['Player']:
        """
        Returns a player for a given username if they are in the given database.
        :param database: where to look for the user
        :type database: dictionary
        :param username: the name of the user to look for
        :type username: string
        :return: The player instance or None
        :rtype: Player or None
        """
        if username in database:
            return database[username]
        return None
