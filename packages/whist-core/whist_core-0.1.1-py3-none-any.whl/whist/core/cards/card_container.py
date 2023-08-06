"""Extraction of common methods for class that contains a set of cards"""
import abc
import random
from typing import Iterator, Optional

from pydantic import BaseModel, PrivateAttr

from whist.core.cards.card import Card, Suit


class CardContainer(BaseModel, abc.ABC):
    """
    Abstract Base Class for card containers. Duplicate cards are not allowed.
    """

    cards: tuple[Card, ...]

    # pylint: disable=too-few-public-methods
    class Config:
        """
        Configuration class for base model to make it immutable.
        """
        allow_mutation = False

    @classmethod
    def empty(cls) -> 'CardContainer':
        """
        Creates an empty card container.

        :return: empty ard container
        :rtype: correct subtype of CardContainer
        """
        return cls(cards=())

    @classmethod
    def with_cards(cls, *cards) -> 'CardContainer':
        """
        Creates a card container with the given cards.

        :param cards: cards to add
        :return: card container with given cards
        :rtype: correct subtype of CardContainer
        """
        if len(cards) == 1 and not isinstance(cards[0], Card):
            cards = cards[0]
        return cls(cards=cards)

    @classmethod
    def full(cls) -> 'CardContainer':
        """
        Create a full card container.

        :return: full card container
        :rtype: correct subtype of CardContainer
        """
        return cls(cards=Card.all_cards())

    def pop_random(self) -> Card:
        """
        Removes one random card from card container.

        :return: A card from deck.
        """
        card = random.choice(self.cards)
        self.remove(card)
        return card

    def __contains__(self, card: Card) -> bool:
        return card in self.cards

    def __len__(self):
        return len(self.cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def __str__(self) -> str:
        return str(self.cards)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(cards={self.cards!r})'

    def remove(self, card: Card) -> None:
        """
        Remove a card from this container.

        :param card: card to remove
        """
        if not isinstance(card, Card):
            raise ValueError(f'cannot remove {card} of type {type(card)} from card container')
        if card not in self:
            raise ValueError(f'{card} not in card container')
        self._remove_impl(card)

    @abc.abstractmethod
    def _remove_impl(self, card: Card) -> None:
        raise NotImplementedError

    def add(self, card: Card) -> None:
        """
        Add a card to this container.

        :param card: card to add
        """
        if not isinstance(card, Card):
            raise ValueError(f'cannot add {card} of type {type(card)} to card container')
        if card in self:
            raise ValueError(f'{card} already in card container')
        self._add_impl(card)

    @abc.abstractmethod
    def _add_impl(self, card: Card) -> None:
        raise NotImplementedError

    def contains_suit(self, suit: Suit) -> bool:
        """
        Checks if a card of a suit is still in the card container.

        :param suit: which should be checked
        :return: True if contains this suit else False
        """
        return any(card.suit == suit for card in self)

    def get_cards_of_suit(self, suit: Suit) -> Iterator[Card]:
        """
        Get all cards of a suit in the card container.

        :param suit: which should be checked
        :return: iterator of cards of given suit
        """
        return filter(lambda card: card.suit == suit, self)


class UnorderedCardContainer(CardContainer):
    """
    Base Class unordered card containers
    """

    _cards_set: set[Card] = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._cards_set = set(self.cards)
        self.__resync()

    def __contains__(self, card: Card) -> bool:
        return card in self._cards_set

    def _remove_impl(self, card: Card) -> None:
        self._cards_set.remove(card)
        self.__resync()

    def _add_impl(self, card: Card) -> None:
        self._cards_set.add(card)
        self.__resync()

    def __resync(self) -> None:
        """
        de-duplicate and re-sort self.cards - i.e. synchronize with the set representation
        """
        self.__config__.allow_mutation = True
        self.cards = tuple(sorted(self._cards_set))
        self.__config__.allow_mutation = False


class OrderedCardContainer(CardContainer):
    """
    Base Class ordered card containers
    """

    def _remove_impl(self, card: Card) -> None:
        card_list = list(self.cards)
        card_list.remove(card)

        self.__config__.allow_mutation = True
        self.cards = tuple(card_list)
        self.__config__.allow_mutation = False

    def _add_impl(self, card: Card) -> None:
        self.__config__.allow_mutation = True
        self.cards = (*self.cards, card)
        self.__config__.allow_mutation = False

    @property
    def first(self) -> Optional[Card]:
        """
        Returns the first card in the card container.
        :return: The first card played if it exists. Else None.
        """
        if len(self) == 0:
            return None
        return self.cards[0]

    @property
    def last(self) -> Optional[Card]:
        """
        Returns the last card in the card container.
        :return: The last card played if it exists. Else None.
        """
        if len(self) == 0:
            return None
        return self.cards[-1]

    def get_turn(self, card: Card) -> int:
        """
        Gets the turn of a card played.
        :param card: for which the turn number shall be found
        :return: the index of the card in the card container. 0 is the first the card played
        """
        return self.cards.index(card)

    def get_turn_and_winner_card(self, trump: Suit) -> Optional[tuple[int, Card]]:
        """
        Returns the highest trump card or the highest card of the suit played first.
        :param trump: suit of trump
        :return: the winning card and its index
        """
        if len(self) == 0:
            return None
        winner_suit_cards = list(self.get_cards_of_suit(trump))
        if len(winner_suit_cards) == 0:
            winner_suit_cards = self.get_cards_of_suit(self.first.suit)
        winner_card = max(winner_suit_cards, key=lambda x: x.rank)
        return self.get_turn(winner_card), winner_card
