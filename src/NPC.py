import Event
import random
from Utilities import FPS, get_name


class NPC:
    speed = 1.5 / FPS
    babyPrint = ' '
    adultPrint = ' '
    baby = bool(random.getrandbits(1))

    def __init__(self, pos, emit, name=''):
        if not name:
            name = get_name()
        self.pos = pos
        self.name = name
        self.emit = emit

    def attempt_move(self):
        if random.random() < self.speed:
            x, y = self.pos
            new_pos = random.choice([(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)])

            self.emit(Event.Event(Event.Type.MOVE, self,
                                  affects=(Event.AffecteesType.ZOO,),
                                  details={'position': new_pos}))

    def update(self):
        self.attempt_move()

    @property
    def character(self):
        if self.baby:
            return self.babyPrint
        else:
            return self.adultPrint

    def interact(self, other):
        assert isinstance(other, NPC)

    def die(self, notification):
        print(f'death notification emitted for {self}')
        self.emit(Event.Event(Event.Type.DEATH, self,
                              affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                              details={'notification': notification}))


class Visitor(NPC):
    babyPrint = 'v'
    adultPrint = 'V'

    def __init__(self, pos, emit):
        super().__init__(pos, emit)
        self.start = pos
        self.baby = bool(random.getrandbits(1))


class Animal(NPC):
    species = 'animal'
    speed = 2 / FPS
    name = ''
    timeToGrowUp = 150 * FPS
    hunger = 0
    maxHunger = 300 * FPS
    maxAge = 700 * FPS
    baby = True
    babyProbability = 0.002

    def __init__(self, position, emit, name=''):
        if not name:
            name = get_name(animal=True)
        super().__init__(position, emit, name)
        self.age = 0

    @property
    def title(self):
        return f'{self.name} the {self.species}'

    def update(self):
        super().update()
        self.age += 1
        self.hunger += 1
        if self.age == self.timeToGrowUp:
            self.baby = False
        if self.hunger == self.maxHunger:
            self.die(f'{self.title} has died of hunger')
        elif self.age == self.maxAge:
            self.die(f'{self.title} has died of old age')

    def feed(self):
        self.hunger = 0

    def interact(self, other):
        if type(self) is type(other) and not (self.baby or other.baby) and random.random() < self.babyProbability:
            name = get_name(animal=True)
            self.emit(Event.Event(Event.Type.SPAWN_NPC, type(self)(self.pos, name),
                                  affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                  details={
                                      'notification': f'{self.title} and {other.title} have given birth to {name}'}))


class Predator(Animal):
    attackProbability = 0.8

    def interact(self, other):
        if not isinstance(other, Predator):
            if random.random() < self.attackProbability:
                if isinstance(other, Animal):
                    other.die(f'{self.title} attacked and killed {other.title}')
                elif isinstance(other, Visitor):
                    other.die(f'{self.title} attacked and killed {other.name}')
        else:
            super().interact(other)


class Lion(Predator):
    species = 'lion'
    babyPrint = 'l'
    adultPrint = 'L'


class Tiger(Predator):
    species = 'tiger'
    babyPrint = 't'
    adultPrint = 'T'


class Jaguar(Predator):
    species = 'jaguar'
    babyPrint = 'j'
    adultPrint = 'J'


class Zebra(Animal):
    species = 'zebra'
    babyPrint = 'z'
    adultPrint = 'Z'


class Camel(Animal):
    species = 'camel'
    babyPrint = 'c'
    adultPrint = 'C'


class Giraffe(Animal):
    species = 'giraffe'
    babyPrint = 'g'
    adultPrint = 'G'


class Moose(Animal):
    species = 'moose'
    babyPrint = 'm'
    adultPrint = 'M'


class Buffalo(Animal):
    species = 'buffalo'
    babyPrint = 'b'
    adultPrint = 'B'


class Penguin(Animal):
    species = 'penguin'
    babyPrint = 'p'
    adultPrint = 'P'


class Yak(Animal):
    species = 'yak'
    babyPrint = 'y'
    adultPrint = 'Y'


NPCLookup = {
    'V': Visitor,
    'L': Lion,
    'T': Tiger,
    'Z': Zebra,
    'C': Camel,
    'M': Moose,
    'G': Giraffe,
    'B': Buffalo,
    'P': Penguin,
    'Y': Yak,
    'J': Jaguar
}
