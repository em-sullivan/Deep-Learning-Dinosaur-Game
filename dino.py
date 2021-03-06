'''
Code for playing dinoasur game
'''
import pyautogui
from PIL import Image, ImageGrab, ImageOps
import time


class dino:
    '''
    Class for playing dinosaur game. This class (as a whole)
    should keep track of the parameters that will need to be passed
    to the NN, as well as contain the methods needed to control the dinoasur
    playing the game. It will use PIL to to capture the screen, and pyautogui
    to control the dino to jump or duck if needed.
    '''
    def __init__(self):
        '''
        Init stuff for the dinosuar. This should
        have where it is on screen, its current speed,
        score (probably) and stuff
        '''

        self.speed = 0
        self.score = 0

    def obstacle_distance(self):
        '''
        Calculate the distance for the next obstacle
        '''
        pass

    def action(self):
        '''
        Dinosaur peforms action
        (Jump or duck or nada)
        '''
        pass

# All of this code bellow is just an attempt to make a basic
# bot to play the game. Most of this stuff will be incorparated into
# the class above once this stuff works ok

def draw_rect(data, x_range, y_range):
	
    for i in range(x_range[0], x_range[1]):
        for j in range(y_range[0], y_range[1]):
            data[i, j] = 0

def jump():
    pyautogui.keyDown('space')
    time.sleep(.05)
    print("Jump!")
    time.sleep(.10)
    pyautogui.keyUp('space')

def check_hit(data):
    for i in range(100, 140):
        for j in range(100, 130):
            if data[i, j] < 150:
                jump()     
def main():

    #time.sleep(5)
    #pyautogui.keyDown('up')

    while True:
        #time.sleep(2)
        #pyautogui.keyDown('up')

        # Capture image of current game field
        # Convert to grayscale
        '''
		Eric's monitor = (650, 170, 1300, 350)
		John's monitor = (500, 330, 1397, 522)
		Note:
		For consistency have this image grab be:
		- left and right edge --> as close as possible to the edge of the terrain
		- top edge            --> as close as possible to top edge of HI-SCORE
		- bottom edge         --> as close as possible to bottom of Dino's feet
		'''
        image = ImageGrab.grab(bbox = (650, 170, 1300, 350)).convert('L')
        #image = ImageOps.invert(image)
        data = image.load()
        #check_hit(data)
        #print(data[70,110])
	
        # Draw rectangle on screen - little rectangle in front
        # of the dinosaur
        # Eric - 80, 90, 100, 140 - Little rectangle in front of dino
        draw_rect(data, (100, 180), (100, 120))
        #print(data[80,100])
        break
	
    image.show()

def runTest():
    print("Test playing starting...")
    time.sleep(5)
    jump()
    while True:
        image = ImageGrab.grab(bbox = (650, 170, 1300, 350)).convert('L')
        data = image.load()
        check_hit(data)

    return

if __name__ == '__main__':
    #main()
    runTest()