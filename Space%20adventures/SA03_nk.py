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

#sides of square of the ship
shipHeight = 20
shipWidth = 10

#speed of plasma shots of foe planets
plasmaSpeed=5.0

#max speed of asteroids inside catcher
maxInCatcherSpeed=5.0

#speed of catcher's push
speedCatcherPush=5.0

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

    def __hash__(self):
        return hash((self.x, self.y))

    def valueVec(self):
        return (self.x, self.y)

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
    return math.sqrt(math.pow(vec.x, 2)+math.pow(vec.y, 2))

class battleShip(pygame.sprite.Sprite):
    def __init__(self, position=vector((0,0))): #take position as a vector in input
        pygame.sprite.Sprite.__init__(self)
        # defines initial position and speed characterictics of the battle ship
        self.position=position
        self.speed=vector((0, 0))
        self.acc=vector((0, 0))
        self.onOrbit=False
        self.trajectory=[]
        self.alive=True
        self.catcherRadius=40
        self.catcherOn=False
        self.asteroidCaught=None

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

        #calculate coordintes of asteroid catcher
        self.catcherCenter=vecSum(vector((math.cos(self.angle)*(shipHeight/2.0+self.catcherRadius), -math.sin(self.angle)*(shipHeight/2.0+self.catcherRadius))), self.position)

    def update(self, force, speedDelta, rotationDelta, asteroidBelt):
        if self.onOrbit==False:
            #update decartes position
            # first update position, then - speed and finally - acceleration
            self.position=vecSum(self.position,vecSum(multSc(deltaT, self.speed), multSc(math.pow(deltaT, 2)/2, force)))
            self.speed=vecSum(self.speed, vecSum(speedDelta, multSc(deltaT,force)))
            self.acc=force             
            #update rotation
            # first update angle, then rotation
            self.angle=self.angle+deltaT*self.rotation
            if self.angle>(2*math.pi): self.angle=self.angle%(2*math.pi)
            self.rotation=self.rotation+rotationDelta
            if self.rotation>(2*math.pi): self.rotation=self.rotation%(2*math.pi)
        else:
            #when ship moves on friendly's planet orbit speed and rotation are used in absolute terms
            self.position=vecSum(self.position, multSc(deltaT, speedDelta))
            self.speed=speedDelta
            self.angle=self.angle+deltaT*rotationDelta
            if self.angle>(2*math.pi): self.angle=self.angle%(2*math.pi)
            self.rotation=rotationDelta
            if self.rotation>(2*math.pi): self.rotation=self.rotation%(2*math.pi)

        #calculate caught asteroids movements and asteroid catch

        if self.asteroidCaught!=None and self.catcherOn==True:
            self.asteroidCatch(self.asteroidCaught)
        elif self.asteroidCaught!=None and self.catcherOn==False:
            self.asteroidPush(self.asteroidCaught)
            self.asteroidCaught=None
        elif self.asteroidCaught==None and self.catcherOn==True:
            distanceToNearest=self.catcherRadius
            for i in asteroidBelt:
                print (vecMag(vecDif(self.catcherCenter, i.position)))
                if vecMag(vecDif(self.catcherCenter, i.position))<distanceToNearest:
                    self.asteroidCaught=i
                    distanceToNearest=vecMag(vecDif(self.catcherCenter, i.position))
            if self.asteroidCaught==None:
                self.catcherOn=False
            else: self.asteroidCatch(self.asteroidCaught)           
           

        #calculate coordintes of asteroid catcher
        self.catcherCenter=vecSum(vector((math.cos(self.angle)*(shipHeight/2.0+self.catcherRadius), -math.sin(self.angle)*(shipHeight/2.0+self.catcherRadius))), self.position)

        #rotate ship

        self.rotSurf = pygame.transform.rotate(self.Surf, self.angle*radDegRatio-90)
        self.rotSurf.set_colorkey(BLACK)#?? delete this line?
        
        self.image=self.rotSurf
        self.rect=pygame.Rect(self.position.x-shipHeight/2, self.position.y-shipHeight/2, shipHeight, shipHeight)
        self.mask=pygame.mask.from_surface(self.rotSurf) #create mask for collision

        #check whether the ship is collided
        if self.alive==False:
            self.kill()

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
                              

    def respawn(self, respawnPoint, ships):
        self.position=respawnPoint
        self.speed=vector((0, 0))
        self.acc=vector((0, 0))
        self.angle=float(0) 
        self.rotation=float(0)
        self.rotationAcc=float(0)
        self.rect=pygame.Rect(respawnPoint.x-shipHeight/2, respawnPoint.y-shipHeight/2, shipHeight, shipHeight)
        ships.add(self)
        return True
        

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

    def update(self, other, plasmaGroup):
        pygame.sprite.Sprite.update(self)

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

