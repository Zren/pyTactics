#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Admin
#
# Created:     12/07/2011
# Copyright:   (c) Admin 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
import Config, Resource
from PyGameEngine import PyGameEngine
from Hud import *
import random
import time

def overlayLevel(low, high):
    def level(f):
        if f <= 0.5:
            return f*2
        else:
            return (1.0-f)*2
    t = time.time()
    return low + (high-low) * level(t - int(t))

def isoGridRenderOrder(width, height):
    order = []
    col, row = 0, 0
    index = 0
    while True:
        order.append((col,row))
        if col >= width-1 and row >= height-1:
            break
        col -= 1
        row += 1
        if col < 0 or row >= height:
            index += 1
            col = index
            row = 0
            if index >= width:
                overflow = index - width + 1
                row +=  overflow
                col = width - 1
    return order
def isoCoordinates(col, row):
    x = col * (Config.tileWidth/2) - row * (Config.tileWidth/2)
    y = col * (Config.tileHeight/2) + row * (Config.tileHeight/2)
    return [x, y]

def isoHeightMapCoordinates(cellData):
    # Isometric Coordinates
    x, y = isoCoordinates(cellData.x, cellData.y)
    # Tile Height
    y -= cellData.h * Config.tileWallHeight
    return [x, y]

class Cell:
    def __init__(self, x, y, h=0):
        self.x = x
        self.y = y
        self.h = h
    def xy(self):
        return (self.x, self.y)

class GroundTile:
    def __init__(self, groundTexture=None, wallTexture=None):
        self.groundTexture = groundTexture
        self.wallTexture = wallTexture
    def render(self, height):
        dimensions = (Config.tileWidth, Config.tileHeight + height * Config.tileWallHeight)
        tile = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        tile.blit(self.groundTexture, (0,0))
        for h in range(height):
            y = Config.tileHeight/2 + h * Config.tileWallHeight
            tile.blit(self.wallTexture, (0, y))
        return tile

class IsoGrid:
    def __init__(self, dimensions, data):
        self.width, self.height = dimensions
        self.data = data

    def __getitem__(self, coord):
        if type(coord) == tuple or type(coord) == list:
            return self.data[coord[0]][coord[1]]
        else:
            return self.data[coord % self.width][coord / self.width]
    def __setitem__(self, coord, value):
        if type(coord) == tuple:
            self.data[coord[0]][coord[1]] = value
        else:
            self.data[coord % self.width][coord / self.width] = value
    def validCoord(self, coord):
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height
    def renderCell(self, surface, cellData, offset, selected=False):
        cell = self.data[cellData.x][cellData.y]
        if cell == None:
            return
        tile = cell.render(cellData.h)
        if selected:
            c = overlayLevel(0, 64)
            tile.fill((c,c,0), special_flags=pygame.BLEND_ADD)
        x, y = isoHeightMapCoordinates(cellData)
        # Offset
        x += offset[0]
        y += offset[1]
        surface.blit(tile, (x,y))

class Action:
    def __init__(self, playerSpriteIds=[0], prepTime=int(0), cooldown=int(0), target=None, overlaySprites=[]):
        self.prepTime = prepTime
        self.cooldown = cooldown
        self.playerFrame = 0
        self.overlayFrame = 0
        self.playerSpriteIds = playerSpriteIds
        self.overlaySprites = overlaySprites
        self.target = target
    def getPlayerSpriteId(self):
        return self.playerSpriteIds[self.playerFrame]
    def tick(self, player, engine):
        if player.mode == Player.Mode.Moving:
            self.do(player, engine)
        self.playerFrame += 1
        if self.playerFrame >= len(self.playerSpriteIds):
            self.playerFrame = 0
        self.overlayFrame += 1
        if self.overlayFrame >= len(self.overlaySprites):
            self.overlayFrame = 0
    def do(self, player, engine):
        self.doneAction(player)
    def doneAction(self, player):
        player.nextMode()
    def __repr__(self):
        return "<Action(prep='%d', cooldown='%d' playerFrame='%d')>" % (self.prepTime, self.cooldown, self.playerFrame)

