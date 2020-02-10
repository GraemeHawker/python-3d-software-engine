import pygame
import numpy as np
import time
from primitives import Triangle, Mesh

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 460
WINDOW_TITLE = 'Spinning Cube Demo'
MAX_FRAMERATE = 0

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

def main():

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("img/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption(WINDOW_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # define a variable to control the main loop
    running = True

    # projection matrix
    fNear = 0.1
    fFar = 1000.0
    fFov = 90.0
    fFovRad = 1.0 / np.tan(np.radians(fFov) * 0.5)
    fAspectRatio = float(SCREEN_HEIGHT) / float(SCREEN_WIDTH)

    matProj = np.zeros((4,4))
    matProj[0][0] = fAspectRatio * fFovRad
    matProj[1][1] = fFovRad
    matProj[2][2] = fFar / (fFar - fNear)
    matProj[3][2] = (-fFar * fNear) / (fFar - fNear)
    matProj[2][3] = 1.0

    # create cube Mesh
    cubeMesh = Mesh([
        # SOUTH
		[0.0, 0.0, 0.0,    0.0, 1.0, 0.0,    1.0, 1.0, 0.0],
		[0.0, 0.0, 0.0,    1.0, 1.0, 0.0,    1.0, 0.0, 0.0],

		# EAST
		[1.0, 0.0, 0.0,    1.0, 1.0, 0.0,    1.0, 1.0, 1.0],
		[1.0, 0.0, 0.0,    1.0, 1.0, 1.0,    1.0, 0.0, 1.0],

		# NORTH
		[1.0, 0.0, 1.0,    1.0, 1.0, 1.0,    0.0, 1.0, 1.0],
		[1.0, 0.0, 1.0,    0.0, 1.0, 1.0,    0.0, 0.0, 1.0],

		# WEST
		[0.0, 0.0, 1.0,    0.0, 1.0, 1.0,    0.0, 1.0, 0.0],
		[0.0, 0.0, 1.0,    0.0, 1.0, 0.0,    0.0, 0.0, 0.0],

		# TOP
		[0.0, 1.0, 0.0,    0.0, 1.0, 1.0,    1.0, 1.0, 1.0],
		[0.0, 1.0, 0.0,    1.0, 1.0, 1.0,    1.0, 1.0, 0.0],

		# BOTTOM
		[1.0, 0.0, 1.0,    0.0, 0.0, 1.0,    0.0, 0.0, 0.0],
		[1.0, 0.0, 1.0,    0.0, 0.0, 0.0,    1.0, 0.0, 0.0],])

    # start timing for rotation calculations
    last_update = time.time()
    fTheta = 0.0

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        screen.fill(black)
        for tri in cubeMesh.tris:

            # get time elapsed since last update
            delta_t = time.time() - last_update
            fTheta += delta_t

            # calculate Z-rotation matrix for given time elapsed
            matRotZ = np.zeros((4,4))
            matRotZ[0][0] = np.cos(fTheta)
            matRotZ[0][1] = -1.0 * np.sin(fTheta)
            matRotZ[1][0] = np.sin(fTheta)
            matRotZ[1][1] = np.cos(fTheta)
            matRotZ[2][2] = 1.0
            matRotZ[3][3] = 1.0

            # calculate X-rotation matrix for given time elapsed
            matRotX = np.zeros((4,4))
            matRotX[0][0] = 1.0
            matRotX[1][1] = np.cos(fTheta * 0.5)
            matRotX[1][2] = -1.0 * np.sin(fTheta * 0.5)
            matRotX[2][1] = np.sin(fTheta * 0.5)
            matRotX[2][2] = np.cos(fTheta * 0.5)
            matRotX[3][3] = 1.0

            # rotate in Z axis
            triRotatedZ = tri.transform(matRotZ)
            triRotatedZX = triRotatedZ.transform(matRotX)

            # translate in z axis
            triTranslated = triRotatedZX.translate([0.0, 0.0, 3.0])

            # project from 3D --> 2D
            triProjected = triTranslated.transform(matProj)

            # scale into view
            triScaled = triProjected.scale(SCREEN_WIDTH, SCREEN_HEIGHT)

            # draw on screen
            triScaled.draw(screen, white)

        pygame.display.flip()
        last_update = time.time()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
