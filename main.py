from pathlib import WindowsPath
import pygame
import random 
pygame.init()

# class to represent screen panel needed for visualization
class Panel:
    black = 0,0,0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    grey = 128, 128, 128
    background_color = white


    def __init__(self, width, height, lst): # class constructor
        self.width = width
        self.height = height
        
        self.window = pygame.display.set_mode((width, height)) # create game window
        pygame.display.set_caption("Algorithm Sorting Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)


    