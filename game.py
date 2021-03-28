'''
Dinosaur Game
'''

import random
import pygame
import numpy as np
from pygame.locals import *

class Dinosaur:

    DINO_SIZE_STAND_X = 25
    DINO_SIZE_STAND_Y = 50
    DINO_POS_STAND_X = 50
    DINO_POS_STAND_Y = 250
    DINO_SIZE_DUCK_X = 50
    DINO_SIZE_DUCK_Y = 25
    DINO_POS_DUCK_X = 50
    DINO_POS_DUCK_Y = 275

    DINO_JUMP_MAX = 150

    def __init__(self):
        
        self.size = (self.DINO_SIZE_STAND_X, self.DINO_SIZE_STAND_Y)
        self.position = self.x, self.y = (self.DINO_POS_STAND_X, self.DINO_POS_STAND_Y)
        self.speed = 0
        self.score = 0
        self.ducking = False
        self.jumping = False
        self.reachedTop = False

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
        # Jump
        if self.jumping:
            self.jump()

        # Duck
        elif self.ducking:
            self.size = (self.DINO_SIZE_DUCK_X, self.DINO_SIZE_DUCK_Y)
            self.position = (self.DINO_POS_DUCK_X, self.DINO_POS_DUCK_Y)

        # Move normally
        else:
            self.size = (self.DINO_SIZE_STAND_X, self.DINO_SIZE_STAND_Y)
            self.position = (self.DINO_POS_STAND_X, self.DINO_POS_STAND_Y)

    def jump(self):

        # Jump until max jump height is reached
        if self.position[1] > self.DINO_JUMP_MAX and not self.reachedTop:
            self.position = (self.position[0], self.position[1] - 10)

        # Decrease Jump going back down
        else:
            self.reachedTop = True
            self.position = (self.position[0], self.position[1] + 10)
        
        # Stop jump once groun is reached
        if self.position[1] == self.DINO_POS_STAND_Y:
            self.jumping = False
            self.reachedTop = False


    def draw(self, surface):
        '''
        Draw dino onto surface.
        In it's current state, it just draws the hitbox
        of the dinosaur
        '''
        body = pygame.Rect(self.position, self.size)
        pygame.draw.rect(surface, (0, 200, 0), body)

class Obs:

    def __init__(self):

        self.length = 50
        self.width = 50
        self.pos = [400, 200]

    def move(self):
        self.pos[0] -= 10

    def draw(self, surface):

        body = pygame.Rect(self.pos, (self.length, self.width))
        pygame.draw.rect(surface, (0, 0, 0), body)


class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.clock = None

        # Player
        self.dino = Dinosaur()

        # Test - Just draw an obstacle
        self.bad = Obs()

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Dino Game")
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()

        # Init for text
        self.score_font = pygame.font.SysFont('mono', 20)
	
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == K_DOWN:
                # Can't duck when Jumping!
                if self.dino.jumping is False:
                    print("Down!")
                    self.dino.ducking = True
            
            if event.key == K_SPACE or event.key == K_UP:
                # Can't Jump when ducking!
                if self.dino.ducking is False:
                    print("Jump!")
                    self.dino.jumping = True

        else:
            self.dino.ducking = False

    def on_loop(self):

        # Check current position (well, its really the size right not) of dina
        self.dino.check_positiion()

        self.bad.move()

    def on_render(self):
        # White Background
        self._display_surf.fill((255, 255, 255))

        # Draw ground
        ground = pygame.Rect(((0, 300), (self.width, 10)))
        pygame.draw.rect(self._display_surf, (128, 128, 128), ground)

        # Draw dinoasur
        self.dino.draw(self._display_surf)

        # Draw obstacles
        self.bad.draw(self._display_surf)

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