'''
Dinosaur Game
'''

import random
import pygame
import numpy as np
from pygame.locals import *

class Dinosaur:

    def __init__(self):
        
        self.size = (25, 50)
        self.position = self.x, self.y = (50, 250)
        self.speed = 0
        self.ducking = False

    def toggle_duck(self):
        '''
        Toggle the ducking state of the dinosaur
        '''
        self.ducking = not self.ducking

    def check_positiion(self):
        '''
        Modifies the current position of the Dinosuar, in its
        standing, ducking and jumping (not implemented yet) states
        '''
        if self.ducking:
            self.size = (50, 25)
            self.position = (50, 275)
        
        else:
            self.size = (25, 50)
            self.position = (50, 250)

    def draw(self, surface):
        '''
        Draw dino onto surface.
        In it's current state, it just draws the hitbox
        of the dinosaur
        '''
        body = pygame.Rect(self.position, self.size)
        pygame.draw.rect(surface, (0, 200, 0), body)


class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.clock = None

        # Player
        self.dino = Dinosaur()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == K_DOWN:
                print("Down!")
                self.dino.toggle_duck()

    def on_loop(self):

        # Check current position (well, its really the size right not) of dina
        self.dino.check_positiion()

    def on_render(self):
        # White Background
        self._display_surf.fill((255, 255, 255))

        # Draw ground
        ground = pygame.Rect(((0, 300), (self.width, 10)))
        pygame.draw.rect(self._display_surf, (128, 128, 128), ground)

        # Draw dinoasur
        self.dino.draw(self._display_surf)

        # Update display
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute() 