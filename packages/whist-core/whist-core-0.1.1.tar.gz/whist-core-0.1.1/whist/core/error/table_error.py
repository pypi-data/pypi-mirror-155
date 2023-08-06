"""Errors regarding table logic."""


class TableFullError(Exception):
    """
    Thrown if the table is already full.
    """


class TeamFullError(Exception):
    """
    Thrown if the team is already full.
    """


class TableNotReadyError(Exception):
    """
    Is raised when a table requires all player to be ready, but at least one is not.
    """


class TableNotStartedError(Exception):
    """
    Is raised when a table is expected to have started, but it wasn't. Similar to
    TableNotReadyError.
    """


class PlayerNotJoinedError(Exception):
    """
    Raised if a player has not yet joined the table.
    """
