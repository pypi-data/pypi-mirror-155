from .abstract import (
    CardABC,
    CardPropertyABC,
)


_VALID_NUMBERS = set(range(2, 11))
_VALID_HIGH_CARDS = {'J', 'Q', 'K', 'A'}
VALID_FACE_VALUES = _VALID_NUMBERS | _VALID_HIGH_CARDS


class PlayingCardNumberProperty(CardPropertyABC):
    AcceptableValues = VALID_FACE_VALUES


class PlayingCardSuitProperty(CardPropertyABC):
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'
    HEARTS = 'hearts'
    SPADES = 'spades'

    AcceptableValues = {CLUBS, DIAMONDS, HEARTS, SPADES}


class PlayingCard(CardABC):
    CardProperties = [
        PlayingCardNumberProperty('number'),
        PlayingCardSuitProperty('suit'),
    ]