class WalkAction(Action):
    def __init__(self, playerSpriteIds=[0], prepTime=int(0), cooldown=int(0), target=None, overlaySprites=[]):
        Action.__init__(self, playerSpriteIds, prepTime, cooldown, target, overlaySprites)
        self.path = None
        if self.target:
            self.thisCell = None
            self.nextCell = None
            self.thisCellCoord = None
            self.nextCellCoord = None
            self.jumpHeight = 0
    def do(self, player, engine):
        if self.target and self.path == None:
            self.path = engine.scene.pathTo(engine.scene.playerGrid.find(player), self.target)
            if self.path != None:
                self.path.pop(0)
            self.playerFrame = 0
        if self.path == None:
            self.doneAction(player)
        else:
            if len(self.path) > 0:
                if self.playerFrame == 0:
                    self.nextCell = self.path.pop(0)
                    self.thisCell = engine.scene.playerGrid.find(player)
                    player.rotate(self.nextCell[0]-self.thisCell[0], self.nextCell[1]-self.thisCell[1])
                    #print self.path
                    if len(self.playerSpriteIds) > 0:
                        nextCellData = engine.scene[self.nextCell]
                        thisCellData = engine.scene[self.thisCell]
                        self.nextCellCoord = isoHeightMapCoordinates(nextCellData)
                        self.thisCellCoord = isoHeightMapCoordinates(thisCellData)
                        self.jumpHeight = nextCellData.h - thisCellData.h

            if len(self.playerSpriteIds) > 0:
                dx = self.nextCellCoord[0]-self.thisCellCoord[0]
                dy = self.nextCellCoord[1]-self.thisCellCoord[1]

                ox = dx/len(self.playerSpriteIds)*(self.playerFrame+1)
                oy = dy/len(self.playerSpriteIds)*(self.playerFrame+1)
                #if self.playerFrame > len(self.playerSpriteIds)/2:
                #    oy += self.jumpHeight*Config.tileWallHeight/len(self.playerSpriteIds)/2
                if self.jumpHeight > 0:
                    oy += -(self.jumpHeight)*(self.playerFrame-len(self.playerSpriteIds))**2
                elif self.jumpHeight < -2:
                    oy += self.jumpHeight*Config.tileWallHeight*self.playerFrame
                player.offset = (ox, oy)

            if self.playerFrame == len(self.playerSpriteIds)-1:
                player.offset = None
                engine.scene.playerGrid.move(self.thisCell, self.nextCell)
                if len(self.path) == 0:
                    self.doneAction(player)
    def __repr__(self):
        return "<WalkAction(prep='%d', cooldown='%d' playerFrame='%d')>" % (self.prepTime, self.cooldown, self.playerFrame)




class Player:
    class Dir:
        E, S, W, N = range(4)
    class Mode:
        Wait, Ready, Prep, Moving, Cooldown = range(5)
        def __len__():
            return 5
    def __init__(self, sprites):
        self.name = "Chris"
        self.mode = Player.Mode.Wait
        self.direction = 0
        self.sprites = sprites
        self.currentAction = Action(Config.playerWaitSpriteIds)
        self.offset = None
        self.nextAction = 0
        self.stat = {}
        for statName in Config.statNames:
            self.stat[statName] = 1
    def playerSpriteId(self):
        if self.currentAction == None:
            return 0
        else:
            return self.currentAction.getPlayerSpriteId()
    def render(self, height):
        return self.sprites[self.playerSpriteId()][self.direction].copy()
    def doAction(self, action):
        if self.mode == Player.Mode.Ready:
            self.currentAction = action
            self.nextMode()
    def nextMode(self):
        self.mode += 1
        if self.mode > 4:
            self.mode = 0

        if self.mode == Player.Mode.Wait:
            self.nextAction = Config.waitTime
            self.currentAction = Action(Config.playerWaitSpriteIds)
        elif self.mode == Player.Mode.Prep:
            self.nextAction = self.currentAction.prepTime
        elif self.mode == Player.Mode.Cooldown:
            self.nextAction = self.currentAction.cooldown
        else:
            self.nextAction = 0
    def tick(self, engine):
        if self.mode == Player.Mode.Moving:
            if self.currentAction:
                self.currentAction.tick(self, engine)
        elif self.mode == Player.Mode.Ready:
            pass
        else:
            self.nextAction -= self.stat['Speed']
            if self.nextAction <= 0:
                self.nextMode()
    def rotate(self, x, y):
        if x > 0:
            self.direction = 0
        elif x < 0:
            self.direction = 2
        elif y > 0:
            self.direction = 1
        elif y < 0:
            self.direction = 3
    def __repr__(self):
        return "<Player(mode='%d', next='%d' dir='%d', action='%s' stat='%s')>" % (self.mode, self.nextAction, self.direction, self.currentAction, self.stat)




