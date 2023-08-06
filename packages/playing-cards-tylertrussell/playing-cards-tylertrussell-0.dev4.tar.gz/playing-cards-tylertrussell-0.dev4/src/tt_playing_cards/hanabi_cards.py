from .abstract import (
    CardABC,
    CardPropertyABC,
)


class HanabiColorProperty(CardPropertyABC):
    WHITE = 'white'
    YELLOW = 'yellow'
    GREEN = 'green'
    BLUE = 'blue'
    RED = 'red'

    AcceptableValues = {WHITE, YELLOW, GREEN, BLUE, RED}


class HanabiNumberProperty(CardPropertyABC):
    AcceptableValues = set(range(1, 6))


class HanabiCard(CardABC):
    CardProperties = [
        HanabiColorProperty('color'),
        HanabiNumberProperty('number'),
    ]

    def __init__(self, color, number):
        super().__init__(color=color, number=number)
