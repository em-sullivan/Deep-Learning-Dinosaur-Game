'''
Code that contains the neural network,
which will be used to play the snake game
'''
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Activation

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


    def predict_action(self, model_index, input_data):
        '''
        Predicts what action to take when playing the game.
        '''
        pass

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
    print(dinos.dino_networks[49].get_weights())