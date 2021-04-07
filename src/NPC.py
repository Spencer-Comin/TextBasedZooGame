import Event
import random
from Utilities import FPS, get_name


class NPC:
    speed = 1.5 / FPS
    babyPrint = ' '
    adultPrint = ' '
    baby = bool(random.getrandbits(1))
    is_open = None
    emit = None
    path = []
    walls = set()

    def __init__(self, pos, emit, name=''):
        if not name:
            name = get_name()
        self.pos = pos
        self.name = name
        self.emit = emit

    def attempt_move(self):
        if random.random() < self.speed:
            if not self.path:
                x, y = self.pos
                new_pos = random.choice([(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)])
            else:
                new_pos = self.path.pop(0)

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
    gate = None

    def __init__(self, position, emit, name=''):
        if not name:
            name = get_name(animal=True)
        super().__init__(position, emit, name)
        self.age = random.randint(0, 60) * FPS
        self.maxHunger += random.randint(0, 120) * FPS
        self.maxAge += random.randint(0, 180) * FPS

    @property
    def title(self):
        return f'{self.name} the {self.species}'

    def update(self):
        self.age += 1
        self.hunger += 1
        if self.age == self.timeToGrowUp:
            self.baby = False
            self.emit(Event.Event(details={'notification': f'{self.title} has grown up'}))
        if self.hunger == (self.maxHunger * 10) // 9:
            self.emit(Event.Event(details={'notification': f'{self.title} is starving'}))
        if self.hunger == self.maxHunger:
            self.die(f'{self.title} has died of hunger')
        elif self.age == self.maxAge:
            self.die(f'{self.title} has died of old age')
        else:
            super().update()

    def feed(self):
        self.hunger = 0

    def interact(self, other):
        if type(self) is type(other) and not (self.baby or other.baby) and random.random() < self.babyProbability:
            name = get_name(animal=True)
            self.emit(Event.Event(Event.Type.SPAWN_NPC, type(self)(self.pos, self.emit, name),
                                  affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                  details={
                                      'notification': f'{self.title} and {other.title} have given birth to {name}'}))

    @staticmethod
    def three_way_compare(a, b):
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return 0

    def attempt_move(self):
        if self.pos == self.gate:
            self.gate = None
        if self.path and not self.is_open(self.gate):
            self.path = []
        elif not self.path and self.is_open(self.gate):
            # this pathfinding is boring, maybe implement djikstra or A* later
            x, y = self.pos
            end_x, end_y = self.gate
            dx = -self.three_way_compare(x, end_x)
            dy = -self.three_way_compare(y, end_y)
            while x != end_x or y != end_y:
                if x == end_x:
                    dx = 0
                if y == end_y:
                    dy = 0
                x += dx
                y += dy
                self.path.append((x, y))

        super().attempt_move()


class Predator(Animal):
    attackProbability = 0.8

    def interact(self, other):
        if not isinstance(other, Predator):
            if random.random() < self.attackProbability:
                if isinstance(other, Animal):
                    other.die(f'{self.title} attacked and killed {other.title}')
                elif isinstance(other, Visitor):
                    other.die(f'{self.title} attacked and killed {other.name}')
                self.hunger = 0
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
