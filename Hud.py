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
import Config

class Menu:
    def __init__(self, children={}, root=None):
        self.children = children
        self.root = root

class Hud:
    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.font = pygame.font.Font(Config.pathHudFont, Config.hudFontSize)
        self.menu = None
        self.selectedUnitA = None
        self.selectedUnitB = None
        self.helpText = None

    def render(self, surface):
        if self.selectedUnitA:
            surface.blit(surface, (0,0))


def main():
    pass

if __name__ == '__main__':
    main()
