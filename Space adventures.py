import pygame, sys, math, random, textwrap
from pygame.locals import *
from physics import vector, vecSum, vecDif, multSc, vecMag, unitVec, gravityField

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

trajColor=Color(0, 255, 0, 10)
buttonTextColor=Color(0, 80, 255, 255)
fadedPurpleColor=Color(189, 164, 189, 255)
titleColor=Color(179, 31, 15, 255)


FPS = 30
WINDOWWIDTH = 800 # size of window width in pixels
WINDOWHEIGHT = 600 # size of window height in pixels

#time constant
deltaT=1

#ship engine power
engine=0.2

#ship's 1 divided by rotational inertia momentum
rotIner=0.2

#ship rotation speed
rotSpeed=0.1

#ratio to convert radians to degrees
radDegRatio=180/math.pi

#sides of of the ship
shipHeight = 32
shipWidth = 16

#sides of the foe's rockets
rocketHeight=8
rocketWidth=4

#speed of plasma shots of foe planets
plasmaSpeed=2.0

#max speed of asteroids inside catcher
maxInCatcherSpeed=5.0

#speed of catcher's push
speedCatcherPush=5.0

#fuel consumption parameters
engineConsumption=0.05
shuntingEngineConsumption=0.005
navigateConsumption=0.02

#load last level
f=open("currentLevel", "r")
line=f.readline().rstrip()
currentLevelNumber=int(line)
f.close()

# display settings initiation
global FPSCLOCK, DISPLAYSURF
pygame.init()
FPSCLOCK = pygame.time.Clock()
myfont = pygame.font.SysFont("arial", 15)
bigFont = pygame.font.SysFont("arial", 20, True)
smallFont=pygame.font.SysFont("monospace", 10)
hugeFont=pygame.font.SysFont("impact", 40)

