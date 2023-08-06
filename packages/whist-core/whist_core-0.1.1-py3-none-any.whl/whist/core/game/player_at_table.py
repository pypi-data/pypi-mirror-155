"""Player instance during the game phase."""
from pydantic import BaseModel

from whist.core.cards.card_container import UnorderedCardContainer
from whist.core.user.player import Player


class PlayerAtTable(BaseModel):
    """
    Wraps the current hand and player instance.
    """
    player: Player
    hand: UnorderedCardContainer
    team: int

    def __eq__(self, other):
        if not isinstance(other, PlayerAtTable):
            return False
        return self.player == other.player

    def __repr__(self):
        return f'PlayerAtTable: {self.player}'
