import Event
import random
from Constants import FPS, names, animalNames


class NPC:
    speed = 1.5 / FPS
    babyPrint = ' '
    adultPrint = ' '
    baby = bool(random.getrandbits(1))

    def __init__(self, pos, name=random.choice(names)):
        self.pos = pos
        self.name = name

    def attempt_move(self):
        if random.random() < self.speed:
            x, y = self.pos
            new_pos = random.choice([(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)])

            return Event.Event(Event.Type.MOVE, self,
                               affects=(Event.AffecteesType.ZOO,),
                               details={'position': new_pos})

    def update(self):
        move = self.attempt_move()
        if move is not None:
            return [move]
        return []

    @property
    def character(self):
        if self.baby:
            return self.babyPrint
        else:
            return self.adultPrint


class Visitor(NPC):
    babyPrint = 'v'
    adultPrint = 'V'


class Animal(NPC):
    species = 'animal'
    speed = 2 / FPS
    name = ''
    timeToGrowUp = 100 * FPS
    hunger = 0
    maxHunger = 100 * FPS
    maxAge = 500 * FPS
    baby = True

    def __init__(self, position, name=random.choice(animalNames)):
        super(Animal, self).__init__(position, name)
        self.age = 0

    def update(self):
        events = super(Animal, self).update()
        self.age += 1
        self.hunger += 2
        if self.age > self.timeToGrowUp:
            self.baby = False
        if self.hunger > self.maxHunger:
            events = [(Event.Event(Event.Type.DEATH, self,
                                   affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                   details={'notification': f'{self.name} the {self.species} has died of hunger'}))]
        elif self.age > self.maxAge:
            events = [(Event.Event(Event.Type.DEATH, self,
                                   affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                   details={'notification': f'{self.name} the {self.species} has died of old age'}))]
        return events

    def feed(self):
        self.hunger = 0


class Lion(Animal):
    species = 'lion'
    babyPrint = 'l'
    adultPrint = 'L'


class Tiger(Animal):
    species = 'tiger'
    babyPrint = 't'
    adultPrint = 'T'


class Zebra(Animal):
    species = 'zebra'
    babyPrint = 'z'
    adultPrint = 'Z'


class Ostrich(Animal):
    species = 'ostrich'
    babyPrint = 'o'
    adultPrint = 'O'


class Moose(Animal):
    species = 'moose'
    babyPrint = 'm'
    adultPrint = 'M'


NPCLookup = {
    'V': Visitor,
    'L': Lion,
    'T': Tiger,
    'Z': Zebra,
    'O': Ostrich,
    'M': Moose
}