DISPLAYSURF = pygame.display.set_mode ((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Space adventures', 'Space adventures')

#download images
playerImg= pygame.image.load('images/rocket.png').convert_alpha()
mainEngineImg= pygame.image.load('images/rocketMainEngine.png').convert_alpha()
rightShuntingEngineImg= pygame.image.load('images/rocketRightEngine.png').convert_alpha()
leftShuntingEngineImg= pygame.image.load('images/rocketLeftEngine.png').convert_alpha()
leftRightShuntingEngineImg= pygame.image.load('images/rocketLeftRightEngine.png').convert_alpha()
mainLeftShuntingEngineImg= pygame.image.load('images/rocketMainLeftEngine.png').convert_alpha()
mainRightShuntingEngineImg= pygame.image.load('images/rocketMainRightEngine.png').convert_alpha()
mainLeftRightShuntingEngineImg=pygame.image.load('images/rocketMainLeftRightEngine.png').convert_alpha()
neutPlanetImg=pygame.image.load('images/neutPlanet.png').convert_alpha()
frPlanetImg=pygame.image.load('images/frPlanet.png').convert_alpha()
foePlanetImg=pygame.image.load('images/foePlanet.png').convert_alpha()
rocketImg=pygame.image.load('images/foeRocket.png').convert_alpha()
mineralImg=pygame.image.load('images/mineral.png').convert_alpha()
asteroidImg=pygame.image.load('images/asteroid.png').convert_alpha()
asteroidTailImg=pygame.image.load('images/asteroidTail.png').convert_alpha()
startImg=pygame.image.load('images/start.png').convert_alpha()
finishImg=pygame.image.load('images/finish.png').convert_alpha()
finishActiveImg=pygame.image.load('images/finishActive.png').convert_alpha()
background=pygame.image.load('images/background.png').convert_alpha()
menuBackground=pygame.image.load('images/menu.png').convert_alpha()
buttonImg=pygame.image.load('images/button20040.png').convert_alpha()
buttonPressedImg=pygame.image.load('images/buttonPressed20040.png').convert_alpha()
helpPageImg=pygame.image.load('images/helpPage.png').convert_alpha()
mainMenuImg=pygame.image.load('images/mainMenuPicture.png').convert_alpha()
#download explosion
explosions=[]
explosion1=pygame.image.load('images/explosion1.png').convert_alpha()
explosions.append(explosion1)
explosion2=pygame.image.load('images/explosion2.png').convert_alpha()
explosions.append(explosion2)
explosion3=pygame.image.load('images/explosion3.png').convert_alpha()
explosions.append(explosion3)
explosion4=pygame.image.load('images/explosion4.png').convert_alpha()
explosions.append(explosion4)
explosion5=pygame.image.load('images/explosion5.png').convert_alpha()
explosions.append(explosion5)
explosion6=pygame.image.load('images/explosion6.png').convert_alpha()
explosions.append(explosion6)
#download ship's explosion
shipExplosion=[]
explosion1=pygame.image.load('images/rocketExplosion1.png').convert_alpha()
shipExplosion.append(explosion1)
explosion2=pygame.image.load('images/rocketExplosion2.png').convert_alpha()
shipExplosion.append(explosion2)
explosion3=pygame.image.load('images/rocketExplosion3.png').convert_alpha()
shipExplosion.append(explosion3)
explosion4=pygame.image.load('images/rocketExplosion4.png').convert_alpha()
shipExplosion.append(explosion4)
explosion5=pygame.image.load('images/rocketExplosion5.png').convert_alpha()
shipExplosion.append(explosion5)
explosion6=pygame.image.load('images/rocketExplosion6.png').convert_alpha()
shipExplosion.append(explosion6)
#download finish animation
finishAnimation=[]
animation1=pygame.image.load('images/finishAnim1.png').convert_alpha()
finishAnimation.append(animation1)
animation2=pygame.image.load('images/finishAnim2.png').convert_alpha()
finishAnimation.append(animation2)
animation3=pygame.image.load('images/finishAnim3.png').convert_alpha()
finishAnimation.append(animation3)
animation4=pygame.image.load('images/finishAnim4.png').convert_alpha()
finishAnimation.append(animation4)
animation5=pygame.image.load('images/finishAnim5.png').convert_alpha()
finishAnimation.append(animation5)
animation6=pygame.image.load('images/finishAnim6.png').convert_alpha()
finishAnimation.append(animation6)
#download sounds
shipExplosionSound=pygame.mixer.Sound("sounds/ShipExplosion.wav")
finishSound=pygame.mixer.Sound("sounds/Sound.wav")
buttonSound=pygame.mixer.Sound("souns/Sound.wav")
engineSound=pygame.mixer.Sound("sounds/Sound.wav")

class battleShip(pygame.sprite.Sprite):
    def __init__(self, position=vector((0,0))): #take position as a vector in input
        pygame.sprite.Sprite.__init__(self)
        # defines initial position and characterictics of the battle ship
        self.position=position
        self.speed=vector((0, 0))
        self.acc=vector((0, 0))
        self.onOrbit=False
        self.trajectory=[]
        self.alive=True
        self.catcherRadius=20
        self.catcherOn=False
        self.asteroidCaught=None
        self.speedDelta=vector((0, 0))
        self.angleDelta=0.0
        self.mainEngine=False
        self.leftShuntingEngine=False
        self.rightShuntingEngine=False
        self.changeTrajectory=True
        self.mineralCount=0
        self.fuel=10
        self.explosionFramesCount=0
        self.finishFramesCount=0
        self.finish=False

        # defines initial rotation characteristics of battle ship
        # all angular measures are in radians
        self.angle=float(0)
        # intitial rotation
        self.Surf = pygame.Surface((shipWidth, shipHeight))
        self.Surf.blit(playerImg, (0,0))
        self.rotSurf = pygame.transform.rotate(self.Surf, math.degrees(self.angle)-90)
        self.rotSurf.set_colorkey(BLACK)        
        
        self.image=self.rotSurf
        self.rect=self.rotSurf.get_rect().move(self.position.x-self.rotSurf.get_rect().width/2, self.position.y-self.rotSurf.get_rect().height/2)
        self.mask=pygame.mask.from_surface(self.Surf) #create mask for collision

        #calculate coordintes of asteroid catcher
        self.catcherCenter=vecSum(vector((math.cos(self.angle)*(shipHeight/2.0+self.catcherRadius), -math.sin(self.angle)*(shipHeight/2.0+self.catcherRadius))), self.position)

    def update(self, force, asteroidBelt):
        if self.alive and not self.finish:
            if self.onOrbit==False:
                #update decartes position
                # first update position, then - speed and finally - acceleration
                self.position=vecSum(self.position,vecSum(multSc(deltaT, self.speed), multSc(math.pow(deltaT, 2)/2, force)))
                self.speed=vecSum(self.speed, vecSum(self.speedDelta, multSc(deltaT,force)))
                self.acc=force             
                #update rotation
                # first update angle, then rotation
                self.angle+=deltaT*self.angleDelta
                if self.angle>(2*math.pi): self.angle=self.angle%(2*math.pi)
            else:
                #when ship moves on friendly's planet orbit speed and rotation are used in absolute terms
                self.position=vecSum(self.position, multSc(deltaT, self.speedDelta))
                self.speed=self.speedDelta
                self.angle+=deltaT*self.angleDelta
                if self.angle>(2*math.pi): self.angle=self.angle%(2*math.pi)

            #calculate caught asteroids movements and asteroid catch

            if self.asteroidCaught!=None and self.catcherOn==True:
                self.asteroidCatch(self.asteroidCaught)
            elif self.asteroidCaught!=None and self.catcherOn==False:
                self.asteroidPush(self.asteroidCaught)
                self.asteroidCaught=None
            elif self.asteroidCaught==None and self.catcherOn==True:
                distanceToNearest=self.catcherRadius
                for i in asteroidBelt:
                    if vecMag(vecDif(self.catcherCenter, i.position))<distanceToNearest:
                        self.asteroidCaught=i
                        distanceToNearest=vecMag(vecDif(self.catcherCenter, i.position))
                if self.asteroidCaught==None:
                    self.catcherOn=False
                else: self.asteroidCatch(self.asteroidCaught)           
               

            #calculate coordintes of asteroid catcher
            self.catcherCenter=vecSum(vector((math.cos(self.angle)*(shipHeight/2.0+self.catcherRadius), -math.sin(self.angle)*(shipHeight/2.0+self.catcherRadius))), self.position)

            #rotate ship

            self.rotSurf = pygame.transform.rotate(self.Surf, math.degrees(self.angle)-90)
            self.rotSurf.set_colorkey(BLACK)#?? delete this line?
            
            self.image=self.rotSurf
            self.rect=self.rotSurf.get_rect().move(self.position.x-self.rotSurf.get_rect().width/2, self.position.y-self.rotSurf.get_rect().height/2)
            self.mask=pygame.mask.from_surface(self.rotSurf) #create mask for collision

            #set engine and speed characterisics to initial values
            self.speedDelta=vector((0, 0))
            self.angleDelta=0.0
            self.mainEngine=False
            self.leftShuntingEngine=False
            self.rightShuntingEngine=False

        #if player is not alive launch explosion animation
        elif not self.alive:
            animationFrames=5
            numberOfPicture=self.explosionFramesCount//animationFrames
            self.Surf.fill(BLACK)
            self.Surf.blit(shipExplosion[numberOfPicture], (0, 0))
            self.rotSurf = pygame.transform.rotate(self.Surf, math.degrees(self.angle)-90)
            self.rotSurf.set_colorkey(BLACK)
            self.image=self.rotSurf
            self.rect=self.rotSurf.get_rect().move(self.position.x-self.rotSurf.get_rect().width/2, self.position.y-self.rotSurf.get_rect().height/2)
            self.explosionFramesCount+=1
            if self.explosionFramesCount>=FPS:
                pygame.sprite.Sprite.kill(self)
        #if player finished the level launch finish animation
        elif self.finish:
            animationFrames=5
            numberOfPicture=self.finishFramesCount//animationFrames
            self.Surf.fill(BLACK)
            self.Surf.blit(finishAnimation[numberOfPicture], (0, 0))
            self.Surf.set_colorkey(BLACK)
            self.image=self.Surf
            self.rect=self.Surf.get_rect().move(self.position.x-self.Surf.get_rect().width/2, self.position.y-self.Surf.get_rect().height/2)
            self.finishFramesCount+=1
            if self.finishFramesCount>=FPS:
                pygame.sprite.Sprite.kill(self)

    def asteroidCatch(self, other):        
        #returns the speed to the catched object
        if self.catcherCenter==other.position:
            other.speed=self.speed
        elif vecMag(vecDif(self.catcherCenter, other.position))>maxInCatcherSpeed:
            speedDirection=multSc(1.0/vecMag(vecDif(self.catcherCenter, other.position)),vecDif(self.catcherCenter, other.position))
            other.speed=vecSum(self.speed, multSc(maxInCatcherSpeed, speedDirection))
        elif vecMag(vecDif(self.catcherCenter, other.position))<=maxInCatcherSpeed:
            other.speed=vecSum(self.speed, vecDif(self.catcherCenter, other.position))
            
    def asteroidPush(self, other):
        #catcher push in the direction of the player's ship with additional speed of speedCatcherPush in magnitude
        other.speed=multSc(speedCatcherPush, vector((math.cos(self.angle), -math.sin(self.angle))))        

    def engineFlames(self):
        # function is to add flames to ship image
        self.Surf = pygame.Surface((shipWidth, shipHeight))
        #self.Surf.blit(playerImg, (0, 0))
        if self.mainEngine==True:
            if self.leftShuntingEngine==True:
                if self.rightShuntingEngine==True:
                    self.Surf.blit(mainLeftRightShuntingEngineImg, (0, 0))
                    self.fuel-=(engineConsumption+2*shuntingEngineConsumption) 
                else:
                    self.Surf.blit(mainLeftShuntingEngineImg, (0, 0))
                    self.fuel-=(engineConsumption+shuntingEngineConsumption)
            else:
                if self.rightShuntingEngine==True:
                    self.Surf.blit(mainRightShuntingEngineImg, (0, 0))
                    self.fuel-=(engineConsumption+shuntingEngineConsumption)
                else:
                    self.Surf.blit(mainEngineImg, (0, 0))
                    self.fuel-=engineConsumption                 
        else:
            if self.leftShuntingEngine==True:
                if self.rightShuntingEngine==True:
                    self.Surf.blit(leftRightShuntingEngineImg, (0, 0))
                    self.fuel-=2*shuntingEngineConsumption
                else:
                    self.Surf.blit(leftShuntingEngineImg, (0, 0))
                    self.fuel-=shuntingEngineConsumption
            else:
                if self.rightShuntingEngine==True:
                    self.Surf.blit(rightShuntingEngineImg, (0, 0))
                    self.fuel-=shuntingEngineConsumption
                else:
                    self.Surf.blit(playerImg, (0, 0))
    #define function to check whether player collided with the borders
    def checkBorder(self):
        collidedBorder=False
        #for b in borders.sprites():
        #    if pygame.sprite.collide_mask(b, self)!=None: collidedBorder=b.position
        if self.position.x>=WINDOWWIDTH:
            collidedBorder='Right'
        elif self.position.y>=WINDOWHEIGHT:
            collidedBorder='Bottom'
        elif self.position.x<=0:
            collidedBorder='Left'
        elif self.position.y<=0:
            collidedBorder='Top'

        return collidedBorder

    #define new function for ship's behavior after bounce
    def bounce(self, borderPosition):
        impedeFactor=2.0
        if borderPosition=='Left':
            self.speed=vector((abs(self.speed.x/impedeFactor), self.speed.y/impedeFactor))
            self.fuel-=navigateConsumption
            self.speedDelta=vector((0, 0))
        elif borderPosition=='Right':
            self.speed=vector((-abs(self.speed.x/impedeFactor), self.speed.y/impedeFactor))
            self.fuel-=navigateConsumption
            self.speedDelta=vector((0, 0))
        elif borderPosition=='Top':
            self.speed=vector((self.speed.x/impedeFactor, abs(self.speed.y/impedeFactor)))
            self.fuel-=navigateConsumption
            self.speedDelta=vector((0, 0))
        elif borderPosition=='Bottom':
            self.speed=vector((self.speed.x/impedeFactor, -abs(self.speed.y/impedeFactor)))
            self.fuel-=navigateConsumption
            self.speedDelta=vector((0, 0))   

#function to calculate trajectory with given position, speed and acceleration, planetary system
def calcTrajectory(position, velocity, field, planetarySystem):
    traj=[]
    speed=[]
    totalForce=vector((0, 0))
    endOfTraj=False
    
    while not endOfTraj:
        traj.append(position)
        speed.append(velocity)
        #define sum of forces
        totalForce=field.getField(position)
        #define new position and speed
        if totalForce!=vector((0, 0)) or velocity!=vector((0, 0)):
            position=vecSum(position,vecSum(multSc(deltaT, velocity), multSc(math.pow(deltaT, 2)/2, totalForce)))
            velocity=vecSum(velocity, multSc(deltaT,totalForce))
            #check end of trajectory
            if position.x>=WINDOWWIDTH or position.y>=WINDOWHEIGHT or position.x<=0 or position.y<=0: endOfTraj=True
            #check for crash with the plant
            for i in planetarySystem.sprites(): #here i is iterable planet
                planetVec=i.position
                if vecMag(vecDif(position, planetVec))<=i.mass: endOfTraj=True 
            #limit the number of calculated points
            if len(traj)>=3000: endOfTraj=True
        else: endOfTraj=True
    return zip(traj, speed)

class asteroid(pygame.sprite.Sprite):
    def __init__(self, position, speed, tailGroup): #position defines center of the planet and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        # set position and speed of the asteroid
        self.position=position
        self.speed=speed

        #set initial image of the asteroid
        self.surf=pygame.Surface((10, 10)) 
        self.surf.blit(asteroidImg,(0,0))
        self.surf.set_colorkey(BLACK) 
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-5, position.y-5, 10, 10)

        self.tail=asteroidTail(self.position, self.speed)
        tailGroup.add(self.tail)

    def update(self, force, liveState):
        #update decartes position
        # first update position, then - speed 
        self.position=vecSum(self.position,vecSum(multSc(deltaT, self.speed), multSc(math.pow(deltaT, 2)/2, force)))
        self.speed=vecSum(self.speed, multSc(deltaT,force))        
        #update image
        self.rect=pygame.Rect(self.position.x-5, self.position.y-5, 10, 10)
        self.tail.update(self.position, self.speed)

        #check whether the ship is collided
        if liveState==False: self.kill()

    def smashAsteroids(self, other, explosionGroup):
        explosionCenter=vecSum(self.position, multSc(vecMag(vecDif(self.position, other.position))/2.0, unitVec(vecDif(other.position, self.position))))
        explosionGroup.add(explosion(explosionCenter))
        if isinstance(other, asteroid):
            self.kill()
            other.kill()
            self.tail.kill()

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        self.tail.kill()        

class asteroidTail(pygame.sprite.Sprite):
    def __init__(self, astPosition, speed): #position given for tail is the center of its asteroid
        pygame.sprite.Sprite.__init__(self)
        # set position and speed of the asteroid
        self.speed=speed
        self.angle=multSc(-1, self.speed).getAngle()
        self.position=vecSum(astPosition, multSc(7, unitVec(multSc(-1, self.speed))))

        #set an image of the tial
        self.surf=pygame.Surface((10, 15)) 
        self.surf.blit(asteroidTailImg,(0,0))
        self.rotSurf = pygame.transform.rotate(self.surf, math.degrees(self.angle)-90)
        self.rotSurf.set_colorkey(BLACK)        
        
        self.image=self.rotSurf
        self.rect=self.rotSurf.get_rect().move(self.position.x-self.rotSurf.get_rect().width/2, self.position.y-self.rotSurf.get_rect().height/2)

    def update(self, astPosition, speed):

        self.speed=speed
        self.angle=multSc(-1, self.speed).getAngle()
        self.position=vecSum(astPosition, multSc(7, unitVec(multSc(-1, self.speed))))

        self.rotSurf = pygame.transform.rotate(self.surf, math.degrees(self.angle)-90)
        self.rotSurf.set_colorkey(BLACK)        
        
        self.image=self.rotSurf
        self.rect=self.rotSurf.get_rect().move(self.position.x-self.rotSurf.get_rect().width/2, self.position.y-self.rotSurf.get_rect().height/2)
    

# define planet class as sprite
class planet(pygame.sprite.Sprite):
    def __init__(self, mass, color, position): #position defines center of the planet and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        self.mass=mass #mass of the planet define gravity magnitude and radius
        self.color=color #color just for visualization
        self.position=position #position of the planet on screen
        self.surf=pygame.Surface((2*mass, 2*mass)) #surface of the planet
        self.surf.blit(neutPlanetImg, (0, 0))#draw a planet on planets' surface in center of the surface
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-mass, position.y-mass, 2*mass, 2*mass) # mass is subtracted use position as a center

    def update(self, other, plasmaGroup):
        pygame.sprite.Sprite.update(self)
        

