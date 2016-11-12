import pygame, sys, math
from pygame.locals import *

#gravity constant used here as kind of g constant
gConstant=5

pygame.init()

class vector():
    def __init__(self, coordinate):
        self.x=float(coordinate[0])
        self.y=float(coordinate[1])

    def __eq__(self, other):
        if isinstance(other, vector):
            return (self.x==other.x) and (self.y==other.y)
        else: return NotImplemented

    def __ne__(self, other):
        if isinstance(other, vector):
            return (self.x!=other.x) or (self.y!=other.y)
        else: return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def valueVec(self):
        return (self.x, self.y)

    # return angle between positive x axe and vector in counter-clockwise direction

    def getAngle(self):
        if self.x>=0 and self.y>=0:
            return -math.asin(unitVec(self).y)
        if self.x<0 and self.y>=0:
            return -math.acos(unitVec(self).x)
        if self.x<0 and self.y<0:
            return math.acos(unitVec(self).x)
        if self.x>=0 and self.y<0:
            return -math.asin(unitVec(self).y)        

#defines sum of two vectors

def vecSum(vec1, vec2):
    return vector((vec1.x+vec2.x, vec1.y+vec2.y))

#defines the difference between two vectors
#subtract the second vector from the first
def vecDif(vec1, vec2):
    return vector((vec1.x-vec2.x, vec1.y-vec2.y))

#defines mutiplication of vector on scalar

def multSc(scalar, vec):
    return vector((float(scalar)*vec.x, float(scalar)*vec.y))

#defines vector magnitude
def vecMag(vec):
    return math.sqrt(vec.x**2+vec.y**2)

#function to get unit vector of a given vector
def unitVec(vec):
    return multSc(1.0/vecMag(vec), vec)

class gravityField():
    def __init__(self, planets):
        self.planets=planets     
                
    def getField(self, position):
        point=position
        gravity=vector((0,0))
        for p in self.planets.sprites():
            distance=vecMag(vecDif(p.position, point))
            #magnitude of gravitational force for one unit of mass
            if distance>p.mass:
                magGravity=gConstant*p.mass/(distance**2)
                #calculate vector of gravity force for one unit of mass
                gravity=vecSum(gravity, multSc(magGravity, unitVec(vecDif(p.position, point))))
            else:
                magGravity=0
                gravity=vecSum(gravity, vector((0, 0)))
        return gravity
