import pygame, math
from gameutils import *
import vector
from collections import defaultdict

pygame.init()

scale = 4
allImages = {}


airParticles = pygame.sprite.Group()
groundParticles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
tanks = pygame.sprite.Group()

bulletMask = pygame.sprite.GroupSingle()
tankMask = pygame.sprite.GroupSingle()

bgRect = None
def reset():
    airParticles.empty()
    groundParticles.empty()
    bullets.empty()
    tanks.empty()

class Tank(pygame.sprite.Sprite):
    baseSpeed = 40
    baseTurnSpeed = 180
    baseAimSpeed = 90
    baseHealth = 3
    directions = 16
    def __init__(self,pos,hue):
        pygame.sprite.Sprite.__init__(self)

        self.direction = 90
        self.clippedDirection = 90
        self.aim = 90
        self.trackFrame = [0,0]
        self.image = pygame.Surface(scalePx((16,16),scale),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hue = hue
        self.accuratePos = pos
        self.velocity = vector.Vec(0,0)
        self.accuratePos = pos

        self.sPassed = 0

        self.health = self.baseHealth
        self.turnSpeed = self.baseTurnSpeed

        self.images = {
            "body": pygame.transform.scale(hsvHue(loadImage("tankbody.png",allImages).convert_alpha(),hue),scalePx((16,16),scale)),
            "track": loadImage("tanktrack.png",allImages,scale=scale).convert(),
            "barrel": loadImage("tankbarrel.png",allImages,scale=scale).convert_alpha(),
            "bullet": pygame.transform.scale(hsvHue(loadImage("bullet.png",allImages).convert_alpha(),hue),scalePx((12,4),scale//2))
        }

        self.cooldown = defaultdict(int,{"fire":0,"animTrack":0,"trackParticle":0})

        self.mask = pygame.mask.from_surface(self.image)
        self.build()
        self.tasks = []

        self.change = 0
        self.rebuild = True

    def build(self):
        base = pygame.Surface(scalePx((16,16),scale),pygame.SRCALPHA)
        base.blit(self.images["track"], scalePx((2, 3), scale),
                  area=scalePx((0, 2*(self.trackFrame[0]%3), 12, 2), scale))
        base.blit(self.images["track"], scalePx((2, 11), scale),
                  area=scalePx((0, 2*(self.trackFrame[1]%3), 12, 2), scale))
        base.blit(self.images["body"], (0, 0))

        base = pygame.transform.rotate(base,self.clippedDirection)
        baseRect = base.get_rect()
        baseRect.topleft = ((baseRect.width-self.rect.width)/-2,(baseRect.height-self.rect.height)/-2)

        barrel = pygame.transform.rotate(self.images["barrel"],self.aim)
        barrelRect = barrel.get_rect()
        barrelRect.topleft = ((barrelRect.width - self.rect.width) / -2, (barrelRect.height - self.rect.height) / -2)
        self.image.fill((0,0,0,0))
        self.image.blit(base,baseRect)
        self.mask = pygame.mask.from_surface(self.image)
        self.image.blit(barrel,barrelRect)

    def moveTrack(self,left,right):
        if not self.cooldown["animTrack"]:
            self.trackFrame[0] += left
            self.trackFrame[1] += right
            self.cooldown["animTrack"] = 100

    def interact(self,toDo):
        if not self.cooldown[toDo]:
            self.tasks.append(toDo)

    def handleTasks(self,ms):
        self.rebuild = False
        while len(self.tasks) > 0:
            self.rebuild = True
            task = self.tasks.pop(0)
            if task == "forward":
                self.velocity.angle = self.clippedDirection
                self.velocity.magnitude(self.baseSpeed)
                self.moveTrack(-1,-1)
            elif task == "back":
                self.velocity.angle = self.clippedDirection
                self.velocity.magnitude(-1*self.baseSpeed)
                self.moveTrack(1, 1)
            elif task == "turnLeft":
                change = self.baseTurnSpeed*(ms/1000)
                self.updateRot(change)

            elif task == "turnRight":
                change = -1 *self.baseTurnSpeed * (ms / 1000)
                self.updateRot(change)
            elif task == "aimLeft":
                change = self.baseAimSpeed * (ms / 1000)
                self.aim += change
            elif task == "aimRight":
                change = self.baseAimSpeed * (ms / 1000)
                self.aim -= change
            elif task == "fire":
                bullets.add(Bullet(self.images["bullet"],self.aim,
                                   addTuple(self.rect.center,trigOffset(scale*9,self.aim)),self.baseSpeed*1.5,self))
                self.cooldown[task] = 500

            if (task in ("forward", "back")) and not self.cooldown["trackParticle"]:
                groundParticles.add(simpleParticle(self.rect.center, "particletrack", 2000, self.direction))
                self.cooldown["trackParticle"] = 150

    def clipDirection(self,angle):
        spread = 360/self.directions
        angle = angle+spread/2

        for i in range(self.directions):
            angles = (i * spread, i * spread + spread)
            if angle % 360 >= min(angles) and angle % 360 <= max(angles):
                return (spread * i)

    def drawHealthBar(self):
        color = hsvRGB(127*((self.health-1)/(self.baseHealth-1))%128,100,100)
        fullRect = pygame.Rect(0, 4*scale, 12 * scale, 4)
        partialRect = pygame.Rect(0, 4*scale, (12 / self.baseHealth) * self.health * scale, 4)
        fullRect.centerx = self.image.get_width()/2
        partialRect.left = fullRect.left
        pygame.draw.rect(self.image, (0,0,0,255), fullRect, 4)
        pygame.draw.rect(self.image, color, partialRect)

    def updatePos(self,dx,dy):
        oldPos = self.accuratePos

        self.accuratePos = (self.accuratePos[0]+dx,self.accuratePos[1])
        self.rect.centerx = self.accuratePos[0]

        point = pygame.sprite.collide_mask(self,tankMask.sprite)
        tanksHit = pygame.sprite.spritecollide(self,tanks,False,pygame.sprite.collide_mask)
        halfSize = self.rect.width//2
        if point is not None or len(tanksHit)>1 or not contains(self.rect.centerx, bgRect.left+halfSize, bgRect.right-halfSize):
            self.rect.centerx = oldPos[0]
            self.accuratePos = (oldPos[0],self.accuratePos[1])

        self.accuratePos = (self.accuratePos[0],self.accuratePos[1]-dy)
        self.rect.centery = self.accuratePos[1]


        point = pygame.sprite.collide_mask(self, tankMask.sprite)
        tanksHit = pygame.sprite.spritecollide(self, tanks, False, pygame.sprite.collide_mask)
        if point is not None or len(tanksHit)>1 or not contains(self.rect.centery, bgRect.top+halfSize, bgRect.bottom-halfSize):
            self.rect.centery = oldPos[1]
            self.accuratePos = (self.accuratePos[0],oldPos[1])

    def updateRot(self, change):
        self.change = change
        self.direction += change
        self.aim += change
        self.clippedDirection = self.clipDirection(self.direction)
        if change > 0:
            self.moveTrack(1, -1)
        elif change < 0:
            self.moveTrack(-1, 1)

    def update(self,ms):
        self.velocity.x = 0
        self.velocity.y = 0

        self.handleTasks(ms)

        if self.rebuild:
            self.build()

            point = pygame.sprite.collide_mask(self, tankMask.sprite)
            tanksHit = pygame.sprite.spritecollide(self, tanks, False,
                                                   pygame.sprite.collide_mask)
            if point is not None or len(tanksHit) > 1:
                self.updateRot(self.change*-1)
                self.build()
        self.drawHealthBar()

        dx = self.velocity.x * (ms / 1000) * scale
        dy = self.velocity.y * (ms / 1000) * scale
        self.updatePos(dx,dy)

        if self.health <= 0:
            airParticles.add(Particle(self.rect.center, "explosion", 12,size = 2))
            self.kill()

        for movement in self.cooldown:
            if self.cooldown[movement] > 0:
                if ms > self.cooldown[movement]:
                    self.cooldown[movement] = 0
                else:
                    self.cooldown[movement] -= ms

class Bullet(pygame.sprite.Sprite):
    def __init__(self,image,dir,startPos,velocity,owner):
        pygame.sprite.Sprite.__init__(self)
        self.images = image
        self.image = pygame.transform.rotate(image,dir)
        self.rect = self.image.get_rect()
        self.startPos = addTuple(startPos,trigOffset(image.get_height(),dir))
        self.rect.center = startPos
        self.dir = dir
        self.velocity = velocity
        self.flightMs = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.owner = owner

    def update(self,ms):

        self.flightMs += ms

        dx = self.velocity * scale * math.cos(math.radians(self.dir)) * (self.flightMs / 1000)
        dy = self.velocity * scale * math.sin(math.radians(self.dir)) * (self.flightMs / 1000)
        self.rect.center = (self.startPos[0] + dx, self.startPos[1] - dy)

        if not bgRect.contains(self.rect):
            self.kill()

        collidedBullets = pygame.sprite.spritecollide(self, bullets, False)
        for sprite in collidedBullets:
            if sprite is not self:
                c = addTuple(self.rect.center,sprite.rect.center)
                c = (int(c[0]/2),int(c[1]/2))
                airParticles.add(Particle(c,"explosion",12,size = 0.5))
                sprite.kill()
                self.kill()

        collidedTanks = pygame.sprite.spritecollide(self, tanks, False, collided=pygame.sprite.collide_mask)
        for sprite in collidedTanks:
            if sprite is not self.owner:
                sprite.health -= 1
                if sprite.health > 0:
                    airParticles.add(Particle(addTuple(self.rect.center,trigOffset(self.images.get_width()//2,self.dir)), "explosion", 12, size=0.5))

                self.kill()

        collidedPoint = pygame.sprite.collide_mask(self,bulletMask.sprite)
        if collidedPoint is not None:
            airParticles.add(Particle(addTuple(self.rect.center,trigOffset(self.images.get_width()//2,self.dir)), "explosion", 12, size=0.5))
            self.kill()

class Particle(pygame.sprite.Sprite):
    def __init__(self,pos,type,framerate,rotation = 0,repeat = 1,size = 1):
        pygame.sprite.Sprite.__init__(self)
        self.base = loadImage(type+".png",allImages,scale = scale*size).convert_alpha()
        self.image = pygame.Surface((self.base.get_height(),self.base.get_height()),pygame.SRCALPHA)
        self.currentFrame = self.image
        self.frames = self.base.get_width()/self.base.get_height()
        self.rect = self.image.get_rect()
        self.framerate = framerate
        self.pos = pos
        self.timeAlive = 0
        self.repeat = repeat
        self.rotation = rotation

    def update(self,ms):
        self.timeAlive += ms
        frame = int((self.timeAlive/1000)*self.framerate)
        if frame == self.frames:
            frame = 0
            self.timeAlive = 0
            self.repeat -= 1
            if self.repeat == 0:
                self.kill()

        height = self.base.get_height()
        self.currentFrame.fill((0,0,0,0))
        self.currentFrame.blit(self.base,(0,0),(frame*height,0,height+frame*height,height))
        self.image = pygame.transform.rotate(self.currentFrame,self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

class simpleParticle(pygame.sprite.Sprite):
    def __init__(self,pos,type,lifeTime,rotation = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(loadImage(type+".png",allImages,scale = scale),rotation)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.timeAlive = 0
        self.lifeTime = lifeTime

    def update(self, ms):
        self.timeAlive += ms
        if self.timeAlive > self.lifeTime:
            self.kill()

class Mask(pygame.sprite.Sprite):
    def __init__(self,bgRect,mask):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(bgRect.size)
        self.rect = bgRect
        self.mask = mask