class start(pygame.sprite.Sprite):
    def __init__(self, position): #position defines center of the start and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        self.position=position #position of the start on screen
        self.surf=pygame.Surface((20, 20)) #surface of the start
        self.surf.blit(startImg, (0, 0))
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-10, position.y-10, 20, 20)

class finish(pygame.sprite.Sprite):
    def __init__(self, position): #position defines center of the start and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        self.active=False
        self.position=position #position of the start on screen
        self.surf=pygame.Surface((20, 20)) #surface of the start
        self.surf.blit(finishImg, (0, 0))
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-10, position.y-10, 20, 20)

    def activate(self):
        self.active=True
        self.surf.blit(finishActiveImg, (0, 0))
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf

class explosion(pygame.sprite.Sprite):
    def __init__(self, position): #position defines center of the explosion and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        self.explosionFramesCount=0
        self.explosionAnimation=explosions
        self.position=position
        self.Surf=pygame.Surface((16, 16))
        self.Surf.set_colorkey(BLACK)
        self.image=self.Surf
        self.rect=pygame.Rect(self.position.x-8, self.position.y-8, 16, 16)

    def update(self, mineralGroup):
        #number of frames for each animation picture
        animationFrames=5
        numberOfPicture=self.explosionFramesCount//animationFrames
        self.Surf.fill(BLACK)
        self.Surf.blit(self.explosionAnimation[numberOfPicture], (0, 0))
        self.image=self.Surf
        self.rect=pygame.Rect(self.position.x-8, self.position.y-8, 16, 16)
        self.explosionFramesCount+=1
        if self.explosionFramesCount>=FPS:
            mineralGroup.add(mineral(self.position))
            pygame.sprite.Sprite.kill(self)

#define class of friendly planet
class frPlanet(planet):
    def __init__(self, mass, color, position):
        planet.__init__(self, mass, color, position)
        #set friendly planet orbit on planets radius plus 20
        self.surf=pygame.Surface((2*mass, 2*mass)) #surface of the planet
        self.surf.blit(frPlanetImg,(0,0))#draw a planet on planets' surface in center of the surface
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-mass, position.y-mass, 2*mass, 2*mass) # mass is subtracted use position as a center
        self.orbitRadius=float(mass+20)
        #define speed of ship on the orbit in number of turns over planet in one frame
        self.orbitalSpeed=1.0/(7.0*FPS)
        self.orbit=[]
        alpha=0
        for i in range(int(1/self.orbitalSpeed)):
            x=self.position.x+int(self.orbitRadius*math.cos(alpha))
            y=self.position.y-int(self.orbitRadius*math.sin(alpha))
            try:
                if self.orbit[len(self.orbit)-1]!=(x, y):
                    self.orbit.append((x, y))
            except:
                self.orbit.append((self.position.x+int(self.orbitRadius), self.position.y))
            alpha+=2.0*math.pi*self.orbitalSpeed

    def takeOnOrbit(self, other):
        if isinstance(other, battleShip):
            deltaAngle=0.0
            other.onOrbit=True
            other.fuel=10
            #returns the list of three numbers: x speed of the ship, y speed of the ship, delta of the ship's angle
            #find nearest orbit's point
            if (int(other.position.x), int(other.position.y)) in self.orbit:
                point=self.orbit.index((int(other.position.x), int(other.position.y)))
                nextPoint=point+1
                if nextPoint>len(self.orbit)-1:
                    nextPoint=nextPoint%len(self.orbit)
                xSpeed=self.orbit[nextPoint][0]-self.orbit[point][0]
                ySpeed=self.orbit[nextPoint][1]-self.orbit[point][1]
            else:
                nearestPoint=min(self.orbit, key=lambda i: math.pow(i[0]-other.position.x, 2)+math.pow(i[1]-other.position.y, 2))
                nextPoint=self.orbit.index(nearestPoint)
                xSpeed=self.orbit[nextPoint][0]-other.position.x
                ySpeed=self.orbit[nextPoint][1]-other.position.y
            other.speedDelta=vector((xSpeed, ySpeed))

#define cless of foe planet
class foePlanet(planet):
    def __init__(self, mass, color, position, fireRadius):
        planet.__init__(self, mass, color, position)
        self.surf=pygame.Surface((2*mass, 2*mass)) #surface of the planet
        self.surf.blit(foePlanetImg,(0,0))#draw a planet on planets' surface in center of the surface
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-mass, position.y-mass, 2*mass, 2*mass) # mass is subtracted use position as a center
        #set fire radius
        self.fireRadius=(mass+fireRadius)
        #set shot interval as internal constant
        self.shotInterval=3*FPS
        self.timeFromLastShot=self.shotInterval

    def update(self, other, plasmaGroup):
        planet.update(self, other, plasmaGroup)
        if self.timeFromLastShot<self.shotInterval: self.timeFromLastShot+=1
        #here foe planet shoots in player when it is close and planet is ready
        if vecMag(vecDif(self.position, other.position))<=(self.fireRadius) and self.timeFromLastShot==self.shotInterval and isinstance(other, battleShip) and other.alive==True:
            self.shoot(other, plasmaGroup)
            self.timeFromLastShot=0

    def shoot(self, other, plasmaGroup):
        trajectory=other.trajectory
        if trajectory!=[]:
            #create a dictionary with the difference between estimated time of plasma ball arrival and estimated time of player arrival to the point in trajectory
            #it also takes mass of the planet (i.e. its radius) as plasmastarts from there
            eta={x: (int((vecMag(vecDif(self.position, x))-self.mass)/plasmaSpeed)-trajectory.index(x))**2 for x in trajectory}
            #take a minimum of differences between time of player and and plasma shot arrival
            shootPoint=min(trajectory, key=lambda x: eta[x])
            shootDirection=multSc(1.0/vecMag(vecDif(shootPoint, self.position)),vecDif(shootPoint, self.position))
            plasmaVector=multSc(plasmaSpeed, shootDirection)
            plasmaPosition=vecSum(self.position, multSc(self.mass, shootDirection))
            plasmaGroup.add(plasmaBall(plasmaPosition, plasmaVector))
    

