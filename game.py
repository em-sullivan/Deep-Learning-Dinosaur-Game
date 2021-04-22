'''
Dinosaur Game
'''

import random
import pygame
import numpy as np
from pygame.locals import *

class Dinosaur:

    DINO_SIZE_STAND_X = 30
    DINO_SIZE_STAND_Y = 50
    DINO_POS_STAND_X = 50
    DINO_POS_STAND_Y = 250
    DINO_SIZE_DUCK_X = 50
    DINO_SIZE_DUCK_Y = 25
    DINO_POS_DUCK_X = 50
    DINO_POS_DUCK_Y = 275

    DINO_JUMP_MAX = 150

    def __init__(self):
        
        self.size = [self.DINO_SIZE_STAND_X, self.DINO_SIZE_STAND_Y]
        self.position = self.x, self.y = [self.DINO_POS_STAND_X, self.DINO_POS_STAND_Y]
        self.speed = 0
        self.score = 0
        self.alive = True
        self.ducking = False
        self.jumping = False
        self.reachedTop = False

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
        # Jump
        if self.jumping:
            self.jump()

        # Duck
        elif self.ducking:
            self.size = [self.DINO_SIZE_DUCK_X, self.DINO_SIZE_DUCK_Y]
            self.position = [self.DINO_POS_DUCK_X, self.DINO_POS_DUCK_Y]

        # Move normally
        else:
            self.size = [self.DINO_SIZE_STAND_X, self.DINO_SIZE_STAND_Y]
            self.position = [self.DINO_POS_STAND_X, self.DINO_POS_STAND_Y]

    def check_hit(self, obs):
        # Awful hit detection
        if self.check_x_hit(obs) and self.check_y_hit(obs):
            self.alive = False

    def check_x_hit(self, obs):
        # Detects if matched up in x position
        if self.position[0] <= obs.pos[0] and (self.position[0] + self.size[0] - 1) >= obs.pos[0]:
            return True
        elif self.position[0] <= (obs.pos[0] + obs.width - 1) and (self.position[0] + self.size[0] - 1) >= (obs.pos[0] + obs.width - 1):
            return True
        return False

    def check_y_hit(self, obs):
        # Detects if matched up in y position
        if self.position[1] <= obs.pos[1] and (self.position[1] + self.size[1] - 1) >= obs.pos[1]:
            return True
        elif self.position[1] <= (obs.pos[1] + obs.length - 1) and (self.position[1] + self.size[1] - 1) >= (obs.pos[1] + obs.length - 1):
            return True
        return False


    def jump(self):

        # Jump until max jump height is reached
        if self.position[1] > self.DINO_JUMP_MAX and not self.reachedTop and not self.ducking:
            self.position[1] -= 10

        # Decrease Jump going back down
        else:
            self.reachedTop = True
        
            if self.position[1] + 15 < self.DINO_POS_STAND_Y:
                self.position[1] += 15
            else:
                self.position[1] = self.DINO_POS_STAND_Y
        
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

    
    def dino_data(self, obs, speed):
        '''
        Input data the will go into neuarl network
        '''
        # Input Layer 5:
        # Speed
        # Y-Position
        # Distance to nearest Object
        # Height of nearest Object
        # Length of nearest object
        # Width of Nearest Object
        dataframe = []
        dataframe.append(self.position[1])
        dataframe.append(speed)
        dataframe.append(obs.pos[0] - self.position[0])
        dataframe.append(300 - obs.pos[1] - obs.length)
        dataframe.append(obs.length)
        dataframe.append(obs.width)

        return dataframe

class Obs:

    def __init__(self, width = 50, length = 50, pos = [700, 250]):

        self.length = length
        self.width = width
        self.pos = pos

    def move(self, speed_increase = 0):
        self.pos[0] -= (10 + speed_increase)

    def draw(self, surface):
        body = pygame.Rect(self.pos, (self.width, self.length))
        pygame.draw.rect(surface, (0, 0, 0), body)

