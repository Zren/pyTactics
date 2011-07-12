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

class Unit:
    def __init__(self):
        self.currentAction = None

class Cell:
    def __init__(self, x, y, h=0, groundTexture=None, wallTexture=None):
        self.x = x
        self.y = y
        self.h = h
        self.groundTexture = groundTexture
        self.wallTexture = wallTexture
    def render(self):
        dimensions = (Config.tileWidth, Config.tileHeight + self.h * Config.tileWallHeight)
        tile = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        tile.blit(self.groundTexture, (0,0))
        for h in range(self.h):
            y = Config.tileHeight/2 + h * Config.tileWallHeight
            tile.blit(self.wallTexture, (0, y))
        return tile

class IsoGrid:
    def __init__(self, dimensions, data):
        self.width, self.height = dimensions
        self.data = data
        self.renderOrder = isoGridRenderOrder(self.width, self.height)
    def __getitem__(self, coord):
        try:
            return self.data[coord[0]][coord[1]]
        except:
            return self.data[coord % self.width][coord / self.width]
    def render(self, dimensions, centerOnCell=(0,0)):
        surface = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        for coord in self.renderOrder:
            col, row = coord
            cell = self.data[col][row]
            if cell == None:
                continue
            tile = cell.render()
            # Isometric Coordinates
            x = col * (Config.tileWidth/2) - row * (Config.tileWidth/2)
            y = col * (Config.tileHeight/2) + row * (Config.tileHeight/2)
            # Tile Height
            y -= cell.h * Config.tileWallHeight
            # Center on surface
            x += dimensions[0]/2
            y += dimensions[1]/2
            # Center on tile
            x -= (Config.tileWidth/2)
            y -= (Config.tileHeight/2)
            # Centering offset
            x += centerOnCell[0] * Config.tileWidth
            y += centerOnCell[1] * Config.tileHeight
            surface.blit(tile, (x,y))
        return surface


class PlayerGrid(IsoGrid):
    def __init__(self, dimensions):
        width, height = dimensions
        IsoGrid.__init__(self, dimensions, [[None for y in range(height)] for x in range(width)])

class GroundGrid(IsoGrid):
    def __init__(self, dimensions):
        width, height = dimensions
        IsoGrid.__init__(self, dimensions, [[Cell(x,y) for y in range(height)] for x in range(width)])


class IsoScene:
    def __init__(self, groundGrid, playerGrid):
        self.groundGrid = groundGrid
        self.playerGrid = playerGrid
        self.camera = (0, 0)
        self.layers = [self.groundGrid, self.playerGrid]

    def render(self, dimensions):
        surface = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        for layer in self.layers:
            surface.blit(layer.render(dimensions, self.camera), (0,0))
        return surface

class IsoTacticsEngine(PyGameEngine):
    def __init__(self, title, icon):
        PyGameEngine.__init__(self, title, icon)
        self.screen = pygame.display.set_mode(Config.resolution)
        pygame.init()
        self.scene = None
    def load(self):
        self.tileSheet = Resource.TileSheet(Config.pathTiles, (64, 32))
        self.wallTileSheet = Resource.TileSheet(Config.pathTileWalls, (64, 24))
    def setup(self):
        import random
        dimensions = (random.randint(3, 10), random.randint(3, 10))
        isoGrid = GroundGrid(dimensions)
        n = 0
        for y in range(isoGrid.height):
            for x in range(isoGrid.width):
                cell = isoGrid[(x, y)]
                cell.groundTexture = self.tileSheet[n]
                cell.wallTexture = self.wallTileSheet[n]
                cell.h = random.randint(0, 6)
                n += 1
        #self.screen.fill((0, 0, 0))
        #self.screen.blit(isoGrid.render(Config.resolution), (0,0))
        self.loadScene(IsoScene(isoGrid, PlayerGrid(dimensions)))

    def keyInput(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_p:
            self.paused = True
        elif key == pygame.K_g:
            self.setup()
    def gameTick(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.scene.render(Config.resolution), (0, 0))
    def loadScene(self, scene):
        self.scene = scene






def main():
    e = IsoTacticsEngine(Config.title, pygame.image.load(Config.pathIcon))
    e.load()
    e.setup()
    e.run()

if __name__ == '__main__':
    main()