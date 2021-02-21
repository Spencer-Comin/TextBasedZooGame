from NPC import Animal, Visitor
from Utilities import neighbours, get_feeling, get_fact

import sys


class CommandHandler:
    notificationsDump = []

    def __init__(self, zoo, player, warehouse):
        self.zoo = zoo
        self.player = player
        self.lookup = {
            'open': self.open,
            'close': self.close,
            'error': lambda x: self.notify(f'{x} is not a valid command'),
            'feed': self.feed,
            'get': self.get,
            'check': self.check,
            'help': self.help,
            'info': self.info
        }
        self.warehouse = warehouse

    def notify(self, message):
        self.notificationsDump.append(message)

    def parse(self, command_string):
        tokens = command_string.split(' ')
        if tokens[0] in self.lookup.keys():
            return tokens[0], tokens[1:]
        else:
            return 'error', [tokens[0]]

    def help(self):
        for key in self.lookup:
            self.notify(key)

    def info(self, obj=''):
        # find animals
        if not obj:
            nearby_npcs = [npc for npc in self.zoo.npcs if npc.pos in neighbours(self.zoo.playerPos, dist=2)]
            for npc in nearby_npcs:
                if isinstance(npc, Animal):
                    self.notify(f'{npc.title}, age: {npc.age}, hunger: {npc.hunger}, max hunger: {npc.maxHunger}')
                elif isinstance(npc, Visitor):
                    self.notify(f'{npc.name} is feeling {get_feeling()}')
            if not nearby_npcs:
                self.notify(f'nothing nearby to get info on, enjoy this animal fact:\n\t{get_fact()}')
        else:
            self.notify(f'getting info on {obj} is not yet implemented')

    def check(self, *objs):
        if 'inventory' in objs or not objs:
            for item, count in self.player.inventory.items():
                self.notify(f'{count} {item}')
        elif 'warehouse' in objs:
            pass
        else:
            for obj in objs:
                self.check_item(obj)

    def check_item(self, obj):
        self.notify(f'{self.player.inventory.get(obj, 0)} {obj}')

    def feed(self):
        # find animals
        nearby_animals = [animal for animal in self.zoo.npcs if
                          isinstance(animal, Animal) and animal.pos in neighbours(self.zoo.playerPos, dist=4)]
        # feed animals
        for animal in nearby_animals:
            if self.player.inventory['food'] > 0:
                animal.feed()
                self.notify(f'feeding {animal.name} the {animal.species}')
                self.player.inventory['food'] -= 1
            else:
                self.notify('out of food')
                break
        if not nearby_animals:
            self.notify('no animals nearby to feed')

    def get(self, amount, obj=''):
        try:
            amount = int(amount)
        except ValueError:
            # only one input given, switch around parameters
            obj = amount
            amount = 1
        if self.zoo.in_warehouse():
            if obj == 'food':
                self.player.inventory['food'] += amount
                self.notify(f'getting {amount} food')
            elif obj == 'info':
                self.info()
            elif obj == 'help':
                self.help()
            else:
                self.notify(f'cannot get {obj}')
        else:
            self.notify('cannot get anything because you are not in the warehouse')

    def open(self, obj=''):
        if obj == 'gate':
            self.open_gate()
        elif obj:
            self.notify(f'{obj} cannot be opened')
        else:
            self.notify("try 'open gate'")

    def open_gate(self):
        zoo = self.zoo
        available_gate = neighbours(zoo.playerPos) & zoo.gates
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

    def close(self, obj=''):
        if obj == 'gate':
            self.close_gate()
        elif obj:
            self.notify(f'{obj} cannot be closed')
        else:
            self.notify("try 'close gate'")

    def close_gate(self):
        zoo = self.zoo
        available_gate = (neighbours(zoo.playerPos) | {zoo.playerPos}) & zoo.gates
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
        try:
            self.lookup.get(command, lambda *x: None)(*args)
        except TypeError:
            _, exc, _ = sys.exc_info()
            error_string = exc.args[0]
            self.notify(f'bad argument: {error_string}')

    def execute(self, command_string):
        command, args = self.parse(command_string)
        self.interpret(command, *args)
