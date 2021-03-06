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

import sys

title = "pyTactics"
resolution = (800, 600)
tileSize = (64, 32)
tileWidth, tileHeight = tileSize
tileWallHeight = 8
playerSpriteHeight = 128
pathImages = sys.path[0] + "\\img\\"
pathTiles = pathImages + "tile.png"
pathTileWalls = pathImages + "tile-wall.png"
pathIcon = pathImages + "icon.png"
numPlayerSprites = 1
pathPlayerSprites = pathImages + "player-%d.png"
framesPerSecond = 8

maxJumpHeight = 4

pathFonts = sys.path[0] + "\\font\\"
pathHudFont = pathFonts + "UnZialish.ttf"
statNames = ['Hp', 'MaxHp', 'Strength', 'Speed', 'Defence']
waitTime = 100

playerWaitSpriteIds = [0, 1]
playerWalkSpriteIds = [2, 3, 4, 5]

hudSelectionSize = (resolution[0]/4, resolution[1]/4)
hudSelectionPosA = (0, resolution[1]-hudSelectionSize[1])
hudSelectionPosB = (resolution[0]-hudSelectionSize[0], resolution[1]-hudSelectionSize[1])

hudBgColor = (32, 32, 32, 128)
hudFontColor = (255, 255, 255)

hudNameFontSize = 20
hudNamePadding = 5

hudStatBarFontSize = 10
hudStatBarPadding = 2
hudStatBarSize = (hudSelectionSize[1]-hudStatBarPadding*2, hudNameFontSize)
hudStatBarColorA = (255, 0, 0)
hudStatBarColorB = (0, 0, 255)





def main():
    pass

if __name__ == '__main__':
    main()
