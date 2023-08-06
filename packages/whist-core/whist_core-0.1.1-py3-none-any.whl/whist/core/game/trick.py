"""Trick implementation"""
from pydantic import BaseModel

from whist.core.cards.card import Card, Suit
from whist.core.cards.card_container import OrderedCardContainer
from whist.core.game.errors import NotPlayersTurnError, TrickDoneError, CardNotInHandError
from whist.core.game.legal_checker import LegalChecker
from whist.core.game.player_at_table import PlayerAtTable
from whist.core.game.warnings import TrickNotDoneWarning, ServSuitFirstWarning
from whist.core.util import enforce_str_on_dict


class Trick(BaseModel):
    """
    One round of where every player plays one card.
    """
    play_order: list[PlayerAtTable]
    stack: OrderedCardContainer = OrderedCardContainer.empty()
    trump: Suit

    @property
    def done(self) -> bool:
        """
        Is the trick done.
        :return: True if trick is done else false.
        :rtype: bool
        """
        return len(self.stack) == len(self.play_order)

    @property
    def winner(self) -> PlayerAtTable:
        """
        Player how won the trick.
        :return: Player instance of the winner if the trick is done.
        Else raises TrickNotDoneWarning
        :rtype: Player
        """
        if not self.done:
            raise TrickNotDoneWarning()
        turn, _ = self.stack.get_turn_and_winner_card(self.trump)
        return self.play_order[turn]

    def play_card(self, player: PlayerAtTable, card: Card) -> None:
        """
        One player plays one card. Which is put on top of the stack.
        :param player: Player who wants to play a card.
        :type player: Player
        :param card: Card which the player wants to play.
        :type card: Card
        :return: None if successful, else raises TrickDoneError if every player already played a
        card.
        Or NotPlayersTurnError if a player attempts to play card although it is not they turn.
        :rtype: None
        """
        turn = len(self.stack)
        if turn == len(self.play_order):
            raise TrickDoneError()
        if player != self.play_order[turn]:
            raise NotPlayersTurnError(player.player, self.play_order[turn].player)
        if not LegalChecker.check_legal(player.hand, card, self.stack.first):
            raise ServSuitFirstWarning()
        if card not in player.hand:
            raise CardNotInHandError(f'{card} is not in {player}\'s hand')

        self.stack.add(card)
        player.hand.remove(card)

    def dict(self, *args, **kwargs):
        super_dict = super().dict(*args, **kwargs)
        return enforce_str_on_dict(super_dict, {'trump'})
