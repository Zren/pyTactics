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

class Cell:
    def __init__(self, x, y, h=0):
        self.x = x
        self.y = y
        self.h = h

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
        if type(coord) == tuple:
            return self.data[coord[0]][coord[1]]
        else:
            return self.data[coord % self.width][coord / self.width]
    def __setitem__(self, coord, value):
        if type(coord) == tuple:
            self.data[coord[0]][coord[1]] = value
        else:
            self.data[coord % self.width][coord / self.width] = value
    def renderCell(self, surface, cellData, offset, selected=False):
        cell = self.data[cellData.x][cellData.y]
        if cell == None:
            return
        tile = cell.render(cellData.h)
        if selected:
            c = overlayLevel(64, 128)
            tile.fill((c,c,0), special_flags=pygame.BLEND_ADD)
        # Isometric Coordinates
        x, y = isoCoordinates(cellData.x, cellData.y)
        # Tile Height
        y -= cellData.h * Config.tileWallHeight
        # Offset
        x += offset[0]
        y += offset[1]
        surface.blit(tile, (x,y))

class Player:
    class Dir:
        E, S, W, N = range(4)
    def __init__(self, sprites):
        self.currentAction = None
        self.direction = 0
        self.sprites = sprites
    def render(self, height):
        #tile = pygame.Surface((0,0), pygame.SRCALPHA, 32)
        return self.sprites[0][0].copy()
        #return tile

class PlayerGrid(IsoGrid):
    def __init__(self, dimensions):
        width, height = dimensions
        IsoGrid.__init__(self, dimensions, [[None for y in range(height)] for x in range(width)])
        self.players = []
    def move(self, a, b):
        if self[b] == None:
            self[b] = self[a]
            self[a] = None
    def moveTo(self, player, target):
        if self[target] == None:
            coord = self.find(player)
            self.move(coord, target)
    def addPlayer(self, player, coord):
        if self[coord]:
            raise Exception, "Player already at that location"
        self.players.append(player)
        self[coord] = player
    def renderCell(self, surface, cellData, offset, selected=False):
        IsoGrid.renderCell(self, surface, cellData, (offset[0], offset[1]-Config.playerSpriteHeight+Config.tileHeight), selected)
    def find(self, player):
        for y in range(self.height):
            for x in range(self.width):
                if self[(x,y)] == player:
                    return (x,y)
        return None
    def shiftPlayer(self, player, x, y):
        c = self.find(player)
        self.move(c, (c[0]+x, c[1]+y))


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

    def update(self):
        pass

    def render(self, dimensions):
        surface = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        centeringOffset = isoCoordinates(self.camera[0], self.camera[1])
        offsetX = dimensions[0]/2 - (Config.tileWidth/2) - centeringOffset[0]
        offsetY = dimensions[1]/2 - (Config.tileHeight/2) - centeringOffset[1]
        for cell in self.renderOrder:
            self.renderCell(surface, cell, (offsetX, offsetY), cell == self.selection)
        return surface
    def renderCell(self, surface, cell, offset, selected=False):
        for layer in self.layers:
            layer.renderCell(surface, cell, offset, selected)
    def addPlayer(self):
        self.playerGrid
    def shiftCamera(self, x, y):
        self.camera[0] += x
        self.camera[1] += y

class IsoTacticsEngine(PyGameEngine):
    def __init__(self, resolution, title, icon):
        PyGameEngine.__init__(self, resolution, title, icon)
        self.scene = None
        self.targetFPS = Config.framesPerSecond
    def load(self):
        self.tileSheet = Resource.TileSheet(Config.pathTiles, (64, 32))
        self.wallTileSheet = Resource.TileSheet(Config.pathTileWalls, (64, 24))
        self.playerSpriteSheets = [Resource.TileSheet(Config.pathPlayerSprites % i, (64, 128)) for i in range(Config.numPlayerSprites)]
        self.playerSprites = [[Resource.GameSprite([playerSpriteSheet[d] for d in range(4)]) for sprite in range(playerSpriteSheet.vert)] for playerSpriteSheet in self.playerSpriteSheets]
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
        self.player = Player(self.playerSprites[0])
        scene.playerGrid.addPlayer(self.player, (0,0))
        self.loadScene(scene)

    def keyInput(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_p:
            self.paused = True
        elif key == pygame.K_g:
            self.setup()
        elif key == pygame.K_RIGHT:
            self.scene.shiftCamera(1, 0)
            self.shift(1, 0)
        elif key == pygame.K_DOWN:
            self.scene.shiftCamera(0, 1)
            self.shift(0, 1)
        elif key == pygame.K_LEFT:
            self.scene.shiftCamera(-1, 0)
            self.shift(-1, 0)
        elif key == pygame.K_UP:
            self.scene.shiftCamera(0, -1)
            self.shift(0, -1)
    def gameTick(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.scene.render(self.resolution), (0, 0))
    def loadScene(self, scene):
        self.scene = scene
    def shift(self, x, y):
        self.scene.playerGrid.shiftPlayer(self.player, x, y)
        self.scene.selection = self.scene[self.scene.playerGrid.find(self.player)]







def main():
    e = IsoTacticsEngine(Config.resolution, Config.title, pygame.image.load(Config.pathIcon))
    e.load()
    e.setup()
    e.run()

if __name__ == '__main__':
    main()