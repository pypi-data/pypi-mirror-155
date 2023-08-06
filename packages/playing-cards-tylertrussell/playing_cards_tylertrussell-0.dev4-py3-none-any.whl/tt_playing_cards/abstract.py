"""Generic library for playing cards
"""

from abc import ABCMeta
from typing import Optional


class CardPropertyABC(metaclass=ABCMeta):
    """Abstract Base Class for all card *property* classes.

    Examples of properties include suit, color, number.
    """
    
    # name of this property e.g. suit
    # PropertyName = None

    # acceptable values for this property e.g. diamond/heart/club/spades
    AcceptableValues = None

    # whether this property must be populated on any given card
    Required = True

    def __init__(self, name):
        self.name = name

    def validate(self, value):
        if self.Required and value is None:
            raise ValueError('Property {} is required'.format(self.name))

        if self.AcceptableValues:
            failed_value_validation = False
            if callable(self.AcceptableValues):
                failed_value_validation = not self.AcceptableValues(value)
            else:
                failed_value_validation = value not in self.AcceptableValues
            if failed_value_validation:
                raise ValueError('"{}" is not an acceptable value for {}'.format(value, self.name))


class CardABC(metaclass=ABCMeta):
    """Abstract Base Class for all card classes."""

    # types of properties on this type of card
    # property_name:  property_value
    CardProperties = []

    @classmethod
    def required_props(cls):
        return [prop.key() for prop in self.CardProperties if prop.required]

    def __init__(self, **kwargs) -> None:

        self._data = {}
        self._properties = {
            prop.name: prop
            for prop in self.CardProperties
        }

        # validate properties passed-in to ctor
        for prop_name, prop in self._properties.items():
            prop_value = kwargs.get(prop_name)
            prop.validate(prop_value)
            self._data[prop_name] = prop_value

    def get(self, prop_name, error_if_missing=True) -> Optional[str]:
        if prop_name not in self._data:
            if error_if_missing:
                raise KeyError('Prop {} not in this card'.format(prop_name))
            else:
                return
        return self._data[prop_name]

