'''
Dinosaur Game
'''

import random
import pygame
import numpy as np
from pygame.locals import *

class Dinosaur:

    DINO_SIZE_STAND = (25, 50)
    DINO_POS_STAND = (50, 250)
    DINO_SIZE_DUCK = (50, 25)
    DINO_POS_DUCK = (50, 275)


    def __init__(self):
        
        self.size = self.DINO_SIZE_STAND
        self.position = self.x, self.y = self.DINO_POS_STAND
        self.speed = 0
        self.score = 0
        self.ducking = False

    def toggle_duck(self):
        '''
        Toggle the ducking state of the dinosaur
        '''
        self.ducking = not self.ducking
        # Little test to be srue score is working
        self.score += 10

    def check_positiion(self):
        '''
        Modifies the current position of the Dinosuar, in its
        standing, ducking and jumping (not implemented yet) states
        '''
        if self.ducking:
            self.size = self.DINO_SIZE_DUCK
            self.position = self.DINO_POS_DUCK
        
        else:
            self.size = self.DINO_SIZE_STAND
            self.position = self.DINO_POS_STAND

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
        pygame.display.set_caption("Dino Game")
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()

        # Init for text
        self.score_font = pygame.font.SysFont('timesnewroman', 20)
	


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

        # Display score in left corner
        score = self.score_font.render(str(self.dino.score), True, (128, 128, 128))
        self._display_surf.blit(score, (10, 5))

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
            self.clock.tick(30)

        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute() 