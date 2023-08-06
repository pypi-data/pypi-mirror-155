"""Exceptions called from Hands."""


class HandAlreadyDealtError(Exception):
    """
    Is raised when hand is requested to deal a second time.
    """