class plasmaBall(pygame.sprite.Sprite):
    def __init__(self, position, speed): #position defines center of the plasma ball and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        # set position and speed of the plasma shot
        self.position=position
        self.speed=speed
        #calculate angle of the rocket
        self.angle=self.speed.getAngle()
           
        #set initial image of the foe's rocket
        self.Surf = pygame.Surface((rocketWidth, rocketHeight))
        self.Surf.blit(rocketImg, (0, 0))
        self.rotSurf = pygame.transform.rotate(self.Surf, math.degrees(self.angle)-90)
        self.rotSurf.set_colorkey(BLACK)        
        
        self.image=self.rotSurf
        self.rect=pygame.Rect(self.position.x-rocketHeight/2, self.position.y-rocketHeight/2, rocketHeight, rocketHeight)
        self.mask=pygame.mask.from_surface(self.rotSurf) #create mask for collision

    def update(self, liveState):
        #update decartes position
        # first update position, then - speed 
        self.position=vecSum(self.position,multSc(deltaT, self.speed))              
                
        #update image
        self.rect=pygame.Rect(self.position.x-rocketHeight/2, self.position.y-rocketHeight/2, rocketHeight, rocketHeight)

        #check whether the ship is collided
        if liveState==False: self.kill()

    def kill(self):
        pygame.sprite.Sprite.kill(self)
       
class asteroidSpawnSpot():
    def __init__(self, position, velocity, interval, planetarySystem, asteroidGroup, tailGroup):
        self.position=position #position of the asteroid spawn spot
        self.velocity=velocity #speed of the asteroids from this particular spot
        self.interval=interval #interval asteroids respawn in frames
        self.internalFrames=0 #number of frames from last asteroid respawn
        field=gravityField(planetarySystem)
        spotTraj=calcTrajectory(self.position, self.velocity, field, planetarySystem)
        for i, y in spotTraj:
            if spotTraj.index((i, y))%self.interval==0:
                asteroidGroup.add(asteroid(i, y, tailGroup))

    def update(self, asteroidGroup, tailGroup):
        #check whether it is time to shoot
        self.internalFrames+=1
        if self.internalFrames==self.interval:
            #spawn asteroid and number of frames from last asteroid respawn set to zero
            asteroidGroup.add(asteroid(self.position, self.velocity, tailGroup))
            self.internalFrames=0

class mineral(pygame.sprite.Sprite):
    def __init__(self, position): #position defines center of the mineral and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        self.position=position #position of the mineral on screen
        self.surf=mineralImg
        self.surf.set_colorkey(BLACK) #set black as transperent color
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-self.surf.get_width()/2, position.y-self.surf.get_height()/2, self.surf.get_width(), self.surf.get_height()) #dimensions of the surface are direct from image

    def kill(self):
        pygame.sprite.Sprite.kill(self)


class button():
    def __init__(self, center, image, imagePressed, text):
        self.image=image
        self.imagePressed=imagePressed
        self.text=text
        self.buttonPressed=False
        buttonWidth=self.image.get_rect().width
        buttonHeight=self.image.get_rect().height
        self.rect=pygame.Rect((center[0]-buttonWidth/2, center[1]-buttonHeight/2), (buttonWidth, buttonHeight))

    def update(self, displaySurf, mousePressedPoint):
        if self.rect.collidepoint(mousePressedPoint)==False:            
            displaySurf.blit(self.image, self.rect.topleft)
            buttonText=myfont.render(self.text, 1, buttonTextColor)
            textWidth, textHeight=myfont.size(self.text)
            displaySurf.blit(buttonText, (self.rect.centerx-int(textWidth/2), self.rect.centery-int(textHeight/2)))
        elif self.rect.collidepoint(mousePressedPoint)==True:
            displaySurf.blit(self.imagePressed, self.rect.topleft)
            buttonText=myfont.render(self.text, 1, WHITE)
            textWidth, textHeight=myfont.size(self.text)
            displaySurf.blit(buttonText, (self.rect.centerx-int(textWidth/2), self.rect.centery-int(textHeight/2)))
            #buttonSound.play(loops=0)
            self.buttonPressed=True

class label():
    def __init__(self, leftTopCorner, text, widthChar, width=0, height=0, thickness=1, color=BLUE): #here widthChar taken in # of characters, not pixels
        self.leftTopCorner=leftTopCorner
        self.thickness=thickness
        self.color=color
        self.textLines=textwrap.wrap(text, widthChar)
        self.textLinesRender=[]
        self.width=0
        self.height=6 #3 is top and bottom indent
        for l in self.textLines:
            renderLine=myfont.render(l, 1, self.color)
            self.textLinesRender.append(renderLine)
            lineWidth=myfont.size(l)[0]+10 #5 is left and right indent
            lineHeight=myfont.size(l)[1]
            self.width=max(self.width, lineWidth)
            self.height+=lineHeight
        #if height and width are listed and larger than width of text - use them
        if self.height<height: self.height=height
        if self.width<width: self.width=width
        self.rect=pygame.Rect(self.leftTopCorner, (self.width, self.height))
            
    def draw(self, displaySurf):
        pygame.draw.rect(displaySurf, WHITE, self.rect)
        if self.thickness!=0:
            pygame.draw.rect(displaySurf, self.color, self.rect, self.thickness)
        currentCorner=(self.leftTopCorner[0]+5, self.leftTopCorner[1]+3)
        for l in self.textLinesRender:
            displaySurf.blit(l, currentCorner)
            currentCorner=(currentCorner[0], currentCorner[1]+((self.height-6)/len(self.textLinesRender)))     
   

class inputHandler():
    def __init__(self):
        pass

    def update(self, keys, previousKeys, game):       
               
        if game.gameMode.name=='campaign' or game.gameMode.name=='random level' or game.gameMode.name=='training':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if game.gameMode.name=='campaign':
                        f=open("currentLevel", 'r+')
                        f.write("%d\n" %game.currentLevel.number)
                        f.close()
                    pygame.quit()
                    sys.exit()
                   
                elif game.paused==True and event.type==KEYDOWN:
                    game.paused=False
               
            if keys[pygame.K_UP]!=0 and game.playerShip.fuel>=0:
                game.playerShip.speedDelta=vecSum(game.playerShip.speedDelta, vector((engine*math.cos(game.playerShip.angle), -engine*math.sin(game.playerShip.angle))))#engines work and ship moves forward
                game.playerShip.mainEngine=True
                game.playerShip.onOrbit=False
                game.playerShip.changeTrajectory=True

            elif keys[pygame.K_RIGHT]!=0 and game.playerShip.fuel>=0:
                game.playerShip.angleDelta-=rotSpeed# left shunting engine is on and ship slightly rotates clockwise
                game.playerShip.leftShuntingEngine=True

            elif keys[pygame.K_LEFT]!=0 and game.playerShip.fuel>=0:
                game.playerShip.angleDelta+=rotSpeed# right shunting engine is on and ship slightly rotates counter-clockwise
                game.playerShip.rightShuntingEngine=True

            elif keys[pygame.K_SPACE]!=0 and previousKeys[pygame.K_SPACE]==0 and game.playerShip.fuel>=0:
                #if space is pushed asteroid catcher is on
                game.playerShip.catcherOn=not game.playerShip.catcherOn

            elif keys[pygame.K_PAUSE]!=0 and previousKeys[pygame.K_PAUSE]==0 and game.paused==False:
                game.paused=True

        elif game.gameMode.name in ['finish', 'death', 'main menu', 'finish random', 'training death', 'training finish', 'help', 'win', 'training win']:
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    game.mousePressed=pygame.mouse.get_pos()
                elif event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()

#define a class of game mode
class mode():
    def __init__(self, name, buttons):
        self.name=name
        self.buttons=buttons

