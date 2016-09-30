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


FPS = 30
WINDOWWIDTH = 800 # size of window width in pixels
WINDOWHEIGHT = 600 # size of window height in pixels

cellWidth=WINDOWWIDTH/30
cellHeight=WINDOWHEIGHT/20

#time constant
deltaT=1

#ship engine power
engine=0.2

#ship's rotational inertia momentum
rotIner=0.11

#ratio to convert radians to degrees
radDegRatio=180/math.pi

#gravity constant used here as kind of g constant
gConstant=5

#side of square of the ship
shipHeight = 20
shipWidth = 10

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

    def __eq__(self, other):
        if isinstance(other, vector):
            return (self.x==other.x) and (self.y==other.y)
        else: return NotImplemented

    def __ne__(self, other):
        if isinstance(other, vector):
            return (self.x!=other.x) or (self.y!=other.y)
        else: return NotImplemented

    def valueVec(self):
        return (self.x, self.y)

#defines sum of two vectors

def vecSum(vec1, vec2):
    return vector((vec1.x+vec2.x, vec1.y+vec2.y))

#defines the difference between two vectors
#subtract the second vector for the first
def vecDif(vec1, vec2):
    return vector((vec1.x-vec2.x, vec1.y-vec2.y))

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
        # intitial rotation
        self.Surf = pygame.Surface((shipWidth, shipHeight))
        self.Surf.blit(playerImg, (0, 0))
        self.rotSurf = pygame.transform.rotate(self.Surf, self.angle*radDegRatio-90)
        self.rotSurf.set_colorkey(BLACK)        
        
        self.image=self.rotSurf
        self.rect=pygame.Rect(self.position.x-shipHeight/2, self.position.y-shipHeight/2, shipHeight, shipHeight)
        self.mask=pygame.mask.from_surface(self.Surf) #create mask for collision

    def update(self, force, speedDelta, rotationDelta, liveState):
        #update decartes position
        # first update position, then - speed and finally - acceleration
        self.position=vecSum(self.position,vecSum(multSc(deltaT, self.speed), multSc(math.pow(deltaT, 2)/2, force)))
        self.speed=vecSum(self.speed, vecSum(speedDelta, multSc(deltaT,force)))
        self.acc=force
                
        #update rotation
        # first update angle, then rotation
        self.angle=self.angle+deltaT*self.rotation
        self.rotation=self.rotation+rotationDelta

        #rotate ship

        self.rotSurf = pygame.transform.rotate(self.Surf, self.angle*radDegRatio-90)
        self.rotSurf.set_colorkey(BLACK)#?? delete this line?
        
        self.image=self.rotSurf
        self.rect=pygame.Rect(self.position.x-shipHeight/2, self.position.y-shipHeight/2, shipHeight, shipHeight)
        self.mask=pygame.mask.from_surface(self.rotSurf) #create mask for collision

        #check whether the ship is collided
        if liveState==False: self.kill()

    def engineFlames(self, leftEngine, leftShuntingEngine, rightShuntingEngine, rightEngine):
        # function should go before update method
        # function is to add flames to ship image
        self.Surf = pygame.Surface((shipWidth, shipHeight))
        self.Surf.blit(playerImg, (0, 0))
        if leftEngine==True: self.Surf.blit(leftEngineImg, (0, 0))
        if leftShuntingEngine==True: self.Surf.blit(leftShuntingEngineImg, (0, 0))
        if rightShuntingEngine==True: self.Surf.blit(rightShuntingEngineImg, (0, 0))
        if rightEngine==True: self.Surf.blit(rightEngineImg, (0, 0))

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        #?? here should call for explosion animation

#function to calculate trajectory with given position, speed and acceleration, planetary system
def calcTrajectory(position, velocity, planetarySystem, finish):
    traj=[]
    totalForce=vector((0, 0))
    endOfTraj=False
    
    while endOfTraj==False:
        totalForce=vector((0, 0))
        traj.append(position)
        #define sum of forces
        for i in planetarySystem: #here i is iterable planet
            planetVec=i.position
            #?? below need to use vector differnece function
            gravityVec=vector(((planetVec.x-position.x), (planetVec.y-position.y))) #define vector connecting planet and player's ship
            distance=vecMag(gravityVec)
            iGravityX=i.mass*gConstant*math.pow(distance, -3)*gravityVec.x #calculate x coordinate of planet i gravity
            iGravityY=i.mass*gConstant*math.pow(distance, -3)*gravityVec.y #calculate y coordinate of planet i gravity
            totalForce=vecSum(totalForce, vector((iGravityX, iGravityY)))
        #define new position and speed
        position=vecSum(position,vecSum(multSc(deltaT, velocity), multSc(math.pow(deltaT, 2)/2, totalForce)))
        velocity=vecSum(velocity, multSc(deltaT,totalForce))
        
        

        #check end of trajectory
        if position.x>=800 or position.y>=600 or position.x<=0 or position.y<=0: endOfTraj=True
        #check for crash with the plant
        for i in planetarySystem.sprites(): #here i is iterable planet
            planetVec=i.position
            if vecMag(vecDif(position, planetVec))<=i.mass: endOfTraj=True

        #check for trjectory points to end
        for i in finish.sprites(): #here i is iterable finish
            if vecMag(vecDif(position, i.position))<=i.mass: endOfTraj=True

    return traj

        
        

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
        self.rect = pygame.Rect(position.x-mass, position.y-mass, 2*mass, 2*mass) # mass is subtracted use position as a center

