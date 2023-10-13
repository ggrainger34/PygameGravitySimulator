"""
This is a short program that allows the user to click to place a celestial body.
The body will move according to Newton's laws of Gravitation.
This was implemented in python with the module pygame
The time complexity of this algorithm is O(n^2) and works by cycling through each body and working out the impact each other body has on it, hence O(n^2)
The program does not handle a large number of bodies well - further improvements could involve adding a quadtree to approximate the gravitional effects
which could bring the program to O(nlogn) time
"""

from tkinter import CURRENT
import pygame
from random import randint
from sys import exit
import math

#Define computational constants as well as game constants
screenSize = ((1000, 800))
gravitationalConstant = 40
physicsTimeStep = 0.05
#bodyList is an array of all bodies affected by the gravitational force
bodyList = []

#Define class body
class Body:
    def __init__(self, pos_x, pos_y, vel_x, vel_y, mass, image):
        #Load the sprite image
        bodyImage = pygame.image.load(image)
        #Define mass, x and y postions and x and y velocities 
        #Velocities will be used to update the position of the body
        self.mass = mass
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.bodyRadius = (math.sqrt(self.mass), math.sqrt(self.mass))
        self.centreOfMass_x = self.pos_x + (self.bodyRadius[0] / 2)
        self.centreOfMass_y = self.pos_y + (self.bodyRadius[1] / 2)
        self.previousLocations = []
        #Scale the body according to mass (for the purposes of simulation, objects with larger masses will be larger)
        self.bodyImage = pygame.transform.scale(bodyImage, self.bodyRadius)
        #Add the new body to the body list
        bodyList.append(self)
        
    def update(self):
        #Loop through all bodies in the list and calculate how their masses impact the movement of the body
        #This particular algorithm is O(n^2) when calculating all bodies and is in dire need of improvement but works for a low number of bodies
        for otherBody in bodyList:
            #The if statement stops bodies from being attracted to themselves 
            #If the bodies positions are the same do not count gravitational attraction. If this is not included it results
            #In a divide by zero error
            if otherBody != self and otherBody.pos_y != self.pos_y and otherBody.pos_x != self.pos_x:
                rSquared = ((otherBody.pos_x - self.pos_x) ** 2) + ((otherBody.pos_y - self.pos_y) ** 2)
                self.centreOfMass_x = self.pos_x + (self.bodyRadius[0] / 2)
                self.centreOfMass_y = self.pos_y + (self.bodyRadius[1] / 2)
                self.y_normalised = (otherBody.centreOfMass_y - self.centreOfMass_y) / (math.sqrt(rSquared))
                self.x_normalised = (otherBody.centreOfMass_x - self.centreOfMass_x) / (math.sqrt(rSquared))
                self.acceleration = (gravitationalConstant * otherBody.mass) / rSquared
                #Update position and velocity after calculating the desired acceleration
                self.updateVelocity()
                self.updatePosition()
        #Update the screen
        self.renderTrail()
        screen.blit(self.bodyImage, (self.pos_x, self.pos_y))
        self.previousLocations.append((self.centreOfMass_x, self.centreOfMass_y))

    #This code displays where the body has been in all past positions 
    def renderTrail(self):
        for location in self.previousLocations:
            pygame.draw.circle(screen, (55,55,55), location, 1)
        
    def updateVelocity(self):
        self.vel_x += self.acceleration * physicsTimeStep * self.x_normalised
        self.vel_y += self.acceleration * physicsTimeStep * self.y_normalised
        
    def updatePosition(self):
        self.pos_x += (self.vel_x * physicsTimeStep)
        self.pos_y += (self.vel_y * physicsTimeStep)
        
def makeNewBody():
    mousePos = pygame.mouse.get_pos()
    Body(mousePos[0],mousePos[1], 0, 0, 400, 'assets/Object.png')

#Initialise the pygame screen and set dimensions, clock speed and title of application
pygame.init()
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption('2-body Simulation')
clock = pygame.time.Clock()

#Keep running the simulation until the user decides to quit
mouseDownLastFrame = False

while True:
    currentMouse = False
    for event in pygame.event.get():
        number = 0
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            currentMouse = True
            
    if currentMouse and not mouseDownLastFrame:
        makeNewBody()
    #Calculate the new positions of the bodies
    for body in bodyList:
        body.update()
    #Update screen
    pygame.display.update()
    #Clear screen
    screen.fill((0,0,0))
    clock.tick(60)
    mouseDownLastFrame = currentMouse