class PlayerGrid(IsoGrid):
    def __init__(self, dimensions):
        width, height = dimensions
        IsoGrid.__init__(self, dimensions, [[None for y in range(height)] for x in range(width)])
        self.players = []
    def move(self, a, b):
        if self.validCoord(a) and self.validCoord(b) and self[b] == None:
            self[b] = self[a]
            self[a] = None
            return True
        return False
    def moveTo(self, player, target):
        if self[target] == None:
            coord = self.find(player)
            return self.move(coord, target)
        return False
    def addPlayer(self, player, coord):
        if self[coord]:
            raise Exception, "Player already at that location"
        self.players.append(player)
        self[coord] = player
    def renderCell(self, surface, cellData, offset, selected=False):
        offsetX = offset[0]
        offsetY = offset[1] - Config.playerSpriteHeight + Config.tileHeight
        player = self[cellData.xy()]
        if player and player.offset:
            offsetX += player.offset[0]
            offsetY += player.offset[1]
        IsoGrid.renderCell(self, surface, cellData, (offsetX, offsetY), selected)
    def find(self, player):
        for y in range(self.height):
            for x in range(self.width):
                if self[(x,y)] == player:
                    return (x,y)
        return None
    def shiftPlayer(self, player, x, y):
        c = self.find(player)
        player.rotate(x, y)
        return self.move(c, (c[0]+x, c[1]+y))


class GroundGrid(IsoGrid):
    def __init__(self, dimensions):
        width, height = dimensions
        IsoGrid.__init__(self, dimensions, [[GroundTile() for y in range(height)] for x in range(width)])

class IsoScene(IsoGrid):
    def __init__(self, dimensions):
        width, height = dimensions
        IsoGrid.__init__(self, dimensions, [[Cell(x, y) for y in range(height)] for x in range(width)])
        self.groundGrid = GroundGrid(dimensions)
        self.playerGrid = PlayerGrid(dimensions)
        self.camera = [0, 0]
        self.layers = [self.groundGrid, self.playerGrid]
        self.renderOrder = [self[coord] for coord in isoGridRenderOrder(self.width, self.height)]
        self.selection = None
        self.hud = Hud(dimensions)
        self.selectedPlayer = None
        self.select(self.camera)

    def render(self, dimensions):
        surface = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        centeringOffset = isoCoordinates(self.camera[0], self.camera[1])
        offsetX = dimensions[0]/2 - (Config.tileWidth/2) - centeringOffset[0]
        offsetY = dimensions[1]/2 - (Config.tileHeight/2) - centeringOffset[1]
        for cell in self.renderOrder:
            self.renderCell(surface, cell, (offsetX, offsetY), cell == self.selection)
        self.hud.render(surface)
        return surface
    def renderCell(self, surface, cell, offset, selected=False):
        for layer in self.layers:
            layer.renderCell(surface, cell, offset, selected)
    def addPlayer(self):
        self.playerGrid
    def shiftCamera(self, x, y):
        self.camera[0] += x
        self.camera[1] += y
    def playerWalkTo(self, player, target):
        here = self.playerGrid.find(player)
        path = self.pathTo(here, target)
        if path:
            return self.playerGrid.shiftPlayer(player, path[1][0]-here[0], path[1][1]-here[1])
        return False
    def select(self, coord):
        if self.validCoord(coord):
            self.selection = self[coord]
            self.hud.selectedPlayerA = self.playerGrid[coord]
            self.camera = list(coord)
    def pathTo(self, a, b):
        if a == b:
            return None
        class Node:
            def __init__(self, root):
                self.root = root
        def neighbours(coord):
            x, y = coord
            return [(x+1,y), (x,y+1), (x-1,y), (x,y-1)]
        def getPath(grid, pathNodes, node):
            path = [n]
            node = nodes[n]
            while node.root != None:
                path.insert(0, node.root)
                node = nodes[node.root]
            return path
        WALKED = 2
        WALKABLE = 0
        WALL = 1
        dist = [[WALKABLE for y in range(self.height)] for x in range(self.width)]
        q = [a]
        for y in range(self.height):
            for x in range(self.width):
                if self.playerGrid[(x,y)] != None:
                    dist[x][y] = WALL
        dist[a[0]][a[1]] = WALKED
        nodes = {a : Node(None)}
        while len(q) > 0:
            here = q.pop(0)
            for n in neighbours(here):
                if self.validCoord(n) and self[here].h+Config.maxJumpHeight-self[n].h >= 0:
                    if n == b:
                        nodes[n] = Node(here)
                        return getPath(dist, nodes, here)
                    x, y = n
                    if dist[x][y] == WALKABLE:
                        q.append(n)
                        dist[x][y] = WALKED
                        nodes[n] = Node(here)
        return None
    def triggerSelection(self):
        if self.selectedPlayer:
            self.walkToSelection()
            self.selectedPlayer = None
        else:
            self.selectedPlayer = self.playerGrid[self.selection.xy()]

    def walkToSelection(self):
        if self.selectedPlayer:
            self.selectedPlayer.doAction(WalkAction(Config.playerWalkSpriteIds, 0, 0, self.selection.xy()))