class asteroid(pygame.sprite.Sprite):
    def __init__(self, position, speed): #position defines center of the planet and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        # set position and speed of the asteroid
        self.position=position
        self.speed=speed

        #set initial image of the asteroid
        self.surf=pygame.Surface((10, 10)) 
        pygame.draw.circle(self.surf, GRAY, (5,5), 5)
        self.surf.set_colorkey(BLACK) 
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-5, position.y-5, 10, 10)

    def update(self, force, liveState):
        #update decartes position
        # first update position, then - speed 
        self.position=vecSum(self.position,vecSum(multSc(deltaT, self.speed), multSc(math.pow(deltaT, 2)/2, force)))
        self.speed=vecSum(self.speed, multSc(deltaT,force))        
                
        #update image
        self.rect=pygame.Rect(self.position.x-5, self.position.y-5, 10, 10)

        #check whether the ship is collided
        if liveState==False: self.kill()

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        #?? here should call for explosion animation
        
def deathSituation(ships):
    DISPLAYSURF.blit(myfont.render("Killed!!!", 1, RED), (100, 180)) #killed situation
    DISPLAYSURF.blit(myfont.render("continue? Y/N", 1, RED), (100, 200)) #continue or not?
    print('dead')
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key==K_y:
                playerShip = battleShip(start)
                playerIsAlive=True
                ships.add(playerShip)
                DISPLAYSURF.fill(WHITE)
                deltaSpeed=vector((0, 0))
                deltaRot=0.0
                gravity=vector((0,0))
                leftEngine=False
                rightEngine=False
                leftShuntingEngine=False
                rightShuntingEngine=False
            elif event.key==K_n:
                pygame.quit()
                sys.exit()

def finishSituation(ships):
    DISPLAYSURF.blit(myfont.render("Finish!!!", 1, GREEN), (100, 180)) #finish situation
    DISPLAYSURF.blit(myfont.render("continue? Y/N", 1, RED), (100, 200)) #continue or not?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key==K_y:
                playerShip = battleShip(start)
                playerIsAlive=True
                ships.add(playerShip)
                DISPLAYSURF.fill(WHITE)
                deltaSpeed=vector((0, 0))
                deltaRot=0.0
                gravity=vector((0,0))
                leftEngine=False
                rightEngine=False
                leftShuntingEngine=False
                rightShuntingEngine=False
            elif event.key==K_n:
                pygame.quit()
                sys.exit()

