import pygame, sys, math
from pygame.locals import *

def collisionCheck (solid1,solid2):
    if solid1.hitbox[0] <= solid2.hitbox[0] <= solid1.hitbox[2] or solid1.hitbox[0] <= solid2.hitbox[2] <= solid1.hitbox[2] or solid2.hitbox[0] < solid1.hitbox[0] and solid1.hitbox[2] < solid2.hitbox[2]:
        if solid1.hitbox[1] <= solid2.hitbox[1] <= solid1.hitbox[3] or solid1.hitbox[1] <= solid2.hitbox[3] <= solid1.hitbox[3] or solid2.hitbox[1] < solid1.hitbox[1] and solid1.hitbox[3] < solid2.hitbox[3]:
            return True
    return False

def offscreenCheck (surface,solid):
    if solid.posx < 0 or solid.posy < 0:
        return True
    elif (solid.posx + solid.width) > surface.get_width() or (solid.posy + solid.height) > surface.get_height():
        return True
    else:
        return False
        
class Solid():
    def makeHitBox(self):
        return [self.posx,self.posy,self.posx + self.width,self.posy + self.height]
    
    def addVelx(self,v):
        self.velx += v

    def addVely(self,v):
        self.vely += v    

    def setImage(self,imageName):
        self.pic = pygame.image.load (imageName)

    def setBlock(self,colour):
        self.pic = pygame.Surface((self.width,self.height))
        self.pic.fill(colour)
    
    def __init__(self,x,y,w,h):
        #Position/Dimension Variables
        self.posx = x
        self.posy = y
        self.width = w
        self.height = h
        self.centerx = (2*self.posx + self.width)/2
        self.centery = (2*self.posy + self.height)/2
        self.hitbox = self.makeHitBox()
        #Active Properties Variables
        self.direction = 0
        self.velx = 0
        self.vely = 0

    def move(self):
        self.posx += self.velx
        self.posy += self.vely
        self.centerx = (2*self.posx + self.width)/2
        self.centery = (2*self.posy + self.height)/2
        self.hitbox = self.makeHitBox()

    def reverse(self):
        self.posx += -self.velx
        self.posy += -self.vely
        self.centerx = (2*self.posx + self.width)/2
        self.centery = (2*self.posy + self.height)/2
        self.hitbox = self.makeHitBox()
        
    def draw(self,surf):
        surf.blit (pygame.transform.rotate(self.pic,self.direction),(self.posx,self.posy))

    def collide(self):
        pass
        
class Avatar(Solid):
    
    def __init__(self,x,y,h,w):
        Solid.__init__(self,x,y,h,w)
        self.projectiles = []
        self.speed = 1
        self.projectileSpeed = 5
        self.ammo = 5
        
    def fire(self):
        if len(self.projectiles) <= 5:
            shot = Projectile(self.centerx-2,self.centery-3,4,6)
            self.projectiles.append(shot)
            shot.launch (self.projectileSpeed,self.direction)
            shot.setBlock ((255,0,0))
    
class Projectile(Solid):
    def launch (self,s,d):
        self.velx += s*math.cos(math.radians(d))
        self.vely += -s*math.sin(math.radians(d))
        
        
class Player():

    num = 1

    def __init__(self):
        self.key_up = ord ('w')
        self.key_down = ord ('s')
        self.key_right = ord ('d')
        self.key_left = ord ('a')
        self.key_fire = ord ('e')
        
        self.name = "Player " + str(Player.num)
        Player.num += 1

    def setControls(self,u,d,l,r,f):
        self.key_up = ord(u)
        self.key_down = ord(d)
        self.key_right = ord(r)
        self.key_left = ord(l)
        self.key_fire = ord(f)
        
    def setControlsDirect(self,u,d,l,r,f):
        self.key_up = u
        self.key_down = d
        self.key_right = r
        self.key_left = l
        self.key_fire = f
        
    def setAvatar(self,a):
        self.avatar = a
        
    def playerEvent(self,event):
        if event.type == KEYDOWN:
            if event.key == self.key_up:
                self.avatar.addVely(-self.avatar.speed)
                self.avatar.direction = 90
            elif event.key == self.key_down:
                self.avatar.addVely(self.avatar.speed)
                self.avatar.direction = 270
            elif event.key == self.key_right:
                self.avatar.addVelx(self.avatar.speed)
                self.avatar.direction = 0
            elif event.key == self.key_left:
                self.avatar.addVelx(-self.avatar.speed)
                self.avatar.direction = 180
            elif event.key == self.key_fire:
                self.avatar.fire()
        elif event.type == KEYUP:
            if event.key == self.key_up:
                self.avatar.addVely(self.avatar.speed)
            elif event.key == self.key_down:
                self.avatar.addVely(-self.avatar.speed)
            elif event.key == self.key_right:
                self.avatar.addVelx(-self.avatar.speed)    
            elif event.key == self.key_left:
                self.avatar.addVelx(self.avatar.speed)
    
def eventHandler(players):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        for p in players:
            p.playerEvent(event)
        
def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode ((1280,720))
    people = []
    for i in range (1,5):
        thing = Avatar(100*i,100*i,50,50)
        thing.setImage ("ship"+ str(i) +".png")
        play1 = Player()
        play1.setAvatar (thing)
        people.append(play1)

    people[1].setControls('y','h','g','j','u')
    people[2].setControls('p',';','l',"'",'[')
    people[3].setControlsDirect(K_UP,K_DOWN,K_LEFT,K_RIGHT,K_RCTRL)
    while True:
        DISPLAYSURF.fill ((100,160,255))
        eventHandler(people)
        
        for p in people:
            p.avatar.move()
            if offscreenCheck (DISPLAYSURF,p.avatar):
                p.avatar.reverse()
            else:
                for p2 in people:
                    if not (p == p2) and collisionCheck (p.avatar,p2.avatar):
                        p.avatar.reverse()
            
            for b in p.avatar.projectiles:
                b.move()
                if offscreenCheck (DISPLAYSURF,b):
                    p.avatar.projectiles.remove(b)
                else:
                    for p2 in people:
                        if not (p == p2) and collisionCheck (p2.avatar,b):
                            print"HIT"
                            p.avatar.projectiles.remove(b)
                            break
                            
        for p in people:
            p.avatar.draw(DISPLAYSURF)
            for b in p.avatar.projectiles:
                b.draw(DISPLAYSURF)
                
        pygame.display.update()
    


