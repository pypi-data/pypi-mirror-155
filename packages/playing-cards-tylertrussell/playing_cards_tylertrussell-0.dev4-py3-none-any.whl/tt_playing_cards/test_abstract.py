
import pytest

from .abstract import (
    CardABC,
    CardPropertyABC,
)


def test_empty_cards():
    
    class SimpleCard(CardABC):
        pass

    SimpleCard()


def test_card_definition_with_one_property():

    class TestProperty(CardPropertyABC):
        AcceptableValues = {1, 2, 3, 4}

    class TestCard(CardABC):
        CardProperties = [TestProperty('value')]

    with pytest.raises(ValueError):
        TestCard(test_value='break')

    with pytest.raises(ValueError):
        TestCard(value=5)

    TestCard(value=1)


@staticmethod  # must be a static method to prevent becoming bound
def is_string(s):
    return isinstance(s, str)


def test_card_definition_with_many_properties():

    class NameProperty(CardPropertyABC):
        AcceptableValues = is_string

    class NumberProperty(CardPropertyABC):
        AcceptableValues = range(1, 101)

    class PokemonCard(CardABC):
        CardProperties = [
            NameProperty('name'),
            NumberProperty('hp'),
            NumberProperty('power'),
        ]

    PokemonCard(
        name='charizard',
        hp=100,
        power=35,
    )

    # mismatched argument
    with pytest.raises(ValueError):
        PokemonCard(
            name=4,
            hp=100,
            power=35,
        )

    # missing values
    with pytest.raises(ValueError):
        PokemonCard(name='Pikachu')


