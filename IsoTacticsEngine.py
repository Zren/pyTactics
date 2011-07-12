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

class Cell:
    def __init__(self, x, y, h=0, groundTextureId=0, wallTextureId=0):
        self.x = x
        self.y = y
        self.h = h
        self.groundTextureId = groundTextureId
        self.wallTextureId = wallTextureId
    def render(self, tileSheet, wallTileSheet):
        dimensions = (Config.tileWidth, Config.tileHeight + self.h * Config.tileWallHeight)
        tile = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        tile.blit(tileSheet[self.groundTextureId], (0,0))
        for h in range(self.h):
            y = Config.tileHeight/2 + h * Config.tileWallHeight
            tile.blit(wallTileSheet[self.wallTextureId], (0, y))
        return tile


class IsoGrid:
    def __init__(self, dimensions, tileSheet, wallTileSheet):
        self.width, self.height = dimensions
        self.data = [[Cell(x,y) for y in range(self.height)] for x in range(self.width)]
        self.tileSheet = tileSheet
        self.wallTileSheet = wallTileSheet
    def __getitem__(self, coord):
        try:
            return self.data[coord[0]][coord[1]]
        except:
            return self.data[coord % self.width][coord / self.width]
    def render(self, dimensions, centerOnCell=(0,0)):
        surface = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        col, row = 0, 0
        while True:
            cell = self.data[col][row]
            tile = cell.render(self.tileSheet, self.wallTileSheet)
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

            if col == self.width && row == self.height:
                break
            col -= 1
            row += 1
            if col < 0:

        return surface

class IsoScene:
    def __init__(self, isoGrid):
        self.isoGrid = isoGrid

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
        isoGrid = IsoGrid((10, 10), self.tileSheet, self.wallTileSheet)
        n = 0
        import random
        for y in range(isoGrid.height):
            for x in range(isoGrid.height):
                cell = isoGrid[(x, y)]
                cell.groundTextureId = n
                cell.h = random.randint(0, 6)
                n += 1
        self.screen.fill((0, 0, 0))
        self.screen.blit(isoGrid.render(Config.resolution), (0,0))
        self.loadScene(IsoScene(isoGrid))

    def keyInput(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_p:
            self.paused = True
        elif key == pygame.K_g:
            self.setup()
    #def gameTick(self):
    #    pass
    def loadScene(self, scene):
        self.scene = scene






def main():
    e = IsoTacticsEngine(Config.title, pygame.image.load(Config.pathIcon))
    e.load()
    e.setup()
    e.run()

if __name__ == '__main__':
    main()