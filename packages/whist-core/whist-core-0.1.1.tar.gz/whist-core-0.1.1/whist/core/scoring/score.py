"""
Result after one hand.
"""
from typing import Any

from pydantic import BaseModel

from whist.core.scoring.team import Team


class Score(BaseModel):
    """
    Score of a hand being played.
    """
    hand_score: dict = {}

    def __init__(self, teams: list[Team], scores: list[int], **data: Any):
        super().__init__(**data)
        for team, score in zip(teams, scores):
            self.hand_score.update({team: score})
            team.games_played()

    def __getitem__(self, item):
        return self.hand_score[item]

    @property
    def winner(self) -> Team:
        """
        Returns the winner team.
        :rtype: Team
        """
        return max(self.hand_score.items(), key=lambda x: x[1])[0]

    def won(self, team: Team) -> bool:
        """
        Check if the team won that round.
        :param team: Team for which to check if has won.
        :type team: Team
        :return: True if won, else false
        :rtype: bool
        """
        return self.hand_score[team] == max(self.hand_score.values())
