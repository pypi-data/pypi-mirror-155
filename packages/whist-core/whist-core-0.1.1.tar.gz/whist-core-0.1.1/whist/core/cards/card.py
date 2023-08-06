"""Card related classes"""

from enum import Enum
from functools import total_ordering
from typing import Any, Optional, Iterator

from pydantic import BaseModel

from whist.core.util import enforce_str_on_dict


@total_ordering
class _CardEnum(Enum):
    def __new__(cls, *args) -> '_CardEnum':
        obj = object.__new__(cls)
        obj._value_ = args[0]
        # pylint: disable=protected-access, unused-private-member
        obj.__ordinal = len(cls.__members__)
        return obj

    def __init__(self, _: str, short_name: Optional[str] = None):
        self.__short_name = short_name

    @classmethod
    def _missing_(cls, value: Any) -> Optional['_CardEnum']:
        if isinstance(value, int):
            try:
                return list(cls.__members__.values())[value]
            except IndexError:
                pass
        elif isinstance(value, str):
            for member in cls.__members__.values():
                if value in (member.long_name, member.short_name):
                    return member

        return None

    @property
    def ordinal(self) -> int:
        """
        Get the ordinal.

        :return: ordinal
        """
        return self.__ordinal

    @property
    def long_name(self) -> str:
        """
        Get the long version of the name.

        :return: long version of name
        """
        return self.value

    @property
    def short_name(self) -> str:
        """
        Get the short version of the name.

        :return: short version of name
        """
        return self.__short_name

    def __lt__(self, other: Any) -> bool:
        if self.__class__ is other.__class__:
            return self.ordinal < other.ordinal
        return NotImplemented

    def __str__(self) -> str:
        return self.value


class Suit(_CardEnum):
    """Suits in a playing card deck"""

    CLUBS = ('clubs', '♣')
    DIAMONDS = ('diamonds', '♦')
    HEARTS = ('hearts', '♥')
    SPADES = ('spades', '♠')


class Rank(_CardEnum):
    """Ranks in a playing card deck"""

    NUM_2 = '2'
    NUM_3 = '3'
    NUM_4 = '4'
    NUM_5 = '5'
    NUM_6 = '6'
    NUM_7 = '7'
    NUM_8 = '8'
    NUM_9 = '9'
    NUM_10 = '10'
    J = ('jack', 'J')
    Q = ('queen', 'Q')
    K = ('king', 'K')
    A = ('ace', 'A')


@total_ordering
class Card(BaseModel):
    """A playing card"""

    suit: Suit
    rank: Rank

    # pylint: disable=too-few-public-methods
    class Config:
        """
        Configuration class for base model to make it immutable and hashable.
        """
        frozen = True

    @staticmethod
    def all_cards() -> Iterator['Card']:
        """
        Get iterator of all cards.

        :return: all cards
        """
        return (Card(suit=suit, rank=rank) for suit in Suit for rank in Rank)

    @property
    def short_name(self) -> str:
        """
        Get the short name of this card.

        :return: short name
        """
        short_name = self.rank.short_name \
            if self.rank.short_name is not None \
            else self.rank.long_name
        return f'{self.suit.short_name}{short_name}'

    @property
    def name(self) -> str:
        """
        Get the name of this card.

        :return: name
        """
        return f'{self.rank} of {self.suit}'

    def dict(self, *args, **kwargs):
        super_dict = super().dict(*args, **kwargs)
        return enforce_str_on_dict(super_dict, ('suit', 'rank'))

    def __lt__(self, other: Any) -> bool:
        if self.__class__ is other.__class__:
            return (self.suit, self.rank) < (other.suit, other.rank)
        return NotImplemented

    def __str__(self) -> str:
        return self.name
