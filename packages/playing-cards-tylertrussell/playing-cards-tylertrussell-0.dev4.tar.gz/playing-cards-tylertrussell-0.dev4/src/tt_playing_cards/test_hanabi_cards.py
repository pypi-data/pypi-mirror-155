import pytest

from .hanabi_cards import HanabiCard, HanabiColorProperty


def test_making_hanabi_cards():
    with pytest.raises(TypeError):
        HanabiCard()

    with pytest.raises(ValueError):
        HanabiCard('purple', 1)

    with pytest.raises(ValueError):
        HanabiCard(HanabiColorProperty.YELLOW, 6)

    HanabiCard(HanabiColorProperty.WHITE, 5)
    HanabiCard(HanabiColorProperty.BLUE, 1)

