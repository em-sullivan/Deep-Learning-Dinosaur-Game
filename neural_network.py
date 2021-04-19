'''
Code that contains the neural network,
which will be used to play the snake game
'''
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Activation
import numpy as np

class dino_pop:

    def __init__(self, popSize = 10):

        self.population_size = popSize
        self.dino_networks = []
        self.fitness = []

        for i in range(popSize):
            self.dino_networks.append(self.create_network())
            self.fitness.append(0)


    def create_network(self):
        '''
        Create a DINO neural network,
        which will play the dinosaur game
        '''

        model = Sequential()

        # Input Layer 5:
        # Speed
        # Y-Position
        # Distance to nearest Object
        # Height of nearest Object
        # Length of nearest object
        # Width of Nearest Object
        model.add(Dense(10, input_dim = 6, activation = 'relu'))
        
        # Hidden Layer
        model.add(Dense(16, activation = 'relu'))

        # Output layer: Sigmoid
        # Run
        # Jump
        # Go Down (Ends jump early or ducks)
        model.add(Dense(4, activation = 'sigmoid'))

        model.compile(loss = "mse", optimizer = 'adam')
        return model

    def save_pop(self, save_location):

        for i in range(self.population_size):
            self.dino_networks[i].save_weights(save_location + str(i) + ".keras")
        
        print("Pool Saved")

    def load_pop(self, load_location):

        for i in range(self.population_size):
            self.dino_networks[i].load_weights(load_location + str(i) + ".keras")

    def predict_action(self, model_index, input_data):
        '''
        Predicts what action to take when playing the game.
        '''
        input = np.atleast_2d(input_data)
        output = self.dino_networks[model_index].predict(input, 1)
        return output.argmax()

    def reset_fitness(self):
        '''
        Reset fintess scores for all networks
        in a population
        '''       
        for i in range(self.population_size):
            self.fitness[i] = 0

if __name__ == "__main__":
    population_size = 50

    dinos = dino_pop(50)
    dinos.reset_fitness()
    for i in range(population_size):
        print(dinos.fitness[i])

    # Print weights of a neural network, I want to make sure it works
    #print(dinos.dino_networks[49].get_weights())
    # Predict action
    print(dinos.predict_action(0, [275, 0, 40, 250, 50, 50]))