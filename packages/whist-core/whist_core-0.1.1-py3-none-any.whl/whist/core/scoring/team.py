"""DAO of team."""
from pydantic import BaseModel

from whist.core.user.player import Player


class Team(BaseModel):
    """
    Data wrapper for a team.
    """
    players: list[Player]

    def __hash__(self):
        return hash(tuple(self.players))

    @property
    def rating(self) -> float:
        """
        The average Elo-Rating of the team members.
        :return: average team rating
        :rtype: float
        """
        return sum(player.rating for player in self.players) / len(self.players)

    def games_played(self, amount: int = 1) -> None:
        """
        Increases the games played counter for each team member.
        :param amount: The amount of new games played. Default 1
        :type amount: int
        :return: None
        :rtype: None
        """
        for player in self.players:
            player.games += amount
