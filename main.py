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

    # values used when scaling each of the bars 
    side_padding = 100
    top_padding = 150

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
        
        # scaling values
        self.scale_width = round((self.width - self.side_padding) / len(lst))
        self.scale_height =  round((self.height - self.top_padding) / (self.max_value - self.min_value)) 
        self.start_x = self.side_padding // 2 # starting x position on screen 

    
# generate list with random values between min and max 
def generate_starting_list(n, min_value, max_value):
    lst = []

    # complete loop n-times
    for _ in range(n): 
        val = random.randint(min_value, max_value)
        lst.append(val)

    return lst


# main method
def main():
    run = True
    clock = pygame.time.Clock() # regulate how fast the program will run

    n = 50
    min_value = 0
    max_value = 100

    lst = generate_starting_list(n, min_value, max_value)
    draw_info = Panel(800, 600, lst)

    while run:
        clock.tick(60) # max number of times loop can run per second

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # clickiing red exit corner button
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()