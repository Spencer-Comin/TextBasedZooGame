import Event
from NPC import NPCLookup, Animal, Visitor
from Utilities import neighbours, add_name, distance
import random


class Zoo:
    events = []
    openGateChar = ' '
    closedGateChar = '='
    visitorFlux = 0.004

    def __init__(self, filename, player_char):
        self.npcs = set()
        self.walls = set()
        self.gates = set()
        self.openGates = set()
        self.entrances = set()
        self.warehouseCorners = [(0, 0), (0, 0)]
        self.playerPos = ()
        self.playerChar = player_char
        self.map = self.build_from_file(filename)
        self.analyze_map()

    @property
    def npc_positions(self):
        return {npc.pos: npc for npc in self.npcs}

    @staticmethod
    def build_from_file(filename):
        matrix = []
        with open(filename, 'r') as file:
            for line in file:
                matrix.append([c for c in line.rstrip()])
        return matrix

    def analyze_map(self):
        warehouse_corners = []
        for i, row in enumerate(self.map):
            for j, tile in enumerate(row):
                if tile in '|+#-':
                    self.walls.add((i, j))
                elif tile == '=':
                    self.gates.add((i, j))
                elif tile == '*':
                    self.walls.add((i, j))
                    warehouse_corners.append((i, j))
                elif tile == '%':
                    self.entrances.add((i, j))
                elif tile == self.playerChar:
                    self.playerPos = (i, j)
                elif tile.upper() in NPCLookup.keys():
                    npc = NPCLookup[tile.upper()]((i, j))
                    npc.baby = tile.islower()
                    if not npc.baby and isinstance(npc, Animal):
                        npc.age = npc.timeToGrowUp
                    self.npcs.add(npc)
        x1, y1 = warehouse_corners[0]
        x2, y2 = warehouse_corners[1]
        self.warehouseCorners = ((min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)))

    def in_warehouse(self, pos=None):
        x, y = pos if pos is not None else self.playerPos
        x1, y1 = self.warehouseCorners[0]
        x2, y2 = self.warehouseCorners[1]
        return x1 < x < x2 and y1 < y < y2

    def update(self):
        new_events = []
        while self.events:
            event = self.events.pop()
            new_events.extend(self.handle_event(event))
        for animal in self.npcs:
            self.events.extend(animal.update())
        self.attempt_visitor_enter()
        return [event for event in self.events if Event.AffecteesType.PLAYER in event.affectees] + new_events

    def attempt_visitor_enter(self):
        for entrance in self.entrances:
            if random.random() < self.visitorFlux:
                new_visitor = Visitor(entrance)
                self.events.append(Event.Event(
                    Event.Type.VISITOR_ENTER,
                    affects=(Event.AffecteesType.PLAYER, Event.AffecteesType.ZOO),
                    asset=new_visitor,
                    details={'notification': f'{new_visitor.name} has entered the zoo'}
                ))

    def attempt_visitor_exit(self, visitor):
        if random.random() < self.visitorFlux:
            return Event.Event(
                Event.Type.VISITOR_EXIT,
                affects=(Event.AffecteesType.PLAYER, Event.AffecteesType.ZOO),
                asset=visitor,
                details={'notification': f'{visitor.name} has left the zoo'}
            )

    def handle_event(self, event: Event.Event):
        responses = []
        if event.type is Event.Type.DEATH:
            # remove dead npc
            dead_npc = event.asset
            try:
                self.npcs.remove(dead_npc)
            except KeyError:
                # idk what's going on here
                print('mystery zone')
                assert dead_npc not in self.npcs
            x, y = dead_npc.pos
            self.map[x][y] = ' '
            # recycle name
            add_name(dead_npc.name, animal=isinstance(dead_npc, Animal))
        elif event.type is Event.Type.MOVE:
            npc = event.asset
            try:
                new_position = event.details['position']
                if new_position not in (self.walls | self.gates) - self.openGates:
                    x, y = npc.pos
                    self.map[x][y] = ' '
                    npc.pos = new_position
                    x, y = new_position
                    self.map[x][y] = npc.character
                    for position in neighbours(new_position) & set(self.npc_positions.keys()):
                        other = self.npc_positions[position]
                        new_event = npc.interact(other)
                        if new_event is not None:
                            responses.append(new_event)
                    if isinstance(npc, Visitor) and min([distance(npc.pos, entrance) for entrance in self.entrances]) < 4:
                        new_event = self.attempt_visitor_exit(npc)
                        if new_event is not None:
                            responses.append(new_event)
            except KeyError:
                print('Error getting position from details in MOVE event')
        elif event.type is Event.Type.MOVE_PLAYER:
            try:
                change = event.details['move']
                new_position = (self.playerPos[0] + change[0], self.playerPos[1] + change[1])
                if new_position not in (self.walls | self.gates) - self.openGates:
                    x, y = self.playerPos
                    self.map[x][y] = ' '
                    self.playerPos = new_position
                    x, y = new_position
                    self.map[x][y] = self.playerChar
            except KeyError:
                print('Error getting position from details in MOVE_PLAYER event')
                # change affectees list and pass on event
            event.affectees = (Event.AffecteesType.PLAYER,)
            responses.append(event)
        elif event.type is Event.Type.BIRTH:
            baby = event.asset
            x, y = baby.pos
            self.map[x][y] = baby.character
            self.npcs.add(baby)
        elif event.type is Event.Type.VISITOR_EXIT:
            visitor = event.asset
            self.npcs.remove(visitor)
            x, y = visitor.pos
            self.map[x][y] = ' '
            add_name(visitor.name)
        elif event.type is Event.Type.VISITOR_ENTER:
            visitor = event.asset
            x, y = visitor.pos
            self.map[x][y] = visitor.character
            self.npcs.add(visitor)
        return responses