#class that stores imformation on the game level
class level():
    def __init__(self, number, mode='campaign'):
        self.number=number
        self.startGroup=pygame.sprite.Group()
        self.finishGroup=pygame.sprite.Group()
        self.planetarySystem=pygame.sprite.Group()
        #set asteroids
        self.asteroidBelt=pygame.sprite.Group()
        self.tailGroup=pygame.sprite.Group()
        self.asteroidSpawnPoints=[]
        #set plasma
        self.plasmaShots=pygame.sprite.Group()
        #set explosions
        self.explosionGroup=pygame.sprite.Group()
        #set group of minerls sprites
        self.minerals=pygame.sprite.Group()
        self.load(self.number, mode)

    def load(self, number, mode='campaign'):
        self.number=number
        self.startGroup.empty()
        self.finishGroup.empty()
        self.planetarySystem.empty()
        self.asteroidBelt.empty()
        self.tailGroup.empty()
        self.plasmaShots.empty()
        self.explosionGroup.empty()
        self.minerals.empty()
        self.asteroidSpawnPoints=[]
        self.requiredMinerals=0
        self.pausedLabels=[]
        self.pausedLabels.append(label((280, 550),"Press any key to resume game", 30, 0, 0, 0, RED))
        self.winSituation=False
        self.trWinSituation=False
        levelLoaded=False
        if mode=='campaign':
            levelFile=open("levels", "r")
        elif mode=='training':
            levelFile=open("trLevels", "r")
        while not levelLoaded:
            strLevelNumber=''
            line=levelFile.readline().rstrip()
            if line=='':
                if mode=='campaign': self.winSituation=True
                elif mode=='training':
                    self.trWinSituation=True
                break
            #check that we read needed level
            if line[0]=='#':
                for i in range(1, len(line)):
                    strLevelNumber+=line[i]
            if strLevelNumber=='': strLevelNumber='0'
            if self.number==int(strLevelNumber):
                #read block of strings line by line with planet coordinates and other parameters
                while line[0]!='-':
                    line=levelFile.readline().rstrip()
                    if line=='planets':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            planetParams=line.split(' ')
                            try:
                                self.planetarySystem.add(planet(int(planetParams[2]), BLUE, vector((int(planetParams[0]), int(planetParams[1])))))
                            except: pass
                            line=levelFile.readline().rstrip()
                    elif line=='frPlanets':
                        line=levelFile.readline()
                        while line!='.':
                            planetParams=line.split(' ')
                            try:
                                self.planetarySystem.add(frPlanet(int(planetParams[2]), GREEN, vector((int(planetParams[0]), int(planetParams[1])))))
                            except: pass
                            line=levelFile.readline().rstrip()
                    elif line=='foePlanets':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            planetParams=line.split(' ')
                            try:
                                self.planetarySystem.add(foePlanet(int(planetParams[2]), RED, vector((int(planetParams[0]), int(planetParams[1]))), int(planetParams[3])))
                            except: pass
                            line=levelFile.readline().rstrip()
                    elif line=='asteroidSpawnPoints':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            parameters=line.split(' ')
                            try:
                                self.asteroidSpawnPoints.append(asteroidSpawnSpot(vector((int(parameters[0]), int(parameters[1]))), vector((parameters[2], parameters[3])), int(parameters[4]), self.planetarySystem, self.asteroidBelt,
                                                                                  self.tailGroup))
                            except IndexError: pass
                            line=levelFile.readline().rstrip()
                    elif line=='minerals':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            parameters=line.split(' ')
                            try:
                                self.minerals.add(mineral(vector((int(parameters[0]), int(parameters[1])))))
                            except: pass
                            line=levelFile.readline().rstrip()
                    elif line=='required minerals':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            parameters=line.split(' ')
                            try:
                                self.requiredMinerals=int(parameters[0])
                            except: pass
                            line=levelFile.readline().rstrip()    
                    elif line=='labels':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            parameters=[]
                            if line[0]=='?': text=line[1:]
                            else:
                                parameters=line.split(' ')
                            try:
                                if parameters!=[]:
                                    self.pausedLabels.append(label((int(parameters[0]), int(parameters[1])), text, int(parameters[2]), int(parameters[3]), int(parameters[4]), int(parameters[5])))
                            except IndexError: pass
                            line=levelFile.readline().rstrip()
                    elif line=='start':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            parameters=line.split(' ')
                            self.start=vector((int(parameters[0]), int(parameters[1])))
                            self.startGroup.add(start(self.start))
                            line=levelFile.readline().rstrip()
                    elif line=='finish':
                        line=levelFile.readline().rstrip()
                        while line!='.':
                            parameters=line.split(' ')
                            self.finish=vector((int(parameters[0]), int(parameters[1])))
                            self.finishGroup.add(finish(self.finish))
                            line=levelFile.readline().rstrip()
                levelLoaded=True
        levelFile.close()
    #method to create random level
    def getRandom(self):
        random.seed()
        #clear current level
        self.startGroup.empty()
        self.finishGroup.empty()
        self.planetarySystem.empty()
        self.asteroidBelt.empty()
        self.tailGroup.empty()
        self.plasmaShots.empty()
        self.explosionGroup.empty()
        self.asteroidSpawnPoints=[]
        #set group of minerls sprites
        self.minerals=pygame.sprite.Group()
        self.requiredMinerals=0
        self.pausedLabels=[]

        #define the number of level objects
        numberPlanets=random.randint(1,7)
        numberFrPlanets=random.randint(1,3)
        numberFoePlanets=random.randint(1,3)
        numberAsteroidSpawnPoints=random.randint(1,3)

        #set loops controllers
        levelSet=False
        planetsSet=False
        frPlanetsSet=False
        foePlanetsSet=False
        asteroidSpawnSpotsSet=False
        startSet=False
        finishSet=False

        while not levelSet:
            #set planets
            i=0
            while not planetsSet:
                newMass=40
                newX=random.randint(newMass, WINDOWWIDTH-newMass)
                newY=random.randint(newMass, WINDOWHEIGHT-newMass)
                newPosition=vector((newX, newY))
                if self.planetarySystem.sprites()==[]:
                    self.planetarySystem.add(planet(newMass, BLUE, newPosition))
                else:
                    overlap=0
                    for p in self.planetarySystem.sprites():
                        if vecMag(vecDif(newPosition, p.position))<=(newMass+p.mass):
                            overlap+=1
                    if overlap==0:
                        self.planetarySystem.add(planet(newMass, BLUE, newPosition))
                        i+=1
                        if i==numberPlanets: planetsSet=True

            #set friendly planets
            i=0
            while not frPlanetsSet:
                newMass=40
                newX=random.randint(newMass, WINDOWWIDTH-newMass)
                newY=random.randint(newMass, WINDOWHEIGHT-newMass)
                newPosition=vector((newX, newY))
                overlap=0
                for p in self.planetarySystem.sprites():
                    if isinstance(p, frPlanet) and vecMag(vecDif(newPosition, p.position))<=(newMass+20+p.orbitRadius):
                        overlap+=1
                    elif vecMag(vecDif(newPosition, p.position))<=(newMass+20+p.mass):
                        overlap+=1
                if overlap==0:
                    self.planetarySystem.add(frPlanet(newMass, GREEN, newPosition))
                    i+=1
                    if i==numberFrPlanets: frPlanetsSet=True

            #set foe planets
            i=0
            while not foePlanetsSet:
                newMass=40
                newX=random.randint(newMass, WINDOWWIDTH-newMass)
                newY=random.randint(newMass, WINDOWHEIGHT-newMass)
                newPosition=vector((newX, newY))
                newFireRadius=random.randint(20, 70)
                overlap=0
                for p in self.planetarySystem.sprites():
                    if isinstance(p, frPlanet) and vecMag(vecDif(newPosition, p.position))<=(newMass+p.orbitRadius):
                        overlap+=1
                    elif vecMag(vecDif(newPosition, p.position))<=(newMass+p.mass):
                        overlap+=1
                if overlap==0:
                    self.planetarySystem.add(foePlanet(newMass, RED, newPosition, newFireRadius))
                    i+=1
                    if i==numberFoePlanets: foePlanetsSet=True

            #set asteroid spawn spots
            i=0
            while not asteroidSpawnSpotsSet:
                #asteroid spawn spots are alonge the edges of the window
                newX=random.randint(5, WINDOWWIDTH-5)
                newY=random.randint(5, WINDOWHEIGHT-5)
                seq=((5, newY), (newX, 5), (WINDOWWIDTH-5, newY), (newX, WINDOWHEIGHT-5))
                newPosition=vector(random.choice(seq))
                #set direction of the asteroids speed
                if newPosition.x==5: newXSpeed=random.randint(1, 4)
                elif newPosition.x==WINDOWWIDTH-5: newXSpeed=random.randint(-4, -1)
                else: newXSpeed=random.randint(-4, 4)
                if newPosition.y==5: newYSpeed=random.randint(1, 4)
                elif newPosition.y==WINDOWHEIGHT-5: newYSpeed=random.randint(-4, -1)
                else: newYSpeed=random.randint(-4, 4)
                newSpeed=vector((newXSpeed, newYSpeed))
                #set asteroid interval
                newInterval=random.randint(10, 60)
                #add new asteroid spawn spot
                self.asteroidSpawnPoints.append(asteroidSpawnSpot(newPosition, newSpeed, newInterval, self.planetarySystem, self.asteroidBelt, self.tailGroup))
                i+=1
                if i==numberAsteroidSpawnPoints: asteroidSpawnSpotsSet=True

            #set start
            i=0
            while not startSet:
                newX=random.randint(newMass, WINDOWWIDTH-newMass)
                newY=random.randint(newMass, WINDOWHEIGHT-newMass)
                newPosition=vector((newX, newY))
                overlap=0
                for p in self.planetarySystem.sprites():
                    if isinstance(p, frPlanet) and vecMag(vecDif(newPosition, p.position))<=(10+p.orbitRadius):
                        overlap+=1
                    elif vecMag(vecDif(newPosition, p.position))<=(10+p.mass):
                        overlap+=1
                if overlap==0:
                    self.startGroup.add(start(newPosition))
                    self.start=newPosition
                    i+=1
                    if i==1: startSet=True

            #set finish
            i=0
            while not finishSet:
                newX=random.randint(newMass, WINDOWWIDTH-newMass)
                newY=random.randint(newMass, WINDOWHEIGHT-newMass)
                newPosition=vector((newX, newY))
                overlap=0
                for p in self.planetarySystem.sprites():
                    if isinstance(p, frPlanet) and vecMag(vecDif(newPosition, p.position))<=(10+p.orbitRadius):
                        overlap+=1
                    elif vecMag(vecDif(newPosition, p.position))<=(10+p.mass):
                        overlap+=1
                if overlap==0:
                    self.finishGroup.add(finish(newPosition))
                    self.finish=newPosition
                    i+=1
                    if i==1: finishSet=True
            levelSet=True

