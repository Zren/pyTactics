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
hudFontSize = 20



def main():
    pass

if __name__ == '__main__':
    main()
