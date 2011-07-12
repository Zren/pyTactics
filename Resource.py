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

from Config import Config
import pygame

class Tile:
    def render(ground, wall, z):
        tile = pygame.Surface((Config.tileWidth, Config.tileHeight + z * Config.tileWallHeight))
        tile.blit(ground, (0,0))
        for y in range(Config.tileHeight, tile.get_height(), Config.tileWallHeight):
            tile.blit(wall, (0, y))
        return tile

# Origional Author: www.scriptefun.com/transcript-2-using
# Edited
class TileSheet:
    def __init__(self, filename, tileSize):
        try:
            self.sheet = pygame.image.load(filename).convert()
            w,h = tileSize
            rects = [[(x, y, x+w-1, y+h-1) for x in range(0, self.sheet.get_width(), w)] for y in range(0, self.sheet.get_height())]
            self.sprites = images_at(rects)
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

class GameSprite():
    class Dir:
        E, S, W, N = range(4)
    def __init__(self, sprites):
        self.sprites = sprites
    def render(direction):
        return self.sprites[direction]


tiles = TileSheet("sprites/tile.png", (64, 32))
tileWalls = TileSheet("sprites/tile-wall.png", (64, 24))