#define a class with key game mechanics for each game mode
class game():
    def __init__(self, gameMode):
        self.gameMode=gameMode
        self.mousePressed=(0,0)
        self.paused=False
        self.deathClock=0 #this counts for 40 frames after each collision
        self.finishClock=0 #counts for 40 frames after finish moment 

    def update(self, displaySurf):
        global currentLevelNumber
        if self.gameMode.name=='main menu':
            displaySurf.blit(menuBackground, (0,0))
            headText=hugeFont.render("Space adventures", 1, titleColor)
            headTextWidth, headTextHeight=hugeFont.size("Space adventures")
            displaySurf.blit(headText, (400-int(headTextWidth/2), 230-int(headTextHeight/2)))
            displaySurf.blit(mainMenuImg, (400-int(headTextWidth/2), 130-int(headTextHeight/2)))
            
            #draw main menu
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='NEW CAMPAIGN':
                        currentLevelNumber=1
                        self.currentLevel=level(1)                        
                        self.changeMode(campaignMode)
                    if b.text=='RESUME CAMPAIGN':
                        self.currentLevel=level(currentLevelNumber)
                        self.changeMode(campaignMode)
                    elif b.text=='HOW TO PLAY':
                        self.currentLevel=level(1, 'training')
                        self.changeMode(trainingMode)
                    elif b.text=='RANDOM MAP':
                        randomLevelMode=mode('random level', [])
                        self.currentLevel=level(1)
                        self.currentLevel.getRandom()
                        self.changeMode(randomLevelMode)
                    elif b.text=='HELP':
                        self.changeMode(helpPageMode)
                    elif b.text=='EXIT':
                        pygame.quit()
                        sys.exit()
                    b.buttonPressed=False
                    self.mousePressed=(0,0)
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            
        
        elif self.gameMode.name=='campaign' or self.gameMode.name=='random level' or self.gameMode.name=='training':
            #print ('started game mode')
            displaySurf.blit(background, (0, 0))            
            gravity=vector((0,0))
            astGravity=vector((0,0))
        
            #print('calculate gravity force for player ship')
            gravity=self.levelGravity.getField(self.playerShip.position)

            #print('for friendly planets check that player is on the orbit')        
            for i in self.planetarySystem.sprites():
                if isinstance(i, frPlanet):
                    if vecMag(vecDif(i.position, self.playerShip.position))<=i.orbitRadius+1: #+1 here used as a kind of tolerance                   
                        if self.playerShip.mainEngine==False:
                            i.takeOnOrbit(self.playerShip)

            #print('asteroids position and collision check')
            for ast in self.asteroidBelt.sprites():
                astGravity=self.levelGravity.getField(ast.position)
                astAlive=True
                #check on collisions with planets
                for i in self.planetarySystem.sprites():
                    if pygame.sprite.collide_mask(i, ast)!=None: astAlive=False
                
                #check on collisions with borders
                if ast.position.x>=800 or ast.position.y>=600 or ast.position.x<=0 or ast.position.y<=0: astAlive=False
                #check on collision with player
                if pygame.sprite.collide_mask(ast, self.playerShip)!=None:
                    self.playerShip.alive=False
                    astAlive=False
                    if self.deathClock==0:
                        self.deathClock+=1
                        shipExplosionSound.play(loops=0, maxtime=2000)
                if not self.paused: ast.update(astGravity, astAlive)
                #check on collision of two asteroids
                for ast2 in self.asteroidBelt.sprites():
                    if ast2.position!=ast.position:
                        if pygame.sprite.collide_mask(ast, ast2)!=None: ast.smashAsteroids(ast2, self.explosionGroup)                        
        
            #print('plasma shots collision check')
            for shot in self.plasmaShots.sprites():
                shotAlive=True
                if pygame.sprite.collide_mask(shot, self.playerShip)!=None:
                    self.playerShip.alive=False
                    shotAlive=False
                    if self.deathClock==0:
                        self.deathClock+=1
                        shipExplosionSound.play(loops=0, maxtime=2000)
                if not self.paused: shot.update(shotAlive)
                            
            #print('player collision with planet check')
            for i in self.planetarySystem.sprites():
                if pygame.sprite.collide_mask(i, self.playerShip)!=None:
                    self.playerShip.alive=False
                    if self.deathClock==0:
                        self.deathClock+=1
                        shipExplosionSound.play(loops=0, maxtime=2000)

            #print('finish check')
         
            if self.playerShip.mineralCount>=self.requiredMinerals:
                for i in self.finishGroup.sprites():
                    if pygame.sprite.collide_mask(i, self.playerShip)!=None:
                        self.playerShip.finish=True
                        if self.finishClock==0:
                            self.finishClock+=1
                            #finishSound.play(loops=0)
                        

            #print('border check')
            if self.playerShip.checkBorder():
                self.playerShip.bounce(self.playerShip.checkBorder())
                if self.playerShip.fuel<=0:
                    if self.gameMode.name=='campaign': self.changeMode(deathMode)
                    elif self.gameMode.name=='training': self.changeMode(trDeathMode)
                    elif self.gameMode.name=='random level': self.changeMode(finishRandomMode)
                    self.playerShip.kill()
                    
            #minerals collision check
            for m in self.minerals.sprites():
                if pygame.sprite.collide_mask(m, self.playerShip)!=None:
                    self.playerShip.mineralCount+=1
                    m.kill()
                    
            if not self.paused:
                # update the ship with engine flames
                self.playerShip.engineFlames()
                self.ships.update(gravity, self.asteroidBelt)
                #throw away used point in trajectory
                if not self.playerShip.changeTrajectory:
                    if self.playerShip.trajectory!=[]: self.playerShip.trajectory.pop(0)
                
                
                #print('update asteroids')
                for point in self.asteroidSpawnPoints:
                    point.update(self.asteroidBelt, self.tailGroup)

                #print('update planetary system')
                self.planetarySystem.update(self.playerShip, self.plasmaShots)

                #update explosions
                self.explosionGroup.update(self.minerals)
           

            #draw fuel level
            #define top left corner of the left bar of fuel
            currentCorner=(770, 40)
            if self.playerShip.fuel//1>0:
                for bar in range(int(self.playerShip.fuel)):
                    fuelBar=pygame.Rect(currentCorner, (15, 40))
                    pygame.draw.rect(displaySurf, ORANGE, fuelBar)
                    currentCorner=(currentCorner[0]-20, currentCorner[1])
            if self.playerShip.fuel%1>0 and self.playerShip.fuel>0:
                fuelBar=pygame.Rect(currentCorner, (15, int(40*(self.playerShip.fuel%1))))
                pygame.draw.rect(displaySurf, ORANGE, fuelBar)

            #print('draw the trajectory calculate only if it is changed')
            if self.playerShip.onOrbit==False and self.playerShip.alive==True:
                if self.playerShip.changeTrajectory==True:
                    #engineSound.play(loops=0, maxtime=1000)
                    self.playerShip.trajectory=list(zip(*calcTrajectory(self.playerShip.position, self.playerShip.speed, self.levelGravity, self.planetarySystem))[0])
                    self.playerShip.changeTrajectory=False
                trajectorySurf=pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
                trajectorySurf.fill(BLACK)
                trajectorySurf.set_colorkey(BLACK)
                count=0
                for i in self.playerShip.trajectory:
                    if count%10==0:
                        pygame.draw.circle(trajectorySurf, trajColor, (int(i.x), int(i.y)), 2)
                    count+=1
                trajectorySurf.set_alpha(128)
                displaySurf.blit(trajectorySurf, (0,0))
            
            #print('draw objects')

            self.tailGroup.draw(displaySurf)
            self.planetarySystem.draw(displaySurf)
            self.asteroidBelt.draw(displaySurf)
            self.plasmaShots.draw(displaySurf)
            self.startGroup.draw(displaySurf)
            self.explosionGroup.draw(displaySurf)
            self.minerals.draw(displaySurf)

            #draw finish active if required minerals are collected
            
            for f in self.finishGroup:
                if self.playerShip.mineralCount>=self.requiredMinerals and f.active==False: f.activate()
            self.finishGroup.draw(displaySurf)

            #draw player
            self.ships.draw(displaySurf)

            #draw asteroid catcher
            if self.playerShip.alive and not self.playerShip.finish:
                pygame.draw.circle(displaySurf, BLUE, (int(self.playerShip.catcherCenter.x), int(self.playerShip.catcherCenter.y)), 0)
                pygame.draw.circle(displaySurf, BLUE, (int(self.playerShip.catcherCenter.x), int(self.playerShip.catcherCenter.y)), int(self.playerShip.catcherRadius), 1)
            #draw freindly orbits and foe fire radii
            for p in self.planetarySystem:
                if isinstance(p, frPlanet):
                    for i in p.orbit:
                        pygame.draw.circle(displaySurf, GREEN, (int(i[0]), int(i[1])), 0)
                if isinstance(p, foePlanet):
                    pygame.draw.circle(displaySurf, RED, (int(p.position.x), int(p.position.y)), int(p.fireRadius), 1)

            

            # module to see ship's movement characteristics
            '''textAngle=myfont.render("Angle %f" %self.playerShip.angle, 1, RED) # text of current angle
            textAcc=myfont.render("angle to planet %f" %((400.0 - self.playerShip.position.x)/60.0), 1, RED) # text of current angle to planet
            textSpeed=myfont.render("Speed %f, %f" %(self.playerShip.speed.x, self.playerShip.speed.y), 1, RED) #text of current speed
            textPosition=myfont.render("Position %f, %f" %(self.playerShip.position.x, self.playerShip.position.y), 1, RED) #text of current position

            displaySurf.blit(textAngle, (100, 100))
            displaySurf.blit(textAcc, (100, 120))
            displaySurf.blit(textSpeed, (100, 140))
            displaySurf.blit(textPosition, (100, 160))'''
            #draw text
            textMinerals=bigFont.render("Minerals %d / %d" %(self.playerShip.mineralCount, self.requiredMinerals), 1, WHITE)
            textFuel=bigFont.render("Fuel", 1, ORANGE)
            startText=smallFont.render("start", 1, GREEN)
            startTextWidth, startTextHeight=smallFont.size("start")
            displaySurf.blit(startText, (self.start.x-int(startTextWidth/2), self.start.y-20-int(startTextHeight/2)))
            if self.playerShip.mineralCount>=self.requiredMinerals: finishText=smallFont.render("finish", 1, PURPLE)
            else: finishText=smallFont.render("finish", 1, fadedPurpleColor)
            finishTextWidth, finishTextHeight=smallFont.size("finish")
            displaySurf.blit(finishText, (self.finish.x-int(finishTextWidth/2), self.finish.y-20-int(finishTextHeight/2)))
            displaySurf.blit(textMinerals, (10,10))
            displaySurf.blit(textFuel, (590,10))

            #if death happend wait for 40 frames to show explosion animation
            if self.deathClock>0:
                if self.deathClock>=40:
                    if self.gameMode.name=='campaign': self.changeMode(deathMode)
                    elif self.gameMode.name=='training': self.changeMode(trDeathMode)
                    elif self.gameMode.name=='random level': self.changeMode(finishRandomMode)
                    self.deathClock=0
                else: self.deathClock+=1

            #if finish happend wait for 40 frames to show explosion animation
            if self.finishClock>0:
                if self.finishClock>=40:
                    if self.gameMode.name=='campaign': self.changeMode(finishMode)
                    elif self.gameMode.name=='training': self.changeMode(trFinishMode)
                    elif self.gameMode.name=='random level': self.changeMode(finishRandomMode)
                    self.finishClock=0
                else: self.finishClock+=1
            
            #if game is paused draw labeles for pause and and cover semitransperant surface
            if self.paused:
                coverSurface=pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
                coverSurface.set_alpha(100)
                displaySurf.blit(coverSurface, (0,0))
                for l in self.pausedLabels:
                    l.draw(displaySurf)
                
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        elif self.gameMode.name=='death':
            displaySurf.blit(menuBackground, (0,0))
            headText=hugeFont.render("Your ship is crashed", 1, titleColor)
            headTextWidth, headTextHeight=hugeFont.size("Your ship is crashed")
            displaySurf.blit(headText, (400-int(headTextWidth/2), 230-int(headTextHeight/2)))
            #draw death menu
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='RETRY LEVEL':
                        self.currentLevel.load(self.currentLevel.number)
                        self.changeMode(campaignMode)                        
                    elif b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                        f=open("currentLevel", 'r+')
                        f.write("%d\n" %self.currentLevel.number)
                        f.close()
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        elif self.gameMode.name=='training death':
            displaySurf.blit(menuBackground, (0,0))
            headText=hugeFont.render("Your ship is crashed", 1, titleColor)
            headTextWidth, headTextHeight=hugeFont.size("Your ship is crashed")
            displaySurf.blit(headText, (400-int(headTextWidth/2), 230-int(headTextHeight/2)))
            #draw death menu
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='RETRY LEVEL':
                        self.currentLevel.load(self.currentLevel.number, 'training')
                        self.changeMode(trainingMode)                        
                    elif b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        elif self.gameMode.name=='finish':
            displaySurf.blit(menuBackground, (0,0))
            headText=hugeFont.render("Mission accomplished", 1, titleColor)
            headTextWidth, headTextHeight=hugeFont.size("Mission accomplished")
            displaySurf.blit(headText, (400-int(headTextWidth/2), 230-int(headTextHeight/2)))
            #draw death menu
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='RETRY LEVEL':
                        self.currentLevel.load(self.currentLevel.number)
                        self.changeMode(campaignMode)                        
                    elif b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                        f=open("currentLevel", 'r+')
                        f.write("%d\n" %self.currentLevel.number)
                        f.close()
                    elif b.text=='NEXT LEVEL':
                        self.currentLevel.load(self.currentLevel.number+1)
                        self.changeMode(campaignMode)
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            
        elif self.gameMode.name=='training finish':
            displaySurf.blit(menuBackground, (0,0))
            headText=hugeFont.render("Mission accomplished", 1, titleColor)
            headTextWidth, headTextHeight=hugeFont.size("Mission accomplished")
            displaySurf.blit(headText, (400-int(headTextWidth/2), 230-int(headTextHeight/2)))
            #draw death menu
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='RETRY LEVEL':
                        self.currentLevel.load(self.currentLevel.number, 'training')
                        self.changeMode(trainingMode)                        
                    elif b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                    elif b.text=='NEXT LEVEL':
                        self.currentLevel.load(self.currentLevel.number+1, 'training')
                        self.changeMode(trainingMode)
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        elif self.gameMode.name=='finish random':
            displaySurf.blit(menuBackground, (0,0))
            headText=hugeFont.render("Mission accomplished", 1, titleColor)
            headTextWidth, headTextHeight=hugeFont.size("Mission accomplished")
            displaySurf.blit(headText, (400-int(headTextWidth/2), 230-int(headTextHeight/2)))
            #draw death menu
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='NEW RANDOM MAP':
                        randomLevelMode=mode('random level', [])
                        self.currentLevel.getRandom()
                        self.changeMode(randomLevelMode)
                    elif b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                    elif b.text=='RETRY LEVEL':
                        randomLevelMode=mode('random level', [])
                        self.changeMode(randomLevelMode)
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        elif self.gameMode.name=='help':
            displaySurf.blit(helpPageImg, (0,0))
            #draw help page
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        elif self.gameMode.name=='win':
            displaySurf.blit(menuBackground, (0,0))
            headText1=hugeFont.render("You accomplished all the missions", 1, titleColor)
            headTextWidth1, headTextHeight1=hugeFont.size("You accomplished all the missions")
            displaySurf.blit(headText1, (400-int(headTextWidth1/2), 170-int(headTextHeight1/2)))
            headText2=hugeFont.render("Congratulations", 1, titleColor)
            headTextWidth2, headTextHeight2=hugeFont.size("Congratulations")
            displaySurf.blit(headText2, (400-int(headTextWidth2/2), 230-int(headTextHeight2/2)))
            #draw help page
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:
                    if b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        elif self.gameMode.name=='training win':
            displaySurf.blit(menuBackground, (0,0))
            headText1=hugeFont.render("You accomplished the training", 1, titleColor)
            headTextWidth1, headTextHeight1=hugeFont.size("You accomplished the training")
            displaySurf.blit(headText1, (400-int(headTextWidth1/2), 170-int(headTextHeight1/2)))
            headText2=hugeFont.render("Move to the campaign", 1, titleColor)
            headTextWidth2, headTextHeight2=hugeFont.size("Move to the campaign")
            displaySurf.blit(headText2, (400-int(headTextWidth2/2), 230-int(headTextHeight2/2)))
            #draw death menu
            for b in self.gameMode.buttons:
                b.update(displaySurf, self.mousePressed)
                #??if any button pressed - change game mode accordingly
                if b.buttonPressed==True:           
                    if b.text=='MAIN MENU':
                        self.changeMode(mainMenuMode)
                    elif b.text=='CAMPAIGN':
                        self.currentLevel=level(1)
                        self.changeMode(campaignMode)
                    b.buttonPressed=False
                    self.mousePressed=(0,0)                   
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            
            
    def changeMode(self, nextMode):
        global campaignMode
        global randomLevelMode
        if nextMode.name=='campaign':
            if not self.currentLevel.winSituation:
                campaignMode=mode('campaign', [])
                #set planets and other objects form level
                self.planetarySystem=self.currentLevel.planetarySystem
                self.asteroidBelt=self.currentLevel.asteroidBelt
                self.tailGroup=self.currentLevel.tailGroup
                self.startGroup=self.currentLevel.startGroup
                self.finishGroup=self.currentLevel.finishGroup
                self.asteroidSpawnPoints=self.currentLevel.asteroidSpawnPoints
                self.plasmaShots=self.currentLevel.plasmaShots
                self.explosionGroup=self.currentLevel.explosionGroup
                self.start=self.currentLevel.start
                self.finish=self.currentLevel.finish
                #set group of minerls sprites
                self.minerals=self.currentLevel.minerals
                self.requiredMinerals=self.currentLevel.requiredMinerals
                self.pausedLabels=self.currentLevel.pausedLabels
                #create gravity field
                self.levelGravity=gravityField(self.planetarySystem)
                #set player's ship
                self.playerShip = battleShip(self.start)
                self.ships=pygame.sprite.Group()
                self.ships.add(self.playerShip)
                self.gameMode=campaignMode
            else:
                self.gameMode=winMenuMode
        elif nextMode.name=='training':
            if not self.currentLevel.trWinSituation:
                self.planetarySystem=self.currentLevel.planetarySystem
                self.asteroidBelt=self.currentLevel.asteroidBelt
                self.tailGroup=self.currentLevel.tailGroup
                self.startGroup=self.currentLevel.startGroup
                self.finishGroup=self.currentLevel.finishGroup
                self.asteroidSpawnPoints=self.currentLevel.asteroidSpawnPoints
                self.plasmaShots=self.currentLevel.plasmaShots
                self.explosionGroup=self.currentLevel.explosionGroup
                self.start=self.currentLevel.start
                self.finish=self.currentLevel.finish
                #set group of minerls sprites
                self.minerals=self.currentLevel.minerals
                self.requiredMinerals=self.currentLevel.requiredMinerals
                self.pausedLabels=self.currentLevel.pausedLabels
                #create gravity field
                self.levelGravity=gravityField(self.planetarySystem)
                #set player's ship
                self.playerShip = battleShip(self.currentLevel.start)
                self.ships=pygame.sprite.Group()
                self.ships.add(self.playerShip)
                self.paused=True
                self.gameMode=trainingMode
            else:
                self.gameMode=trWinMenuMode
        elif nextMode.name=='death':
            self.gameMode=deathMode
        elif nextMode.name=='training death':
            self.gameMode=trDeathMode
        elif nextMode.name=='training finish':
            self.gameMode=trFinishMode
        elif nextMode.name=='main menu':
            self.gameMode=mainMenuMode
        elif nextMode.name=='finish':
            self.gameMode=finishMode
        elif nextMode.name=='help':
            self.gameMode=helpPageMode
        elif nextMode.name=='random level':
            #set planets and other objects form level
            self.planetarySystem=self.currentLevel.planetarySystem
            self.asteroidBelt=self.currentLevel.asteroidBelt
            self.tailGroup=self.currentLevel.tailGroup
            self.startGroup=self.currentLevel.startGroup
            self.finishGroup=self.currentLevel.finishGroup
            self.asteroidSpawnPoints=self.currentLevel.asteroidSpawnPoints
            self.plasmaShots=self.currentLevel.plasmaShots
            self.explosionGroup=self.currentLevel.explosionGroup
            self.start=self.currentLevel.start
            self.finish=self.currentLevel.finish
            #set group of minerls sprites
            self.minerals=self.currentLevel.minerals
            self.requiredMinerals=0
            self.pausedLabels=self.currentLevel.pausedLabels
            #create gravity field
            self.levelGravity=gravityField(self.planetarySystem)
            #set player's ship
            self.playerShip = battleShip(self.currentLevel.start)
            self.ships=pygame.sprite.Group()
            self.ships.add(self.playerShip)
            #set group of minerls sprites
            self.minerals=pygame.sprite.Group()
            self.gameMode=randomLevelMode
        elif nextMode.name=='finish random':
            self.gameMode=finishRandomMode

  
