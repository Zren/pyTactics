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
import math

class Menu:
    def __init__(self, children={}, root=None):
        self.children = children
        self.root = root

class Hud:
    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.fontName = pygame.font.Font(Config.pathHudFont, Config.hudNameFontSize)
        self.fontStatBar = pygame.font.Font(Config.pathHudFont, Config.hudStatBarFontSize)
        self.menu = None
        self.selectedPlayerA = None
        self.selectedPlayerB = None
        self.helpText = None

    def render(self, surface):
        if self.selectedPlayerA:
            self.renderPlayerPanel(surface, Config.hudSelectionPosA, Config.hudSelectionSize, self.selectedPlayerA)
        if self.selectedPlayerB:
            self.renderPlayerPanel(surface, Config.hudSelectionPosB, Config.hudSelectionSize, self.selectedPlayerB)
    def renderPlayerPanel(self, surface, offset, dimensions, player):
        nameRender = self.fontName.render(player.name, True, Config.hudFontColor)
        nameBoxHeight = nameRender.get_height()+Config.hudNamePadding*2
        nameRect = (offset[0], offset[1], nameRender.get_width()+Config.hudNamePadding*2, nameBoxHeight)
        drawRoundedRect(surface, Config.hudBgColor, nameRect, Config.hudNamePadding, 0)
        surface.blit(nameRender, (offset[0]+Config.hudNamePadding, offset[1]+Config.hudNamePadding))

        statBarOffset = (offset[0], offset[1]+nameRect[3], dimensions[0], Config.hudNameFontSize+Config.hudStatBarPadding*2)
        current, maximum = player.stat['Hp'], player.stat['MaxHp']
        statBarText = "%s: %d/%d" % ("HP", current, maximum)
        self.renderPlayerStatBar(surface, Config.hudStatBarColorA, statBarOffset, Config.hudStatBarSize, statBarText, current, maximum)
    def renderPlayerStatBar(self, surface, color, offset, dimensions, text, current, maximum):
        statNameRender = self.fontStatBar.render(text, True, Config.hudFontColor)
        drawRoundedRect(surface, Config.hudBgColor, (offset[0], offset[1], dimensions[0]+Config.hudStatBarPadding*2, dimensions[1]+Config.hudStatBarPadding*2), Config.hudStatBarPadding, 0)

        fullBarRect = [offset[0]+Config.hudStatBarPadding, offset[1]+Config.hudStatBarPadding, dimensions[0], dimensions[1]]
        if current > 0:
            if current > maximum:
                ratio = 1
            else:
                ratio = current/(0.0+maximum)
            fgBarRect = fullBarRect
            fgBarRect[2] = dimensions[0] * ratio
            pygame.draw.rect(surface, color, fgBarRect, 0)
        if current < maximum:
            r,g,b = color
            pygame.draw.rect(surface, (r/2,g/2,b/2, 178), fullBarRect, 0)



def drawRoundedRect(surface, color, rect, radius, width=0):
    x, y, w, h = rect
    assert w >= radius*2 and h >= radius*2
    for p in [(x+radius, y+radius), (x+w-radius, y+radius), (x+radius, y+h-radius), (x+w-radius, y+h-radius)]:
        pygame.draw.circle(surface, color, p, radius, width)
    pygame.draw.rect(surface, color, (x+radius, y, w-radius*2, h), width)
    pygame.draw.rect(surface, color, (x, y+radius, w, h-radius*2), width)



def main():
    pass

if __name__ == '__main__':
    main()
