import pygame, sys, math
from pygame.locals import *

# set color constants
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)


FPS = 20
WINDOWWIDTH = 800 # size of window width in pixels
WINDOWHEIGHT = 600 # size of window height in pixels

cellWidth=WINDOWWIDTH/30
cellHeight=WINDOWHEIGHT/20

#time constant
deltaT=1

#ship engine power
engine=0.2

#ship's rotational inertia momentum
rotIner=0.05

#ratio to convert radians to degrees
radDegRatio=180/math.pi

#gravity constant used here as kind of g constant
gConstant=5

# display settings initiation
global FPSCLOCK, DISPLAYSURF
pygame.init()
FPSCLOCK = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)
DISPLAYSURF = pygame.display.set_mode ((WINDOWWIDTH, WINDOWHEIGHT))

#download images
playerImg= pygame.image.load('rocket.png').convert_alpha()
rightEngineImg= pygame.image.load('rightEngine.png').convert_alpha()
leftEngineImg= pygame.image.load('leftEngine.png').convert_alpha()
rightShuntingEngineImg= pygame.image.load('rightShuntingEngine.png').convert_alpha()
leftShuntingEngineImg= pygame.image.load('leftShuntingEngine.png').convert_alpha()

class vector():
    def __init__(self, coordinate):
        self.x=float(coordinate[0])
        self.y=float(coordinate[1])

    def valueVec(self):
        return (self.x, self.y)

#defines sum of two vectors

def vecSum(vec1, vec2):
    return vector((vec1.x+vec2.x, vec1.y+vec2.y))

#defines mutiplication of vector on scalar

def multSc(scalar, vec):
    return vector((float(scalar)*vec.x, float(scalar)*vec.y))

#defines vector magnitude
def vecMag(vec):
    return math.sqrt(math.pow(vec.x, 2)+math.pow(vec.y, 2))

class battleShip(pygame.sprite.Sprite):
    def __init__(self, position=vector((0,0))): #take position as a vector in input
        pygame.sprite.Sprite.__init__(self)
        # defines initial position and speed characterictics of the battle ship
        self.position=position
        self.speed=vector((0, 0))
        self.acc=vector((0, 0))

        # defines initial rotation characteristics of player's ship
        # all angular measures are in radians
        self.angle=float(0) #angle processed as in radians
        self.rotation=float(0)
        self.rotationAcc=float(0)
        self.image=pygame.image.load('rocket.png').convert_alpha()

    def update(self, force, speedDelta, rotationDelta):
        #update decartes position
        # first update position, then - speed and finally - acceleration
        self.position=vecSum(self.position,vecSum(multSc(deltaT, self.speed), multSc(math.pow(deltaT, 2)/2, self.acc)))
        self.speed=vecSum(self.speed, vecSum(speedDelta, multSc(deltaT,self.acc)))
        self.acc=force
                
        #update rotation
        # first update angle, then rotation
        self.angle=self.angle+deltaT*self.rotation
        self.rotation=self.rotation+rotationDelta

    def kill(self):
        pass

# define planet class as sprite
class planet(pygame.sprite.Sprite):
    def __init__(self, mass, color, position): #position defines center of the planet and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        self.mass=mass #mass of the planet define gravity magnitude and radius
        self.color=color #color just for visualization
        self.position=position #position of the planet on screen
        self.surf=pygame.Surface((2*mass, 2*mass)) #surface of the planet
        pygame.draw.circle(self.surf, color, (mass,mass), mass)#draw a planet on planets' surface in center of the surface
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-mass, position.y-mass, 2*mass, 2*mass) # mass is subtracted use use position as a center

          
    