class frPlanet(planet):
    def __init__(self, mass, color, position):
        planet.__init__(self, mass, color, position)
        #set friendly planet orbit on planets radius plus 20
        self.orbitRadius=float(mass+20)
        #define speed of ship on the orbit in number of turns over planet in one frame
        self.orbitalSpeed=1.0/(5.0*FPS)
        #self.surf=pygame.Surface((2*int(self.orbit), 2*int(self.orbit))) #surface of the planet with orbit
        #pygame.draw.circle(self.surf, GREEN, (int(self.orbit),int(self.orbit)), int(self.orbit), 5)#draw a the orbit on planets' surface in center of the surface
        #self.rect = pygame.Rect(position.x-int(self.orbit), position.y-int(self.orbit), 2*int(self.orbit), 2*int(self.orbit)) # orbit's radius is subtracted to use position as a center
        self.orbit=[]
        self.shipDirections={}
        alpha=0
        for i in range(int(5.0*FPS)):
            x=self.position.x+int(self.orbitRadius*math.cos(alpha))
            y=self.position.y-int(self.orbitRadius*math.sin(alpha))
            try:
                if self.orbit[len(self.orbit)-1]!=(x, y):
                    self.orbit.append((x, y))               
                    self.shipDirections[(x,y)]=0.5*math.pi+alpha
            except:
                self.orbit.append((self.position.x+int(self.orbitRadius), self.position.y))
                self.shipDirections[(self.position.x+int(self.orbitRadius), self.position.y)]=0.5*math.pi
            alpha+=2.0*math.pi/(5.0*FPS)

    def takeOnOrbit(self, other):
        if isinstance(other, battleShip):
            #max speed of ship rotation in radians
            maxShipRot=2.0*math.pi/(4.5*FPS)
            #average speed of ship roration in radians
            avShipRot=2.0*math.pi*self.orbitalSpeed
            deltaAngle=0.0
            other.onOrbit=True
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
                   
            #calculate angular speed
            if other.angle!=self.shipDirections[self.orbit[nextPoint]]:
                if abs(other.angle-self.shipDirections[self.orbit[nextPoint]])>avShipRot:
                    deltaAngle=-maxShipRot*abs(other.angle-self.shipDirections[self.orbit[nextPoint]])/(other.angle-self.shipDirections[self.orbit[nextPoint]])
                else:
                    deltaAngle=self.shipDirections[self.orbit[nextPoint]]-other.angle
            return [xSpeed, ySpeed, deltaAngle]

class foePlanet(planet):
    def __init__(self, mass, color, position, fireRadius):
        planet.__init__(self, mass, color, position)
        #set fire radius
        self.fireRadius=fireRadius
        #set shot interval as internal constant
        self.shotInterval=3*FPS
        self.timeFromLastShot=self.shotInterval

    def update(self, other, plasmaGroup):
        planet.update(self, other, plasmaGroup)
        if self.timeFromLastShot<self.shotInterval: self.timeFromLastShot+=1
        #here foe planet shoots in player when it is close and planet is ready
        if vecMag(vecDif(self.position, other.position))<=(self.fireRadius+self.mass) and self.timeFromLastShot==self.shotInterval and isinstance(other, battleShip) and other.alive==True:
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
    def __init__(self, position, speed): #position defines center of the planet and has to ba a vector
        pygame.sprite.Sprite.__init__(self)
        # set position and speed of the plasma shot
        self.position=position
        self.speed=speed

        #set initial image of the asteroid
        self.surf=pygame.Surface((4, 4)) 
        pygame.draw.circle(self.surf, RED, (2,2), 2)
        self.surf.set_colorkey(BLACK) 
        self.image=self.surf
        self.mask=pygame.mask.from_surface(self.surf) #create mask for collision
        self.rect = pygame.Rect(position.x-2, position.y-2, 4, 4)

    def update(self, liveState):
        #update decartes position
        # first update position, then - speed 
        self.position=vecSum(self.position,multSc(deltaT, self.speed))              
                
        #update image
        self.rect=pygame.Rect(self.position.x-2, self.position.y-2, 4, 4)

        #check whether the ship is collided
        if liveState==False: self.kill()

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        #?? here should call for explosion animation
       
