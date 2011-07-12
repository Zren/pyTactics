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
import time

class PyGameEngine:
    def __init__(self, title, icon):
        print "Initialize PyGame"
        pygame.init()
        self.title = title
        self.icon = icon
        self.paused = False
        self.fpsCounter = 0
        self.lastFPSTime = pygame.time.get_ticks()
        self.running = 1
        self.targetFPS = 30
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.title)
    def pausedInput(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p:
                    self.paused = False
    def gameInput(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keyInput(event.key)
            elif event.type == pygame.USEREVENT:
                self.userEvent()
            #else: #Print All Unknown Events (Gets flooded with Mouse Interaction)
                #print event
    def keyInput(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_p:
            self.paused = True
    def userEvent(self):
        self.fpsCounter += 1
        if pygame.time.get_ticks() - self.lastFPSTime >= 1000:
            #print "FPS:", self.fpsCounter
            self.fpsCounter = 0
            self.lastFPSTime = pygame.time.get_ticks()
    def run(self):
        pygame.time.set_timer(pygame.USEREVENT, int(1000.0 / self.targetFPS + 0.5))
        print "Stepping every %d ticks" % int(1000.0 / self.targetFPS + 0.5)
        last_sec = time.time()
        frames = 0
        while self.running:
            if self.paused:
                self.pausedInput(pygame.event.get())
            else:
                self.gameInput(pygame.event.get())
                self.gameTick()
            pygame.display.flip()
            frames += 1
            if time.time() - last_sec >= 1:
                print "FPS:",frames
                frames = 0
                last_sec = time.time()
        pygame.quit()
    def gameTick(self):
        pass

def main():
    pass

if __name__ == '__main__':
    main()
