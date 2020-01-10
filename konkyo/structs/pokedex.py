#!/usr/bin/env python3

'''
'''

from structs.stats import Statistics


class PokedexEntry:
    """ A data representation of a Pokemon.

    Args:
        id (int): The ID of the Pokemon.
        name (str): The name of the Pokemon.
        type (:obj:`list` of :obj:`str`): The Pokemons' type(s).
        height (float): The height of this Pokemon, in meters.
        weight (float): The weight of this Pokemon, in kilograms.
        desc (str): The Pokedex description of this Pokemon.
        base_stats (Stats): The base statistics of this Pokemon.
    """

    def __init__(self, id: int, name: str, type: list, height: float,
                 weight: float, desc: str, base_stats: Statistics):
        self.id = id
        self.name = name
        self.type = type
        self.height = height
        self.weight = weight
        self.desc = desc
        self.base_stats = base_stats

    def getHP(self) -> int:
        return self.base_stats.hp

    def getATK(self) -> int:
        return self.base_stats.attack

    def getDEF(self) -> int:
        return self.base_stats.defense

    def getSATK(self) -> int:
        return self.base_stats.sattack

    def getSDEF(self) -> int:
        return self.base_stats.sdefense

    def getSPD(self) -> int:
        return self.base_stats.speed

    def getDescription(self) -> str:
        """ Describes all properties of this Pokemon. """
        return ('Pokedex Data\n'
                '------------\n'
                'ID: {id}\n'
                'Name: {name}\n'
                'Types: {types}\n'
                'Height: {height} m\n'
                'Weight: {weight} kg\n'
                '\n'
                'Description\n'
                '-----------\n'
                '{desc}\n'
                '\n'
                'Base Statistics\n'
                '---------------\n'
                'HP: {hp}\n'
                'ATK: {atk}\n'
                'DEF: {defn}\n'
                'S. ATK: {satk}\n'
                'S. DEF: {sdef}\n'
                'SPD: {spd}\n'
                ).format(id=self.id, name=self.name, types=self.type,
                         height=self.height, weight=self.weight,
                         desc=self.desc, hp=self.base_stats.hp,
                         atk=self.base_stats.attack,
                         defn=self.base_stats.defense,
                         satk=self.base_stats.sattack,
                         sdef=self.base_stats.sdefense,
                         spd=self.base_stats.speed)