def main():

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.set_colorkey(WHITE)
    pygame.display.update()

    #set start and finish
    start=vector((50, 550))
    finish=vector((750, 50))
    startPoint=planet(10, GREEN, start)
    finishPoint=planet(10, PURPLE, finish)
    startGroup=pygame.sprite.Group()
    finishGroup=pygame.sprite.Group()
    startGroup.add(startPoint)
    finishGroup.add(finishPoint)

    #set player's ship
    playerShip = battleShip(start)
    playerIsAlive=True
    ships=pygame.sprite.Group()
    ships.add(playerShip)

    #set planetary system
    planetarySystem=pygame.sprite.Group()
    planetarySystem.add(planet(30, RED, vector((100, 100))))
    planetarySystem.add(planet (20, BLUE, vector((400, 200))))
    planetarySystem.add(planet (20, BLUE, vector((50, 280))))
    planetarySystem.add(planet (20, BLUE, vector((600, 500))))
    planetarySystem.add(planet (20, BLUE, vector((500, 320))))

    #set asteroids
    asteroidBelt=pygame.sprite.Group()
    asteroidBelt.add(asteroid(vector((150, 5)), vector((3, 3))))

    #set a group of objects that are nortal and not player
    mortalNPC=pygame.sprite.Group()
    mortalNPC=asteroidBelt.copy()

    #the follwing boolean True on the first main loop, need ed for trajectory calculation and draw
    #need to make it more elegant
    firstLoop=True


   
    while True:

        DISPLAYSURF.fill(WHITE)
        deltaSpeed=vector((0, 0))
        deltaRot=0.0
        gravity=vector((0,0))
        astGravity=vector((0,0))
        leftEngine=False
        rightEngine=False
        leftShuntingEngine=False
        rightShuntingEngine=False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            elif event.type == KEYDOWN:
                if event.key==K_RIGHT:#if right arrow pressed -
                    deltaSpeed=vecSum(deltaSpeed, vector((engine*math.cos(playerShip.angle), -engine*math.sin(playerShip.angle))))#right engine works and ship moves forward 
                    deltaRot=deltaRot+engine*rotIner#and slightly rotates counter-clockwise
                    rightEngine=True
                    
                elif event.key==K_LEFT:#if left arrow pressed -
                    deltaSpeed=vecSum(deltaSpeed, vector((engine*math.cos(playerShip.angle), -engine*math.sin(playerShip.angle))))#left engine works and ship moves forward
                    deltaRot=deltaRot-engine*rotIner#and slightly rotates clockwise
                    leftEngine=True

                elif event.key==K_a:#if 'a' key pressed -
                    deltaRot=deltaRot-engine*rotIner# left shunting engine is on and ship slightly rotates clockwise
                    leftShuntingEngine=True

                elif event.key==K_s:#if 's' key pressed -
                    deltaRot=deltaRot+engine*rotIner# right shunting engine is on and ship slightly rotates counter-clockwise
                    rightShuntingEngine=True
        
        #calculate gravity force for player's ship
        for i in planetarySystem.sprites():
            planetVec=i.position
            gravityVec=vector(((planetVec.x-playerShip.position.x), (planetVec.y-playerShip.position.y))) #define vector connecting planet and player's ship
            distance=vecMag(gravityVec)
            iGravityX=i.mass*gConstant*math.pow(distance, -3)*gravityVec.x #calculate x coordinate of planet i gravity
            iGravityY=i.mass*gConstant*math.pow(distance, -3)*gravityVec.y #calculate y coordinate of planet i gravity
            gravity=vecSum(gravity, vector((iGravityX, iGravityY)))

        for ast in asteroidBelt.sprites():
            astAlive=True
            for i in planetarySystem.sprites():
                planetVec=i.position
                gravityVec=vector(((planetVec.x-ast.position.x), (planetVec.y-ast.position.y)))
                distance=vecMag(gravityVec)
                iGravityX=i.mass*gConstant*math.pow(distance, -3)*gravityVec.x #calculate x coordinate of planet i gravity
                iGravityY=i.mass*gConstant*math.pow(distance, -3)*gravityVec.y #calculate y coordinate of planet i gravity
                astGravity=vecSum(astGravity, vector((iGravityX, iGravityY)))
                #check on collisions with planets
                if pygame.sprite.collide_mask(i, ast)!=None: astAlive=False
                
            #check on collisions with borders
            if ast.position.x>=800 or ast.position.y>=600 or ast.position.x<=0 or ast.position.y<=0: astAlive=False
            #check on collision with player
            if pygame.sprite.collide_mask(ast, playerShip)!=None:
                 playerIsAlive=False
                 deathSituation(ships)
            ast.update(astGravity, astAlive)
        
        #collision check
        for i in planetarySystem:
            if pygame.sprite.collide_mask(i, playerShip)!=None:
                playerIsAlive=False
                deathSituation(ships)
                

        #finish check
        for i in finishGroup:
            if pygame.sprite.collide_mask(i, playerShip)!=None:
                playerIsAlive=False
                finishSituation(ships)

        # border check
        if playerShip.position.x>=800 or playerShip.position.y>=600 or playerShip.position.x<=0 or playerShip.position.y<=0:
            playerIsAlive=False
            deathSituation(ships)
            
        
        # draw the ship with engine flames
        playerShip.engineFlames(leftEngine, leftShuntingEngine, rightShuntingEngine, rightEngine)
        ships.update(gravity, deltaSpeed, deltaRot, playerIsAlive)
        #throw away used point in trajectory
        if not firstLoop:
            if currentTraj!=[]: currentTraj.pop(0)

        #draw the trajectory calculate only if it is changed
        if deltaSpeed!=vector((0,0)) or firstLoop==True:
            currentTraj=calcTrajectory(playerShip.position, playerShip.speed, planetarySystem, finishGroup)
            firstLoop=False            
        for i in currentTraj: pygame.draw.circle(DISPLAYSURF, RED, (int(i.x), int(i.y)), 1)
              
        ships.draw(DISPLAYSURF)
        planetarySystem.draw(DISPLAYSURF)
        asteroidBelt.draw(DISPLAYSURF)
        startGroup.draw(DISPLAYSURF)
        finishGroup.draw(DISPLAYSURF)



        '''# module to see ship's movement characteristics
        textAngle=myfont.render("Angle %f" %playerShip.angle, 1, RED) # text of current angle
        textAcc=myfont.render("Acceleration %f, %f" %(playerShip.acc.x, playerShip.acc.y), 1, RED) # text of current acceleration
        textSpeed=myfont.render("Speed %f, %f" %(playerShip.speed.x, playerShip.speed.y), 1, RED) #text of current speed
        textPosition=myfont.render("Position %f, %f" %(playerShip.position.x, playerShip.position.y), 1, RED) #text of current position

        DISPLAYSURF.blit(textAngle, (100, 100))
        DISPLAYSURF.blit(textAcc, (100, 120))
        DISPLAYSURF.blit(textSpeed, (100, 140))
        DISPLAYSURF.blit(textPosition, (100, 160))'''
             
        pygame.display.update()
        FPSCLOCK.tick(FPS)

       

if __name__== '__main__':
    main()