class IsoTacticsEngine(PyGameEngine):
    def __init__(self, resolution, title, icon):
        PyGameEngine.__init__(self, resolution, title, icon)
        self.scene = None
        self.targetFPS = Config.framesPerSecond
    def load(self):
        self.tileSheet = Resource.TileSheet(Config.pathTiles, (64, 32))
        self.wallTileSheet = Resource.TileSheet(Config.pathTileWalls, (64, 24))
        self.playerSpriteSheets = [Resource.TileSheet(Config.pathPlayerSprites % i, (64, 128)) for i in range(Config.numPlayerSprites)]
        self.playerSprites = [[Resource.GameSprite([playerSpriteSheet[sprite*4+d] for d in range(4)]) for sprite in range(playerSpriteSheet.vert)] for playerSpriteSheet in self.playerSpriteSheets]
    def setup(self):
        dimensions = (random.randint(3, 10), random.randint(3, 10))
        scene = IsoScene(dimensions)
        n = 0
        for y in range(scene.height):
            for x in range(scene.width):
                groundTile = scene.groundGrid[(x, y)]
                groundTile.groundTexture = self.tileSheet[n]
                groundTile.wallTexture = self.wallTileSheet[n]
                scene[(x,y)].h = random.randint(0, 6)
                n += 1
        for i in range(4):
            player = Player(self.playerSprites[0])
            player.stat['Speed'] = 50
            player.stat['Hp'] = 100
            player.stat['MaxHp'] = 100
            scene.playerGrid.addPlayer(player, (i,0))
        self.loadScene(scene)

    def keyInput(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_p:
            self.paused = True
        elif key == pygame.K_g:
            self.setup()
        elif key == pygame.K_RIGHT:
            self.shift(1, 0)
        elif key == pygame.K_DOWN:
            self.shift(0, 1)
        elif key == pygame.K_LEFT:
            self.shift(-1, 0)
        elif key == pygame.K_UP:
            self.shift(0, -1)
        elif key == pygame.K_SPACE:
            self.scene.triggerSelection()
    def gameTick(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.scene.render(self.resolution), (0, 0))
        for player in self.scene.playerGrid.players:
            player.tick(self)
            #print player

    def loadScene(self, scene):
        self.scene = scene
    def shift(self, x, y):
        #if self.scene.playerGrid.shiftPlayer(self.player, x, y):
        self.scene.select((self.scene.camera[0]+x, self.scene.camera[1]+y))
    def secTick(self):
        #player = self.scene.selectedPlayer
        #self.scene.playerWalkTo(self.scene.selectedPlayer, (0,0))
        pass

def main():
    e = IsoTacticsEngine(Config.resolution, Config.title, pygame.image.load(Config.pathIcon))
    e.load()
    e.setup()
    e.run()

if __name__ == '__main__':
    main()