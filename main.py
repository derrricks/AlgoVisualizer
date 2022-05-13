from filecmp import clear_cache
import pygame
import random 
import math
pygame.init()

# class to represent screen panel needed for visualization
class Panel:
    black = 0,0,0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    blue = 0, 0, 255

    background_color = white

    greys = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)  
    ]

    # values used when scaling each of the bars 
    side_padding = 100
    top_padding = 150

    font = pygame.font.SysFont("comicsans", 20)
    large_font = pygame.font.SysFont("comicsans", 30)


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
        self.scale_height =  math.floor((self.height - self.top_padding) / (self.max_value - self.min_value)) 
        self.start_x = self.side_padding // 2 # starting x position on screen 

    
# generate list with random values between min and max 
def generate_starting_list(n, min_value, max_value):
    lst = []

    # complete loop n-times
    for _ in range(n): 
        val = random.randint(min_value, max_value)
        lst.append(val)

    return lst

# method used to draw on the panel
def draw(panel, algorithm_name, ascending):
    panel.window.fill(panel.background_color)

    title = panel.large_font.render(f"{algorithm_name} - {'Ascending' if ascending else'Descending'}", 1, panel.blue)
    panel.window.blit(title, (panel.width/2 - title.get_width()/2, 5))

    controls = panel.font.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, panel.black)
    panel.window.blit(controls, (panel.width/2 - controls.get_width()/2, 45))

    sorting = panel.font.render("I - Insertion Sort | B - Bubble Sort", 1, panel.black)
    panel.window.blit(sorting, (panel.width/2 - sorting.get_width()/2, 75))

    draw_list(panel)
    pygame.display.update()


def draw_list(panel, color_positions = {}, clear_bg = False):
    lst = panel.lst

    if clear_bg:
        clear_rect = (panel.side_padding//2, panel.top_padding, panel.width - panel.side_padding, panel.height - panel.top_padding)
        pygame.draw.rect(panel.window, panel.background_color, clear_rect)

    for i, val in enumerate(lst):
        x = panel.start_x + i * panel.scale_width
        y = panel.height - (val - panel.min_value) * panel.scale_height

        color = panel.greys[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(panel.window, color, (x, y, panel.scale_width, panel.height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(panel, ascending = True):
    lst = panel.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if(num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(panel, {j: panel.green, j + 1: panel.red}, True)
                yield True

    return lst


def insertion_sort(panel, ascending = True):
    lst = panel.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(panel, {i - 1: panel.green, i: panel.red}, True)
            yield True

    return lst

# main method
def main():
    run = True
    clock = pygame.time.Clock() # regulate how fast the program will run

    n = 50 # number of columns to sort
    min_value = 0 
    max_value = 100

    lst = generate_starting_list(n, min_value, max_value)
    panel = Panel(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60) # max number of times loop can run per second

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(panel, sorting_algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # clickiing red exit corner button
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r: # if r-key is pressed
                lst = generate_starting_list(n, min_value, max_value)
                panel.set_list(lst) 
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(panel, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"            
            elif event.key == pygame.K_q: # quit if q-key pressed
                run = False


    pygame.quit()

if __name__ == "__main__":
    main()