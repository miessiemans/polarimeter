## import all libraries for image processing

import cv2 
import numpy as np
import math
from skimage import io, color

import pygame


## set up RGBs, fonts, and texts that will be put out
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
width = 4


pygame.font.init()
large_font = pygame.font.SysFont('Objektiv Mk1', 70)
small_font = pygame.font.SysFont('Objektiv Mk1', 20)

positive_text = large_font.render("Aligned", False, GREEN)
negative_text = large_font.render("Not Aligned", False, RED)



## set up video feed and initialise pygame screen:
feed = cv2.VideoCapture(0)
screen = pygame.display.set_mode((640, 480))
pygame.init()



## write calibration function

def calibrate(img): # takes the snapshot image and returns array of the calibration coordinates
    
    ar = []

    # update screen with the snapshot image
    screen.blit(img, (0,0))
    pygame.display.flip()

    while True:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:

                ## get position of mouse when clicked and add to ar:
                # pygame uses (row, column) coordinates whereas cv2 uses (column, row) so reversed() is used 
                # to transpose the coordinates
                ar.append(list(reversed(pygame.mouse.get_pos())))
        
        if len(ar) == 2:  # if 2 positions are clicked then end function and return ar with coordinates
            return ar
        
# calibrate function outputs cv2 image on pygame screen so we need to convert it 

def generate_img(frame):
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    # change cv2 BGR to pygame RGB
    img = np.transpose(img, (1, 0, 2))  # transpose again (column, row) -> (row, column)

    return pygame.surfarray.make_surface(img)   # use pygame to turn RGB values into an object



## to avoid rogue pixels we take an average of a square around the calibration coordinate
# first we get an array of the coordinates around the calibration coordinate

def get_pixels(coordinate, span = 5):
    ar = []
    coord_x, coord_y = coordinate

    for x in range(coord_x - span, coord_x + span + 1):     # iterate over all pixels -5 and +5 away from the calibration coordinate
        for y in range(coord_y - span, coord_y + span + 1):   
            ar.append((y, x))   # add transpose (again) to the return array

    return ar


# now average out the LAB values for each

def average(img, coordinate):   # just finds the mean of each colour value
    pixels = get_pixels(coordinate)

    L = 0
    A = 0
    B = 0

    for x in pixels:
        L += img[x[0]][x[1]][0]
        A += img[x[0]][x[1]][1]
        B += img[x[0]][x[1]][2]


    div = len(pixels)   
    output = [(L / div), (A / div), (B / div)]

    return output


## make some processing functions 

# this program uses LAB colourspace as we are comparing colours from a polarimeter 
# and LAB corresponds more closely to how we perceive colour than RGB

def rgb_lab(rgb):
    return color.rgb2lab(rgb)


# returns euclidean distance between both lab values, same as distance between 3 dimensional vectors to determine "closeness"
def euclidean_distance(lab1, lab2): 
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(lab1, lab2)))


# for visual cue when delta is small we have a pointer line that gets further from 
# baseline as delta grows
def pointer_position(delta):
    y = 450 - (delta * 3)
    if y < 150:
        y = 150 # set maximum

    return y   # x stays constant




## start main code
# initial calibration

_, frame = feed.read()
image = generate_img(frame)
calib_coordinates = calibrate(image)


running = True
while running:
    screen.fill(WHITE)  # refresh frame

    _, frame = feed.read()  # look at current frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:     # if quit then stop running
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:     # if 'c' is pressed another calibration occurs
                image = generate_img(frame)
                calib_coordinates = calibrate(image)



    lab = rgb_lab(frame)    # convert rgb to lab

    glab1 = average(frame, calib_coordinates[0])    # find average LAB values that will be compared 
    glab2 = average(frame, calib_coordinates[1])    # glab -> global lab

    delta = euclidean_distance(glab1, glab2)
    
    if float(delta) < 5:    # threshold distance, but the lower the delta the closer the colours
        text = positive_text    # if less than threshold they are "Aligned"
    else:
        text = negative_text
    
    # write the delta on the screen:
    D = round(delta, 3)
    D_text = small_font.render(f"Delta = {D}", False, BLACK)


    # create bars for pointer
    pygame.draw.line(screen, BLACK, (370, 450), (370, 150), width)
    pygame.draw.line(screen, BLACK, (470, 450), (470, 150), width)
    
    pygame.draw.line(screen, BLACK, (370, 150), (470, 150), width)
    pygame.draw.line(screen, BLUE, (370, 450), (470, 450), width)


    # render pointer
    y = pointer_position(delta)
    pygame.draw.line(screen, RED, (370, y), (470, y), width)


    # render text
    screen.blit(D_text, (480, 380))
    screen.blit(text, (0,0))

    # update screen
    pygame.display.flip()

pygame.quit()
