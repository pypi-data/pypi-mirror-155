"""Hand of whist"""
from typing import Optional

from pydantic import BaseModel

from whist.core.cards.card import Card, Suit
from whist.core.cards.card_container import UnorderedCardContainer
from whist.core.error.hand_error import HandAlreadyDealtError
from whist.core.game.play_order import PlayOrder
from whist.core.game.player_at_table import PlayerAtTable
from whist.core.game.trick import Trick
from whist.core.game.warnings import TrickNotDoneWarning
from whist.core.util import enforce_str_on_dict


class Hand(BaseModel):
    """
    Hand of whist.
    """
    tricks: list[Trick] = []
    trump: Optional[Suit] = None

    def done(self) -> bool:
        """
        Check if the hand is done.
        :return: True if the hand is done, else False
        :rtype: bool
        """
        return len(self.tricks) == 13 and self.tricks[-1]

    @property
    def current_trick(self):
        """
        Returns the current trick.
        """
        return self.tricks[-1]

    def deal(self, play_order: PlayOrder) -> Trick:
        """
        Deals the hand and starts the first trick.
        :return: the first trick
        :rtype: Trick
        """
        if len(self.tricks) != 0:
            raise HandAlreadyDealtError()

        deck = UnorderedCardContainer.full()
        card: Optional[Card] = None
        while deck:
            player = play_order.get_next_player()
            card = deck.pop_random()
            player.hand.add(card)
        self.trump = card.suit

        first_trick = Trick(play_order=list(play_order), trump=self.trump)
        self.tricks.append(first_trick)
        return first_trick

    def next_trick(self, play_order: PlayOrder) -> Trick:
        """
        Starts the next trick.
        :return: the next trick
        :rtype: Trick
        """
        if not self.tricks[-1].done:
            raise TrickNotDoneWarning()
        next_trick_order = self._winner_plays_first_card(play_order)
        next_trick = Trick(play_order=list(next_trick_order), trump=self.trump)
        self.tricks.append(next_trick)
        return next_trick

    def dict(self, *args, **kwargs):
        super_dict = super().dict(*args, **kwargs)
        return enforce_str_on_dict(super_dict, ['trump'])

    def _winner_plays_first_card(self, play_order: PlayOrder) -> PlayOrder:
        winner: PlayerAtTable = self.tricks[-1].winner
        return play_order.rotate(winner)
