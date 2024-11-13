"""
Gravity Simulator - ZiggyDEV

Small program to simulate gravity under Newton's laws of Gravitation using Euler's method
This was implemented in python with the module pygame.
The time complexity of this algorithm is O(n^2) and works by cycling through each body and working out the forces affecting it
The program is fairly unoptimised - further improvements could involve adding a quadtree or moving to a faster language
"""

import pygame
from sys import exit
from math import sqrt
from time import perf_counter
from colorsys import hsv_to_rgb

#Screen size constant
screenSize = ((1100, 1100))

#Define computational constants as well as game constants
#Gravitational constant is arbitrary
gravitationalConstant = 20
eulerTimeStep = 0.01

#bodyList is an array of all bodies affected by the gravitational force
bodyList = []

#Define class body
class Body:
    def __init__(self, posX, posY, velX, velY, mass, bodyDiameter):
        #Define mass, x and y postions and x and y velocities 
        #Velocities will be used to update the position of the body
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.mass = mass
        self.bodyDiameter = bodyDiameter
        self.bodyRadius = bodyDiameter / 2
        
        #The list of previousLocations is used to render the trail of the body
        self.previousLocations = []
        #Add the new body to the body list - this is used in calculations
        bodyList.append(self)
        
    def update(self):
        resultantForceX = 0
        resultantForceY = 0

        #Loop through all bodies in the list and calculate how 
        #their masses impact the movement of the body
        for otherBody in bodyList:
            singleForceX = 0
            singleForceY = 0

            #The if statement stops bodies from being attracted to themselves 
            #If the bodies positions are the same do not count gravitational attraction.
            #This stops bodies from being attracted to themselves
            if otherBody != self:
                #The distance between the bodies squared
                rSquared = ((otherBody.posX - self.posX) ** 2) + ((otherBody.posY - self.posY) ** 2)

                #Find the direction in which the force is acting and normalise both x and y
                forceNormalisedX = (otherBody.posX - self.posX) / sqrt(rSquared)
                forceNormalisedY = (otherBody.posY - self.posY) / sqrt(rSquared)

                #Newton's law of universal gravitation
                singleForceMagnitude = gravitationalConstant * otherBody.mass / rSquared

                singleForceX = singleForceMagnitude * forceNormalisedX
                singleForceY = singleForceMagnitude * forceNormalisedY

            #Add the forces resulting from all seperate bodies to the resultant force
            resultantForceX += singleForceX
            resultantForceY += singleForceY

        #As F=m_1a and F=G*m_1*m_2 / r^2. We can cut m_1 from the equation. Hence F=a
        accelerationX = resultantForceX
        accelerationY = resultantForceY

        #Update position and velocity after calculating acceleration
        self.updateVelocity(accelerationX, accelerationY)
        self.updatePosition()

        #Update the screen
        self.renderTrail()
        self.renderBody()

        #Add previous locations, this is used for creating a trail
        self.previousLocations.append([self.posX, self.posY, perf_counter()])

    #This code displays where the body has been in all past positions 
    def renderTrail(self):
        for location in self.previousLocations:
            timeSinceCreation = currentTime - location[2]

            #Changes colours as time continues. This is by changing the saturation
            #in the HSV colour space and converting back to RGB
            if timeSinceCreation < 20:
                rgb = hsv_to_rgb(timeSinceCreation/ 36, 1.0, 1.0)
                rgb = tuple([i * 255 for i in rgb])
                pygame.draw.circle(screen, rgb, (location[0], location[1]), 1)

            #Change the values in HSV colour space to make the trail fade to black
            elif 20 < timeSinceCreation and timeSinceCreation < 35:
                decayedValue = float(1 - ((timeSinceCreation - 20) / 35))
                rgb = hsv_to_rgb(20/36, 1.0, decayedValue)
                rgb = tuple([i * 255 for i in rgb])
                pygame.draw.circle(screen, rgb, (location[0], location[1]), 1)

    def renderBody(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.posX, self.posY), self.bodyRadius)
        
    def updateVelocity(self, accelerationX, accelerationY):
        self.velX += accelerationX * eulerTimeStep
        self.velY += accelerationY * eulerTimeStep
        
    def updatePosition(self):
        self.posX += self.velX * eulerTimeStep
        self.posY += self.velY * eulerTimeStep

#This was for testing but can now be cut       
def makeNewBody():
    mousePos = pygame.mouse.get_pos()
    Body(mousePos[0], mousePos[1], 0, 0, 400, 30)

#Initialise the pygame screen and set dimensions, clock speed and title of application
pygame.init()
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption('N-Body Simulation')
clock = pygame.time.Clock()

mouseDownLastFrame = False

prevCounter = perf_counter()
currentTime = perf_counter()

Body(100, 550, 0, -60, 600000, 20)
Body(1000, 550, 0, 60, 600000, 20)

#Keep running the simulation until the user decides to quit
while True:
    currentMouse = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            currentMouse = True

    if currentMouse and not mouseDownLastFrame:
        makeNewBody()
            
    if (currentTime - prevCounter) > eulerTimeStep:
        #Clear screen
        screen.fill((0,0,0))
            
        #Calculate the new positions of the bodies
        for body in bodyList:
            body.update()

        #Update screen
        pygame.display.update()

        prevCounter = perf_counter()

    currentTime = perf_counter()
    mouseDownLastFrame = currentMouse