# Constsnts for enemies
# width, length, y-height
GE = ((50, 50, 250), (25, 50, 250), (50, 25, 275), (50, 40, 260))
FGE = ((50, 25, 225), (25, 25, 250), (50, 25, 250), (50, 25, 225)) # (50, 25, 200),

class ObsList:

    def __init__(self):

        self.enemies = []
        self.speed = 10

    def add_random_enemy(self):
        self.enemies.append(Obs(25, 50, [700, 250]))

    def add_enemy(self, num):

        # Ground types
        #if num == 1:
        #    self.enemies.append(Obs(50, 50, [700, 250]))
        #elif num == 2:
        #    self.enemies.append(Obs(75, 75, [700, 225]))
        #elif num == 3:
        #    self.enemies.append(Obs(25, 75, [700, 225]))
        #elif num == 4:
        #    self.enemies.append(Obs(25, 50, [700, 250]))

        # Air enemies - can still jump
        #elif num == 5:
        #    self.enemies.append(Obs(25, 25, [700, 225]))
        if num < len(GE):
            self.enemies.append(Obs(GE[num][0], GE[num][1], [700, GE[num][2]]))
        else:
            num = len(GE) - num
            self.enemies.append(Obs(FGE[num][0], FGE[num][1], [700, FGE[num][2]]))

    def move_enemies(self, speed_increase = 0):
        for i in self.enemies:
            i.move(speed_increase)

    def remove_enemies(self):
        # Remove enemie from list if it is out of bounds
        for i in self.enemies:
            if i.pos[0] < -i.width:
                self.enemies.remove(i)

    def draw_obs(self, surface):
        # Draw each object int 
        for i in self.enemies:
            i.draw(surface)

class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.clock = None
        self.speed_modifier = 0
        self.random_spawn = 60

        # Player
        self.dino = Dinosaur()

        # Test - list of obsticalts
        self.enemy = ObsList()

        # Tick amount for score, spawn stuff
        self.tick_amt = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Dino Game")
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()

        # Add random enemey
        self.enemy.add_random_enemy()

        # Init for text
        self.score_font = pygame.font.SysFont('mono', 20)
	
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == K_DOWN:
                # Duck or cancel jump
                #print("Down!")
                self.dino.toggle_duck()
            
            if event.key == K_SPACE or event.key == K_UP:
                # Can't Jump when ducking!
                if self.dino.ducking is False:
                    #print("Jump!")
                    self.dino.jumping = True

        else:
            self.dino.ducking = False

    def on_loop(self):

        # Check current position (well, its really the size right not) of dina
        self.dino.check_positiion()
        #self.enemy.move()

        # Randomly spawn enemy
        if self.tick_amt % self.random_spawn == 0:
            
            #self.enemy.add_random_enemy()
            self.enemy.add_enemy(random.randint(0,7))

            # Change random spawn rate
            self.random_spawn += random.randint(30, 40)

        self.enemy.move_enemies(self.speed_modifier)
        self.enemy.remove_enemies()
        
        for current_enemy in self.enemy.enemies:
            self.dino.check_hit(current_enemy)

        # Print dino frame data for the nearest enemy
        for current_enemy in self.enemy.enemies:
            if current_enemy.pos[0] - self.dino.position[0] > 0:
                print(self.dino.dino_data(current_enemy, self.speed_modifier))
                break
        
        # Update player score
        if self.tick_amt % 3 == 0:
            self.dino.score += 1
            # Modify speed
            if self.dino.score % 100 == 0:
                self.speed_modifier += 1


    def on_render(self):
        # White Background
        self._display_surf.fill((255, 255, 255))

        # Draw ground
        ground = pygame.Rect(((0, 300), (self.width, 10)))
        pygame.draw.rect(self._display_surf, (128, 128, 128), ground)

        # Draw dinoasur
        self.dino.draw(self._display_surf)

        # Draw obstacles
        #self.enemy.draw(self._display_surf)
        self.enemy.draw_obs(self._display_surf)

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

        while(self._running and self.dino.alive):

            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(30)
            self.tick_amt += 1
        
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute() 