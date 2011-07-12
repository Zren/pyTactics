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

class Menu:
    def __init__(self, children={}, root=None):
        self.children = children
        self.root = root

class Hud:
    menu = None
    selectedUnitA, selectedUnitB = None, None
    helpText = None

    def render():
        return pygame.Suface(Config.resolution)


def main():
    pass

if __name__ == '__main__':
    main()
