#!/usr/bin/env python3

'''
Represents the statistics of a Pokemon
'''


class Statistics:

    def __init__(self, hp: int, attack: int, defense: int, sattack: int,
                 sdefense: int, speed: int):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sattack = sattack
        self.sdefense = sdefense
        self.speed = speed

    @classmethod
    def fromArray(cls, arr):
        ''' Constructs statistics from an array.

        Indexes in the array will be interpreted in this order:
        HP, ATK, DEF, S.ATK, S.DEF, SPD

        '''

        return cls(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