#construct main menu mode
mainMenuButtons=[]
mainMenuButtons.append(button((400, 300), buttonImg, buttonPressedImg, 'NEW CAMPAIGN'))
mainMenuButtons.append(button((400, 350), buttonImg, buttonPressedImg, 'RESUME CAMPAIGN'))
mainMenuButtons.append(button((400, 400), buttonImg, buttonPressedImg, 'HOW TO PLAY'))
mainMenuButtons.append(button((400, 450), buttonImg, buttonPressedImg, 'RANDOM MAP'))
mainMenuButtons.append(button((400, 500), buttonImg, buttonPressedImg, 'HELP'))
mainMenuButtons.append(button((400, 550), buttonImg, buttonPressedImg, 'EXIT'))

mainMenuMode=mode('main menu', mainMenuButtons)

#construct campaign mode
campaignMode=mode('campaign', [])

#construct random level mode
randomLevelMode=mode('random level', [])

#construct training mode
trainingMode=mode('training', [])

#construct death menu mode
deathModeButtons=[]
deathModeButtons.append(button((400, 450), buttonImg, buttonPressedImg, 'RETRY LEVEL'))
deathModeButtons.append(button((400, 510), buttonImg, buttonPressedImg, 'MAIN MENU'))
deathMode=mode('death', deathModeButtons)

