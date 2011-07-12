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

import Config
import pygame



# Origional Author: www.scriptefun.com/transcript-2-using
# Edited
class TileSheet:
    def __init__(self, filename, tileSize):
        self.sheet = pygame.image.load(filename).convert_alpha()
        w,h = tileSize
        rects = []
        for y in range(0, self.sheet.get_height()):
            for x in range(0, self.sheet.get_width(), w):
                rects.append(pygame.Rect(x, y, w, h))
        self.sprites = self.images_at(rects)
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    def __getitem__(self, i):
        return self.sprites[i];

class GameSprite():
    class Dir:
        E, S, W, N = range(4)
    def __init__(self, sprites):
        self.sprites = sprites
    def render(direction):
        return self.sprites[direction]