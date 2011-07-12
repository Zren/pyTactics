#-------------------------------------------------------------------------------
# Name:        pyTactics
#              A python attempt at a FF Tactics-esque game.
#
# Author:      Chris Holland (Zren)
#
# Created:     11/07/2011
# Copyright:   (c) Chris Holland 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
import Config, Resource
from PyGameEngine import PyGameEngine
from IsoTacticsEngine import IsoTacticsEngine



def main():
    e = IsoTacticsEngine(Config.title, pygame.image.load(Config.pathIcon))
    e.load()
    e.setup()
    e.run()
if __name__ == '__main__':
    main()