class asteroidSpawnSpot():
    def __init__(self, position, velocity, interval):
        self.position=position #position of the asteroid spawn spot
        self.velocity=velocity #speed of the asteroids from this particular spot
        self.interval=interval #interval asteroids respawn in frames
        self.internalFrames=0 #number of frames from last asteroid respawn

    def update(self, asteroidGroup):
        #check whetther it is time to shoot
        self.internalFrames+=1
        if self.internalFrames==self.interval:
            #spawn asteroid and number of frames from last asteroid respawn set to zero
            asteroidGroup.add(asteroid(self.position, self.velocity))
            self.internalFrames=0
        
        

def main():

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.set_colorkey(WHITE)
    pygame.display.update()

    #game modes setup
    possibleGameModes=('game', 'finish', 'death')
    curentGameMode=possibleGameModes[0]

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
    #planetarySystem.add(planet(30, RED, vector((100, 100))))
    planetarySystem.add(planet (40, BLUE, vector((400, 200))))
    planetarySystem.add(frPlanet (20, GREEN, vector((50, 280))))
    planetarySystem.add(planet (20, BLUE, vector((600, 500))))
    #planetarySystem.add(planet (20, BLUE, vector((500, 320))))
        

    #set asteroids
    asteroidBelt=pygame.sprite.Group()
    hary=asteroidSpawnSpot(vector((150, 5)), vector((1, 2)), 60)

    #set plasma
    plasmaShots=pygame.sprite.Group()
    plasmaShots.add(plasmaBall(vector((150, 5)), vector((5, 5))))

    #set a group of objects that are mortal and not player
    mortalNPC=pygame.sprite.Group()
    mortalNPC=asteroidBelt.copy()

    #the follwing boolean True on the first main loop, needed for trajectory calculation and draw
    #??need to make it more elegant
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
                if event.key==K_UP:#if up key pressed -
                    deltaSpeed=vecSum(deltaSpeed, vector((engine*math.cos(playerShip.angle), -engine*math.sin(playerShip.angle))))#right engine works and ship moves forward
                    rightEngine=True
                    leftEngine=True
                    playerShip.onOrbit=False

                elif event.key==K_a:#if 'a' key pressed -
                    deltaRot=deltaRot-engine*rotIner# left shunting engine is on and ship slightly rotates clockwise
                    leftShuntingEngine=True

                elif event.key==K_s:#if 's' key pressed -
                    deltaRot=deltaRot+engine*rotIner# right shunting engine is on and ship slightly rotates counter-clockwise
                    rightShuntingEngine=True

                elif event.key==K_SPACE:
                    #if space is pushed asteroid catcher is on
                    playerShip.catcherOn=not playerShip.catcherOn
                              
        
        #calculate gravity force for player's ship
        for i in planetarySystem.sprites():
            planetVec=i.position
            gravityVec=vector(((planetVec.x-playerShip.position.x), (planetVec.y-playerShip.position.y))) #define vector connecting planet and player's ship
            distance=vecMag(gravityVec)
            iGravityX=i.mass*gConstant*math.pow(distance, -3)*gravityVec.x #calculate x coordinate of planet i gravity
            iGravityY=i.mass*gConstant*math.pow(distance, -3)*gravityVec.y #calculate y coordinate of planet i gravity
            gravity=vecSum(gravity, vector((iGravityX, iGravityY)))
            #for friendly planets check that player is on the orbit
            if isinstance(i, frPlanet):
                if distance<(i.orbitRadius-1.0) or playerShip.onOrbit==True:                    
                    if leftEngine==False and rightEngine==False:
                        xSpeed, ySpeed, angleSpeed =i.takeOnOrbit(playerShip)
                        deltaSpeed=vector((xSpeed, ySpeed))
                        deltaRot=angleSpeed

        #asteroids position and collision check
        for ast in asteroidBelt.sprites():
            astGravity=vector((0, 0))
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
                playerShip.alive=False
                astAlive=False
                DISPLAYSURF.blit(myfont.render("Killed!!!", 1, RED), (100, 180)) #killed situation
                DISPLAYSURF.blit(myfont.render("continue? Y/N", 1, RED), (100, 200)) #continue or not?
                #wait for player is ready to continue
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key==K_y:
                            playerShip.alive=playerShip.respawn(start, ships)
                        elif event.key==K_n:
                            pygame.quit()
                            sys.exit()
            ast.update(astGravity, astAlive)
        
        #plasma shots collision check
        for shot in plasmaShots.sprites():
            shotAlive=True
            if pygame.sprite.collide_mask(shot, playerShip)!=None:
                playerShip.alive=False
                shotAlive=False
                DISPLAYSURF.blit(myfont.render("Killed!!!", 1, RED), (100, 180)) #killed situation
                DISPLAYSURF.blit(myfont.render("continue? Y/N", 1, RED), (100, 200)) #continue or not?
                #wait for player is ready to continue
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key==K_y:
                            playerShip.alive=playerShip.respawn(start, ships)
                        elif event.key==K_n:
                            pygame.quit()
                            sys.exit()
            shot.update(shotAlive)
                            
        #player collision with planet check
        for i in planetarySystem:
            if pygame.sprite.collide_mask(i, playerShip)!=None:
                playerShip.alive=False
                DISPLAYSURF.blit(myfont.render("Killed!!!", 1, RED), (100, 180)) #killed situation
                DISPLAYSURF.blit(myfont.render("continue? Y/N", 1, RED), (100, 200)) #continue or not?
                #wait for player is ready to continue
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key==K_y:
                            playerShip.alive=playerShip.respawn(start, ships)
                        elif event.key==K_n:
                            pygame.quit()
                            sys.exit()
                        
            

        #finish check
        for i in finishGroup:
            if pygame.sprite.collide_mask(i, playerShip)!=None:
                playerShip.alive=False
                DISPLAYSURF.blit(myfont.render("Finish!!!", 1, GREEN), (100, 180)) #finish situation
                DISPLAYSURF.blit(myfont.render("continue? Y/N", 1, RED), (100, 200)) #continue or not?
                #wait for player is ready to continue
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key==K_y:
                            playerShip.alive=playerShip.respawn(start, ships)
                        elif event.key==K_n:
                            pygame.quit()
                            sys.exit()

        # border check
        if playerShip.position.x>=800 or playerShip.position.y>=600 or playerShip.position.x<=0 or playerShip.position.y<=0:
            playerShip.alive=False
            DISPLAYSURF.blit(myfont.render("Killed!!!", 1, RED), (100, 180)) #killed situation
            DISPLAYSURF.blit(myfont.render("continue? Y/N", 1, RED), (100, 200)) #continue or not?
            #wait for player is ready to continue
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key==K_y:
                        playerShip.alive=playerShip.respawn(start, ships)
                    elif event.key==K_n:
                        pygame.quit()
                        sys.exit()
            
        
        # draw the ship with engine flames
        playerShip.engineFlames(leftEngine, leftShuntingEngine, rightShuntingEngine, rightEngine)
        ships.update(gravity, deltaSpeed, deltaRot, asteroidBelt)
        #throw away used point in trajectory
        if not firstLoop:
            if playerShip.trajectory!=[]: playerShip.trajectory.pop(0)

        #draw the trajectory calculate only if it is changed
        if playerShip.onOrbit==False and playerShip.alive==True:
            if deltaSpeed!=vector((0,0)) or firstLoop==True:
                playerShip.trajectory=calcTrajectory(playerShip.position, playerShip.speed, planetarySystem, finishGroup)
                firstLoop=False          
            for i in playerShip.trajectory: pygame.draw.circle(DISPLAYSURF, RED, (int(i.x), int(i.y)), 0)

        #update asteroids
        hary.update(asteroidBelt)

        #update planetary system
        planetarySystem.update(playerShip, plasmaShots)
              
        ships.draw(DISPLAYSURF)
        planetarySystem.draw(DISPLAYSURF)
        asteroidBelt.draw(DISPLAYSURF)
        plasmaShots.draw(DISPLAYSURF)
        startGroup.draw(DISPLAYSURF)
        finishGroup.draw(DISPLAYSURF)

        #draw supplementary lines
        pygame.draw.circle(DISPLAYSURF, BLUE, (int(playerShip.catcherCenter.x), int(playerShip.catcherCenter.y)), 0)
        pygame.draw.circle(DISPLAYSURF, BLUE, (int(playerShip.catcherCenter.x), int(playerShip.catcherCenter.y)), int(playerShip.catcherRadius), 1)


        # module to see ship's movement characteristics
        textAngle=myfont.render("Angle %f" %playerShip.angle, 1, RED) # text of current angle
        textAcc=myfont.render("angle to planet %f" %((400.0 - playerShip.position.x)/60.0), 1, RED) # text of current angle to planet
        textSpeed=myfont.render("Speed %f, %f" %(playerShip.speed.x, playerShip.speed.y), 1, RED) #text of current speed
        textPosition=myfont.render("Position %f, %f" %(playerShip.position.x, playerShip.position.y), 1, RED) #text of current position

        DISPLAYSURF.blit(textAngle, (100, 100))
        DISPLAYSURF.blit(textAcc, (100, 120))
        DISPLAYSURF.blit(textSpeed, (100, 140))
        DISPLAYSURF.blit(textPosition, (100, 160))
             
        pygame.display.update()
        FPSCLOCK.tick(FPS)

       

if __name__== '__main__':
    main()
