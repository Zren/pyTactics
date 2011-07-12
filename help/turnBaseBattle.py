import random

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

class Faction(object):
    def __init__(self, name):
        self.name = name
        self.units = []
    def join(self, unit):
        self.units.append(unit)
        unit.faction = self
    def __repr__(self):
        return "<Faction('%s', '%d')>" % (self.name, len(self.units))

class Unit(object):
    class State:
        Wait, Ready, Prep, Moving, Cooldown = range(5)

    def __init__(self, name, speed):
        self.x, self.y = (0, 0)
        self.name = name
        self.faction = None
        assert speed >= 0
        self.speed = speed
        self.lastMoveFrame = 0
        self.state = Unit.State.Wait
        self.currentMove = None
        self.currentTarget = None
    def nextMoveFrame(self):
        if self.state == Unit.State.Wait:
            return self.lastMoveFrame + self.speed
        elif self.currentMove != None:
            if self.state == Unit.State.Prep:
                return self.lastMoveFrame + self.currentMove.prep
            elif self.state == Unit.State.Cooldown:
                return self.lastMoveFrame + self.currentMove.cooldown
        return self.lastMoveFrame
    def nextMove(self):
        if random.randint(0,1):
            return Move(0, 1)
        else:
            return Attack(1, 2)
    def nextState(self):
        self.state += 1
        self.state %= 5
    def __repr__(self):
        return "<Unit('%s', '%s', '%d', s='%d', n='%d')>" % (self.name, self.faction, self.speed, self.state, self.nextMoveFrame())

class Action(object):
    def __init__(self, prep=0, cooldown=0):
        self.name = ""
        self.prep = prep
        self.cooldown = cooldown

class Move(Action):
    def __init__(self, prep=0, cooldown=0):
        Action.__init__(self, prep, cooldown)
        self.name = "Move"

class Attack(Action):
    def __init__(self, prep=0, cooldown=0):
        Action.__init__(self, prep, cooldown)
        self.name = "Attack"

class Timeline(list):
    def __init__(self):
        list.__init__(self)
        self.now = 0
    def next(self):
        for unit in units:
            if self.now >= unit.nextMoveFrame():
                return unit
        return None
    def tick(self):
        self.now += 1

class Cell(object):
    def __init__(self, terrain, wall, height):
        self.terrain = terrain
        self.wall = wall
        self.height = height

class Grid(object):
    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.cells = [[Cell(0, False, random.randint(0,2)) for y in self.height] for x in self.width]
class Map(Grid):
    def __init__(self, dimensions):
        Grid.__init__(self, dimensions)
class IsoMap(Map):
    def __init__(self, dimensions):
        Map.__init__(self, dimensions)
class Scene(IsoMap):
    def __init__(self, dimensions):
        self.timeline = Timeline()
    def play(self):
        while True:
            while True:
                unit = self.timeline.next()
                if unit == None:
                    break
                #print "%d: %s" % (self.timeline.now, unit)
                if unit.state == Unit.State.Ready:
                    unit.currentMove = unit.nextMove()
                elif unit.state == Unit.State.Moving:
                    self.doMove(unit)
                unit.lastMoveFrame = self.timeline.now
                unit.nextState()
            self.timeline.tick()
            if self.timeline.now > 100:
                break
    def placement(self):
        pass
    def doMove(self, user):
        if user.currentMove != None:
            print "%d) %s -> %s" % (self.timeline.now, user.name, user.currentMove.name)
        user.currentMove = None
        user.currentTarget = None

factions = list(Faction(n) for n in ["Red", "Blue"])
names = []
f = open("names.txt", "r")
n = 0
for line in f:
    n += 1
    if n > 10:
        break
    names.append(line.rstrip())
f.close()



units = list(Unit(n, random.randint(8, 12)) for n in names)
scene = Scene((10,10))
for unit in units:
    scene.timeline.append(unit)
    print unit

scene.placement()

scene.play()