def main():

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.set_colorkey(WHITE)
    pygame.display.update()

    #set player's ship
    playerShip = battleShip(vector((400, 300)))

    #set planetary system
    planetarySystem=pygame.sprite.Group()
    mars = planet(30, RED, vector((100, 100))) 
    venus = planet (20, BLUE, vector((400, 200)))
    planetarySystem.add(mars)
    planetarySystem.add(venus)
    
    while True:
        DISPLAYSURF.fill(WHITE)
        deltaSpeed=vector((0, 0))
        deltaRot=0.0
        gravity=vector((0,0))
        playerSurf = pygame.Surface((10, 20))
        playerSurf.blit(playerShip.image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            elif event.type == KEYDOWN:
                if event.key==K_RIGHT:#if right arrow pressed -
                    deltaSpeed=vecSum(deltaSpeed, vector((engine*math.cos(playerShip.angle), -engine*math.sin(playerShip.angle))))#right engine works and ship moves forward 
                    deltaRot=deltaRot+engine*rotIner#and slightly rotates counter-clockwise
                    playerSurf.blit(rightEngineImg, (0, 0))
                    
                elif event.key==K_LEFT:#if left arrow pressed -
                    deltaSpeed=vecSum(deltaSpeed, vector((engine*math.cos(playerShip.angle), -engine*math.sin(playerShip.angle))))#left engine works and ship moves forward
                    deltaRot=deltaRot-engine*rotIner#and slightly rotates clockwise
                    playerSurf.blit(leftEngineImg, (0, 0))

                elif event.key==K_a:#if 'a' key pressed -
                    deltaRot=deltaRot-engine*rotIner# left shunting engine is on and ship slightly rotates clockwise
                    playerSurf.blit(leftShuntingEngineImg, (0, 0))

                elif event.key==K_s:#if 's' key pressed -
                    deltaRot=deltaRot+engine*rotIner# right shunting engine is on and ship slightly rotates counter-clockwise
                    playerSurf.blit(rightShuntingEngineImg, (0, 0))
        
        for i in planetarySystem.sprites(): #here i is iterable planet
            planetVec=i.position
            gravityVec=vector(((planetVec.x-playerShip.position.x), (planetVec.y-playerShip.position.y))) #define vector connecting planet and player's ship
            distance=vecMag(gravityVec)
            iGravityX=i.mass*gConstant*math.pow(distance, -3)*gravityVec.x #calculate x coordinate of planet i gravity
            iGravityY=i.mass*gConstant*math.pow(distance, -3)*gravityVec.y #calculate y coordinate of planet i gravity
            gravity=vecSum(gravity, vector((iGravityX, iGravityY)))            
        
        playerShip.update(gravity, deltaSpeed, deltaRot)

        rotPlayerSurf = pygame.transform.rotate(playerSurf, playerShip.angle*radDegRatio-90)
        rotPlayerSurf.set_colorkey(BLACK)


        #check for collision with planet
        #for planet in planetarySystem:
        #    if pygame.sprite.collide_mask(rotPlayerSurf, planet.surf):
        #        playerShip.kill()
        #        print 'killed'

              
        textAngle=myfont.render("Angle %f" %playerShip.angle, 1, RED) # text of current angle
        textAcc=myfont.render("Acceleration %f, %f" %(playerShip.acc.x, playerShip.acc.y), 1, RED) # text of current acceleration
        textSpeed=myfont.render("Speed %f, %f" %(playerShip.speed.x, playerShip.speed.y), 1, RED) #text of current speed
        textPosition=myfont.render("Position %f, %f" %(playerShip.position.x, playerShip.position.y), 1, RED) #text of current position
                
        planetarySystem.draw(DISPLAYSURF)
        DISPLAYSURF.blit(rotPlayerSurf, (playerShip.position.x, playerShip.position.y))
        DISPLAYSURF.blit(textAngle, (100, 100))
        DISPLAYSURF.blit(textAcc, (100, 120))
        DISPLAYSURF.blit(textSpeed, (100, 140))
        DISPLAYSURF.blit(textPosition, (100, 160))
        
               
        pygame.display.update()
        FPSCLOCK.tick(FPS)

       
    '''#module to check battleShip works
    print vector.valueVec(playerShip.position)

    while True:
         print vector.valueVec(playerShip.position)
         print vector.valueVec(playerShip.speed)
         print vector.valueVec(playerShip.angle)
         print vector.valueVec(playerShip.rotation)
         playerShip.update(vector((1,2)), vector((0,0)), vector((1, 2)))
         br=raw_input("break?")
         if br=='y':
             break'''
        
    

    """DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.set_colorkey(WHITE)
    pygame.display.update()
    
 
    while True:

       
       DISPLAYSURF.fill(WHITE) 
                   
       pygame.display.update()
       FPSCLOCK.tick(FPS)"""
    
    '''#module to check vector works
    x1=input("X1 value of vector1 ")
    y1=input("Y1 value of vector1 ")
    sc=input("give a scalar ")
    x2=input("X2 value of vector2 ")
    y2=input("Y2 value of vector2 ")
    vec1=vector((x1, y1))
    vec2=vector((x2, y2))
    print 'Sum of vectors is ', vector.valueVec(vecSum(vec1, vec2))
    print 'Multiply vector 1 over scalar is ', vector.valueVec(multSc(sc, vec1))'''

        

if __name__== '__main__':
    main()
