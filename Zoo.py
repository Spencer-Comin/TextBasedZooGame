import Event
from NPC import NPCLookup, Animal


class Zoo:
    events = []
    openGateChar = ' '
    closedGateChar = '='

    def __init__(self, filename, player_char):
        self.npcs = set()
        self.walls = set()
        self.gates = set()
        self.openGates = set()
        self.warehouseCorners = [(0, 0), (0, 0)]
        self.playerPos = ()
        self.playerChar = player_char
        self.map = self.build_from_file(filename)
        self.analyze_map()

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
        return [event for event in self.events if Event.AffecteesType.PLAYER in event.affectees] + new_events

    def handle_event(self, event):
        if event.type is Event.Type.DEATH:
            # remove dead animal
            dead_animal = event.asset
            try:
                self.npcs.remove(dead_animal)
            except KeyError:
                # idk what's going on here
                assert dead_animal not in self.npcs
            x, y = dead_animal.pos
            self.map[x][y] = ' '
            # change affectees list and pass on event
            event.affectees = (Event.AffecteesType.PLAYER,)
            return [event]
        if event.type is Event.Type.MOVE:
            animal = event.asset
            try:
                new_position = event.details['position']
                if new_position not in (self.walls | self.gates) - self.openGates:
                    x, y = animal.pos
                    self.map[x][y] = ' '
                    animal.pos = new_position
                    x, y = new_position
                    self.map[x][y] = animal.character
            except KeyError:
                print('Error getting position from details in MOVE event')
            return []
        if event.type is Event.Type.MOVE_PLAYER:
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
            return [event]

