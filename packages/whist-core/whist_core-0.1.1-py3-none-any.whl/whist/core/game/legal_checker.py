"""Checks the legality of a move."""
from typing import Optional

from whist.core.cards.card import Card
from whist.core.cards.card_container import UnorderedCardContainer


# pylint: disable=too-few-public-methods
class LegalChecker:
    """
    Static legal checker.
    """

    @staticmethod
    def check_legal(hand: UnorderedCardContainer, card: Card, first: Optional[Card]) -> bool:
        """
        Checks if move is legal.
        :param hand: of the current player
        :param card: the card which should be played next
        :param first: the first played card, can be None if no card has been played
        :return: True if legal else false
        """
        first_card_played = first is not None
        if not first_card_played:
            return True
        if card.suit == first.suit:
            return True
        return not hand.contains_suit(first.suit)
