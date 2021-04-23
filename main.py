'''
Main function to run
'''
#import pygame
#import random
#from pygame.locals import *
#import game
#from game import Dinosaur
#from game import ObsList

from game import *
from neural_network import *
import genetic
import numpy as np

class NN_Play:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.clock = None
        self.speed_modifier = 0
        self.random_spawn = 60
        self.end = False

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

    def reset(self):
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
       
	
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:

            if event.key == K_q:
                self._running = False
                self.end = True
            '''
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
            '''
        

    def on_loop(self, nn, index):

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
        
        #for current_enemy in self.enemy.enemies:
            #self.dino.check_hit(current_enemy)

        # Print dino frame data for the nearest enemy
        for current_enemy in self.enemy.enemies:
            if current_enemy.pos[0] + current_enemy.width - self.dino.position[0] > 0:
                self.dino.check_hit(current_enemy)
                #print(nn.predict_action(index, self.dino.dino_data(current_enemy, self.speed_modifier)))

                # NN predicts which action to perform, may move this to another part, maybe the beginning of on_loop?
                self.map_action(nn.predict_action(index, self.dino.dino_data(current_enemy, self.speed_modifier)))
                #print(self.dino.dino_data(current_enemy, self.speed_modifier))
                break
        
        # Predict action

        # Update player score
        if self.tick_amt % 3 == 0:
            self.dino.score += 1
            # Modify speed
            if self.dino.score % 100 == 0:
                self.speed_modifier += 1

    def map_action(self, action_index):

        if action_index == 0:
            # Go down
            self.dino.ducking = True

        elif action_index == 1:
            # Can't Jump when ducking!
            if self.dino.ducking is False:
                #print("Jump!")
                self.dino.jumping = True

        else:
            self.dino.ducking = False

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
        #pygame.quit()
        self.reset

    def on_execute(self, nn, index):

        if self.on_init() == False:
            self._running = False

        while(self._running and self.dino.alive):

            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop(nn, index)
            self.on_render()
            self.clock.tick(30)
            self.tick_amt += 1
        
        nn.fitness[index] = self.dino.score
        self.on_cleanup()

if __name__ == "__main__":

    # to track number of generations
    generations = 0

    save = False
    load = True
    save_location = "Saved_Models/testa"
    load_location = "Saved_Models/testa"

    population_size = 50
    nn = dino_pop(population_size)

    if load is True:
        nn.load_pop(load_location)

    while generations < 250:
        for current in range(population_size):
            game = NN_Play()
            game.on_execute(nn, current)
            if game.end is True:
                break
       
       # if user presses 'q' to quit
        if game.end is True:
            if save is True:
                nn.save_pop(save_location)
            break
        
        # Perform genetic update, reset fitness
        print("Highest Score: " + str(max(nn.fitness)))
        print("Average Score: " + str(np.mean(nn.fitness)))
        print("Number of generations: " + str(generations))
        genetic.genetic_updates(nn.dino_networks, nn.fitness, nn.population_size)
        print(nn.fitness)
        nn.reset_fitness()

        generations += 1

    # if max generations is hit
    if save == True:
        nn.save_pop(save_location)