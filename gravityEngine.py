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
gravitationalConstant = 1
eulerTimeStep = 0.01

#bodyList is an array of all bodies affected by the gravitational force
bodyList = []

#Define class body
class Body:
    def __init__(self, pos_x, pos_y, vel_x, vel_y, mass, bodyRadius, image):
        #Load the sprite image
        bodyImage = pygame.image.load(image)
        #Define mass, x and y postions and x and y velocities 
        #Velocities will be used to update the position of the body
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.bodyRadius = bodyRadius

        #Body centre, from where all calculations are carried out
        self.bodyCentreX = self.pos_x + (self.bodyRadius / 2)
        self.bodyCentreY = self.pos_y + (self.bodyRadius / 2)
        
        #The list of previousLocations is used to render the trail of the body
        self.previousLocations = []
        #Scale the body according to the given size of the body
        self.bodyImage = pygame.transform.scale(bodyImage, (self.bodyRadius, self.bodyRadius))
        #Add the new body to the body list - this is used in calculations
        bodyList.append(self)
        
    def update(self):
        self.bodyCentreX = self.pos_x + (self.bodyRadius / 2)
        self.bodyCentreY = self.pos_y + (self.bodyRadius / 2)

        #Loop through all bodies in the list and calculate how their masses impact the movement of the body
        for otherBody in bodyList:
            resultantForceX = 0
            resultantForceY = 0

            singleForceX = 0
            singleForceY = 0

            #The if statement stops bodies from being attracted to themselves 
            #If the bodies positions are the same do not count gravitational attraction. As this stops bodies from being attracted to themselves
            if not (otherBody.pos_y == self.pos_y and otherBody.pos_x == self.pos_x):
                #The distance between the bodies squared
                rSquared = ((otherBody.pos_x - self.pos_x) ** 2) + ((otherBody.pos_y - self.pos_y) ** 2)

                #Find the direction in which the force is acting and normalise both x and y
                forceDirectionX = (otherBody.bodyCentreX - self.bodyCentreX) / sqrt(rSquared)
                forceDirectionY = (otherBody.bodyCentreY - self.bodyCentreY) / sqrt(rSquared)

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

            #Update position and velocity after calculating the desired acceleration
            self.updateVelocity(accelerationX, accelerationY)
            self.updatePosition()

        #Update the screen
        self.renderTrail()
        self.renderBody()
        self.previousLocations.append((self.bodyCentreX, self.bodyCentreY))

    #This code displays where the body has been in all past positions 
    def renderTrail(self):
        for location in self.previousLocations:
            pygame.draw.circle(screen, (55,55,55), location, 1)

    def renderBody(self):
        screen.blit(self.bodyImage, (self.pos_x, self.pos_y))
        
    def updateVelocity(self, accelerationX, accelerationY):
        self.vel_x += accelerationX
        self.vel_y += accelerationY
        
    def updatePosition(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        #print(self.pos_x, self.pos_y)
        
def makeNewBody():
    mousePos = pygame.mouse.get_pos()
    Body(mousePos[0],mousePos[1], 0, 0, 400, 30, 'Object.png')

#Initialise the pygame screen and set dimensions, clock speed and title of application
pygame.init()
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption('2-body Simulation')
clock = pygame.time.Clock()

#Keep running the simulation until the user decides to quit
mouseDownLastFrame = False

prevCounter = perf_counter()
currentTime = perf_counter()

while True:
    print(currentTime)

    currentMouse = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            currentMouse = True

    if currentMouse and not mouseDownLastFrame:
        makeNewBody()
            
    if currentTime - prevCounter > eulerTimeStep:
        print(currentTime - prevCounter)
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