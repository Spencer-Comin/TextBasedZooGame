from NPC import Animal


class CommandHandler:
    notificationsDump = []

    def __init__(self, zoo, player):
        self.zoo = zoo
        self.player = player
        self.lookup = {
            'open': self.open,
            'close': self.close,
            'error': lambda x: self.notify(f'{x} is not a valid command'),
            'feed': self.feed,
            'get': self.get
        }

    def notify(self, message):
        self.notificationsDump.append(message)

    def parse(self, command_string):
        tokens = command_string.split(' ')
        if tokens[0] in self.lookup.keys():
            return tokens[0], tokens[1:]
        else:
            return 'error', [tokens[0]]

    @staticmethod
    def neighbours(pos):
        x, y = pos
        return {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}

    def feed(self):
        # find animals
        nearby_animals = [animal for animal in self.zoo.npcs if
                          isinstance(animal, Animal) and animal.pos in self.neighbours(self.zoo.playerPos)]
        # feed animals
        for animal in nearby_animals:
            if self.player.food > 0:
                animal.feed()
                self.notify(f'feeding {animal.name} the {animal.species}')
                self.player.food -= 1
            else:
                self.notify('out of food')
                break
        if not nearby_animals:
            self.notify('no animals nearby to feed')

    def get(self, obj):
        if self.zoo.in_warehouse():
            if obj == 'food':
                self.player.food += 10
                self.notify('getting 10 food')
            else:
                self.notify(f'cannot get {obj}')
        else:
            self.notify('cannot get anything because you are not in the warehouse')

    def open(self, obj):
        if obj == 'gate':
            self.open_gate()
        else:
            self.notify(f'{obj} cannot be opened')

    def open_gate(self):
        zoo = self.zoo
        available_gate = self.neighbours(zoo.playerPos) & zoo.gates
        if available_gate:
            gate = available_gate.pop()
            if gate in zoo.openGates:
                self.notify('gate is already open')
            else:
                i, j = gate
                zoo.openGates.add((i, j))
                zoo.map[i][j] = zoo.openGateChar
                self.notify('gate opened')
        else:
            self.notify('no gates nearby')

    def close(self, obj):
        if obj == 'gate':
            self.close_gate()
        else:
            self.notify(f'{obj} cannot be opened')

    def close_gate(self):
        zoo = self.zoo
        available_gate = (self.neighbours(zoo.playerPos) | {zoo.playerPos}) & zoo.gates
        if available_gate:
            gate = available_gate.pop()
            if gate not in zoo.openGates:
                self.notify('gate is already closed')
            elif gate == zoo.playerPos:
                self.notify('you are in the way')
            else:
                i, j = gate
                zoo.openGates.remove((i, j))
                zoo.map[i][j] = zoo.closedGateChar
                self.notify('gate closed')
        else:
            self.notify('no gates nearby')

    def interpret(self, command, *args):
        self.lookup.get(command, lambda *x: None)(*args)

    def execute(self, command_string):
        command, args = self.parse(command_string)
        self.interpret(command, *args)
