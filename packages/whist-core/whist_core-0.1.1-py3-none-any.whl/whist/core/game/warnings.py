"""Warnings during game phase."""


class TrickNotDoneWarning(Warning):
    """The current trick is not done yet."""


class ServSuitFirstWarning(Warning):
    """Player must serv the suit of the lead."""
