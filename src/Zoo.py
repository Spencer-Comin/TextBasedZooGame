import Event
from NPC import NPCLookup, Animal, Visitor
from Utilities import neighbours, add_name, distance
import random


class Zoo:
    openGateChar = ' '
    closedGateChar = '='
    visitorFlux = 0.004
    maxNPCs = 80

    def __init__(self, filename, player_char, emit):
        self.npcs = set()
        self.emit = emit
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

    @property
    def animals(self):
        return {npc for npc in self.npcs if isinstance(npc, Animal)}

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
                    npc = NPCLookup[tile.upper()]((i, j), self.emit)
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
        for animal in self.npcs:
            animal.update()
        self.attempt_visitor_enter()

    def attempt_visitor_enter(self):
        for entrance in self.entrances:
            if random.random() < self.visitorFlux and len(self.npcs) < self.maxNPCs:
                new_visitor = Visitor(entrance, self.emit)
                entrance_fee = len(self.animals)
                self.emit(Event.Event(
                    Event.Type.SPAWN_NPC,
                    affects=(Event.AffecteesType.PLAYER, Event.AffecteesType.ZOO),
                    asset=new_visitor,
                    details={'notification': f'{new_visitor.name} has entered the zoo'}
                ))
                self.emit(Event.Event(
                    Event.Type.ADD_TO_INVENTORY,
                    affects=(Event.AffecteesType.PLAYER,),
                    asset='money',
                    details={'notification': f'{new_visitor.name} paid ${entrance_fee}',
                             'amount': entrance_fee}
                ))

    def attempt_visitor_exit(self, visitor):
        if random.random() < self.visitorFlux:
            self.emit(Event.Event(
                Event.Type.VISITOR_EXIT,
                affects=(Event.AffecteesType.PLAYER, Event.AffecteesType.ZOO),
                asset=visitor,
                details={'notification': f'{visitor.name} has left the zoo'}
            ))

    def handle_event(self, event: Event.Event):
        if event.type is Event.Type.DEATH:
            # remove dead npc
            dead_npc = event.asset
            try:
                self.npcs.remove(dead_npc)
            except KeyError:
                # idk what's going on here
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
                    if isinstance(npc, Visitor) and min([distance(npc.pos, entrance) for entrance in self.entrances if
                                                         entrance is not npc.start]) < 5:
                        self.attempt_visitor_exit(npc)
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
        elif event.type is Event.Type.SPAWN_NPC:
            npc = event.asset
            x, y = npc.pos
            self.map[x][y] = npc.character
            self.npcs.add(npc)
        elif event.type is Event.Type.VISITOR_EXIT:
            visitor = event.asset
            try:
                self.npcs.remove(visitor)
            except KeyError:
                # weird stuff
                pass
            x, y = visitor.pos
            self.map[x][y] = ' '
            add_name(visitor.name)
