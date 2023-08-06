"""One Game of whist"""
from typing import Optional

from pydantic import BaseModel

from whist.core.game.hand import Hand
from whist.core.game.play_order import PlayOrder
from whist.core.game.player_at_table import PlayerAtTable
from whist.core.scoring.score import Score
from whist.core.scoring.score_card import ScoreCard
from whist.core.scoring.team import Team
from whist.core.user.player import Player


class Game(BaseModel):
    """
    One Game of whist.
    """

    play_order: PlayOrder
    win_score: int = 3
    score_card: ScoreCard = ScoreCard()
    current_hand: Optional[Hand] = None

    # pylint: disable=too-few-public-methods
    class Config:
        """
        Enables to have non models as field types and sets the encoder for play order.
        """
        arbitrary_types_allowed = True

    def next_hand(self) -> Hand:
        """
        Checks if the current hand is done and if so will return the next hand. If not it will
        return the current hand.
        :rtype: Hand
        """
        if self.current_hand is None:
            self.current_hand = Hand()
        elif self.current_hand.done():
            score = self._calc_score()
            self.score_card.add_score(score)
            self._next_play_order()
            self.current_hand = Hand()
        return self.current_hand

    def _calc_score(self):
        tricks_won = [0, 0]
        for trick in self.current_hand.tricks:
            winner = trick.winner
            tricks_won[winner.team] += 1
        tricks_won = [max(0, trick_score - 6) for trick_score in tricks_won]
        players_by_team = [[], []]
        for player in self.play_order:
            players_by_team[player.team].append(player.player)
        teams = [Team(players=players) for players in players_by_team]
        score = Score(teams=teams, scores=tricks_won)
        return score

    @property
    def current_trick(self):
        """
        Returns the current trick of the current hand.
        """
        try:
            return self.next_hand().current_trick
        except IndexError:
            return self.next_hand().deal(self.play_order)

    @property
    def done(self):
        """
        Check if game is done.
        :return: True if done else false
        :rtype: bool
        """
        return self.win_score <= self.score_card.max

    def get_player(self, player: Player) -> PlayerAtTable:
        """
        Retrieves the PlayerAtTable for the player given.
        :param player: who needs it's counterpart at the table
        :return: the player at table
        """
        return self.play_order.get_player(player)

    def _next_play_order(self) -> None:
        """
        Creates the next order of player for next hand.
        """
        self.play_order = self.play_order.next_order()