#construct death in training menu mode
trDeathModeButtons=[]
trDeathModeButtons.append(button((400, 450), buttonImg, buttonPressedImg, 'RETRY LEVEL'))
trDeathModeButtons.append(button((400, 510), buttonImg, buttonPressedImg, 'MAIN MENU'))
trDeathMode=mode('training death', trDeathModeButtons)

#construct finish menu mode
finishMenuButtons=[]
finishMenuButtons.append(button((400, 420), buttonImg, buttonPressedImg, 'NEXT LEVEL'))
finishMenuButtons.append(button((400, 480), buttonImg, buttonPressedImg, 'RETRY LEVEL'))
finishMenuButtons.append(button((400, 540), buttonImg, buttonPressedImg, 'MAIN MENU'))
finishMode=mode('finish', finishMenuButtons)

#construct training finish menu mode
trFinishMenuButtons=[]
trFinishMenuButtons.append(button((400, 420), buttonImg, buttonPressedImg, 'NEXT LEVEL'))
trFinishMenuButtons.append(button((400, 480), buttonImg, buttonPressedImg, 'RETRY LEVEL'))
trFinishMenuButtons.append(button((400, 540), buttonImg, buttonPressedImg, 'MAIN MENU'))
trFinishMode=mode('training finish', trFinishMenuButtons)

#construct finish random level mode
finishRandomButtons=[]
finishRandomButtons.append(button((400, 420), buttonImg, buttonPressedImg, 'NEW RANDOM MAP'))
finishRandomButtons.append(button((400, 480), buttonImg, buttonPressedImg, 'RETRY LEVEL'))
finishRandomButtons.append(button((400, 540), buttonImg, buttonPressedImg, 'MAIN MENU'))
finishRandomMode=mode('finish random', finishRandomButtons)

#construct help page
helpPageButtons=[]
helpPageButtons.append(button((400, 540), buttonImg, buttonPressedImg, 'MAIN MENU'))
helpPageMode=mode('help', helpPageButtons)

#construct win menu mode
winButtons=[]
winButtons.append(button((400, 540), buttonImg, buttonPressedImg, 'MAIN MENU'))
winMenuMode=mode('win', winButtons)

#construct training win menu mode
trWinButtons=[]
trWinButtons.append(button((400, 480), buttonImg, buttonPressedImg, 'CAMPAIGN'))
trWinButtons.append(button((400, 540), buttonImg, buttonPressedImg, 'MAIN MENU'))
trWinMenuMode=mode('training win', trWinButtons)


def main():

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.set_colorkey(WHITE)
    pygame.display.update()

    spaceGame=game(mainMenuMode)
    keyInputHandler=inputHandler()
    previousKeys=pygame.key.get_pressed()

 
    while True:

        spaceGame.update(DISPLAYSURF)

        keys=pygame.key.get_pressed()

        keyInputHandler.update(keys, previousKeys, spaceGame)

        previousKeys=keys

if __name__== '__main__':
    main()
