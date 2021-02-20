from enum import Enum


class Type(Enum):
    DEATH = 0
    MOVE = 1
    SPAWN_NPC = 2
    COMMAND = 3
    MOVE_PLAYER = 4
    VISITOR_EXIT = 5
    BALANCE_CHANGE = 6


class AffecteesType(Enum):
    NONE = 0
    PLAYER = 1
    ZOO = 2


class Event:
    def __init__(self, event: Type, asset=None, affects=(AffecteesType.NONE,), details={}):
        self.type = event
        self.asset = asset
        self.affectees = affects
        self.details = details

    def __str__(self):
        return f'EVENT: {self.type}\n\taffects: {self.affectees}\n\tasset: {self.asset}\n\tdetails: {self.details}\n'
