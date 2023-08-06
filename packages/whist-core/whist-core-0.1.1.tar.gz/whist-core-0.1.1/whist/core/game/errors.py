"""Errors in game phase"""
from whist.core.user.player import Player


class CardNotInHandError(Exception):
    """
    Raised when a player tries to play a card, that is not in their hand.
    """


class NotPlayersTurnError(Exception):
    """
    Raised when players tries to play although is not their turn.
    """

    def __init__(self, player: Player, turn_player: Player):
        super().__init__()
        self.message = f'Is not {player} turn, but {turn_player}.'


class NoTrumpSelectedError(Exception):
    """
    Raised when no trump is selected for hand.
    """


class TrickDoneError(Exception):
    """
    Raised when the trick is already done.
    """
