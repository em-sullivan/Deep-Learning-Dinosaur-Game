'''
Code for playing dinoasur game
'''
import pyautogui
from PIL import Image, ImageGrab
import time

def main():

	# Testing pyautogui: just jumps every 2 sec
	while True:
		time.sleep(2)
		pyautogui.keyDown('up')

if __name__ == '__main__':
	main()