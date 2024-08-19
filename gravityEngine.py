"""
This is a short program that allows the user to click to place a celestial body.
The body will move according to Newton's laws of Gravitation.
This was implemented in python with the module pygame.
The time complexity of this algorithm is O(n^2) and works by cycling through each body and working out the forces affecting it, hence O(n^2)
The program does not handle a large number of bodies well - further improvements could involve adding a quadtree to approximate the gravitional effects
which could bring the program to O(nlogn) time
"""

from tkinter import CURRENT
import pygame
from random import randint
from sys import exit
from math import sqrt
from time import perf_counter

#Screen size constant
screenSize = ((1000, 800))

#Define computational constants as well as game constants
#Gravitational constant can be changed
gravitationalConstant = 20
eulerTimeStep = 0.01

#bodyList is an array of all bodies affected by the gravitational force
bodyList = []

#Define class body
class Body:
    def __init__(self, posX, posY, velX, velY, mass, bodyRadius, image):
        #Load the sprite image
        bodyImage = pygame.image.load(image)
        #Define mass, x and y postions and x and y velocities 
        #Velocities will be used to update the position of the body
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.mass = mass
        self.bodyRadius = bodyRadius
        
        #The list of previousLocations is used to render the trail of the body
        self.previousLocations = []
        #Scale the body according to the given size of the body
        self.bodyImage = pygame.transform.scale(bodyImage, (self.bodyRadius, self.bodyRadius))
        #Add the new body to the body list - this is used in calculations
        bodyList.append(self)
        
    def update(self):
        #Loop through all bodies in the list and calculate how their masses impact the movement of the body
        for otherBody in bodyList:
            resultantForceX = 0
            resultantForceY = 0

            singleForceX = 0
            singleForceY = 0

            #The if statement stops bodies from being attracted to themselves 
            #If the bodies positions are the same do not count gravitational attraction. As this stops bodies from being attracted to themselves
            if not (otherBody.posY == self.posY and otherBody.posX == self.posX):
                #The distance between the bodies squared
                rSquared = ((otherBody.posX - self.posX) ** 2) + ((otherBody.posY - self.posY) ** 2)

                #Find the direction in which the force is acting and normalise both x and y
                forceDirectionX = (otherBody.posX - self.posX) / sqrt(rSquared)
                forceDirectionY = (otherBody.posY - self.posY) / sqrt(rSquared)

                #Newton's law of universal gravitation
                singleForceMagnitude = gravitationalConstant * otherBody.mass / rSquared

                singleForceX = singleForceMagnitude * forceDirectionX
                singleForceY = singleForceMagnitude * forceDirectionY

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
        self.previousLocations.append((self.posX + (self.bodyRadius / 2), self.posY + (self.bodyRadius / 2)))

    #This code displays where the body has been in all past positions 
    def renderTrail(self):
        for location in self.previousLocations:
            pygame.draw.circle(screen, (55,55,55), location, 1)

    def renderBody(self):
        screen.blit(self.bodyImage, (self.posX, self.posY))
        
    def updateVelocity(self, accelerationX, accelerationY):
        self.velX += accelerationX * eulerTimeStep
        self.velY += accelerationY * eulerTimeStep
        
    def updatePosition(self):
        self.posX += self.velX * eulerTimeStep
        self.posY += self.velY * eulerTimeStep
        
def makeNewBody():
    mousePos = pygame.mouse.get_pos()
    Body(mousePos[0], mousePos[1], 0, 0, 400, 30, 'Object.png')

#Initialise the pygame screen and set dimensions, clock speed and title of application
pygame.init()
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption('n-body Simulation')
clock = pygame.time.Clock()

mouseDownLastFrame = False

prevCounter = perf_counter()
currentTime = perf_counter()

Body(500, 500, 0, 0, 30000, 30, 'Object.png')
Body(200, 500, 0, 20, 10, 10, 'Object.png')
Body(800, 500, 0, -20, 10, 10, 'Object.png')

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