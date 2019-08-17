
'''
A Pokemon move.
'''

from enum import Enum
from structs.type import Type


class MoveCategory(Enum):
    PHYSICAL = 0
    SPECIAL = 1
    STATUS = 2


class Move:
    """ A struct representing a Pokemon move. """
    def __init__(self, name: str, movetype: Type, category: MoveCategory,
                 power: int, accuracy: int):
        if type(movetype) is str:
            movetype = Type[movetype]

        if type(category) is str:
            category = MoveCategory[category]

        self._name = name
        self._type = movetype
        self._category = category
        self._power = power
        self._accuracy = accuracy

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> Type:
        return self._type

    @property
    def category(self) -> MoveCategory:
        return self._category

    @property
    def power(self) -> int:
        return self._power

    @property
    def accuracy(self) -> int:
        return self._accuracy

    def print(self):
        print((f'Move Data\n'
               f'---------\n'
               f'Name: {self.name}\n'
               f'Type: {self.type.name}\n'
               f'Category: {self.category.name}\n'
               f'\n'
               f'Power: {self.power if self.power != -1 else "N/A"}\n'
               f'Accuracy: {self.accuracy if self.accuracy != -1 else "N/A"}\n'
               ))
