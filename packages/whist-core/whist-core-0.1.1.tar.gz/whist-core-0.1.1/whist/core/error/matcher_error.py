"""Errors raised during players to team distribution"""


class NotEnoughPlayersError(Exception):
    """
    Is raised when not enough players are joined to fill all teams.
    """
