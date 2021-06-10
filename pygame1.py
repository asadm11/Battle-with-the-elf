# Importing necessary libraries
import pygame
from pygame import time, display, image

# Initialising the game engine
pygame.init()

# Setting the screen size and the title
win = display.set_mode((500, 500))
display.set_caption('Battle with the Elf')

# To manage the screen update speed
clock = time.Clock()

# For the background music
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)


# Loading the images of the player and the background image
Rightwalk = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
Leftwalk = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

# All code to draw and logic should be here
class Player():
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 5
        self.isjump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkcount = 0
        self.standing = True
        self.hitbox = (self.x + 15, self.y + 12, 35, 52)
    
    def draw(self, win):
        if self.walkcount + 1 >= 27:
            self.walkcount = 0
        if not(self.standing):
            if self.left:
                win.blit(Leftwalk[self.walkcount//3], (self.x,self.y))
                self.walkcount += 1
            elif self.right:
                win.blit(Rightwalk[self.walkcount//3], (self.x,self.y))
                self.walkcount +=1
        else:
            if self.left:
                win.blit(Leftwalk[0], (self.x, self.y))

            else:
                win.blit(Rightwalk[0], (self.x, self.y))
        self.hitbox = (self.x + 13, self.y + 10, 25, 50)

    def hit(self):
        self.isjump = False
        self.jump_count = 10
        self.x = 250
        self.y = 400
        self.walkcount = 0
        font1 = pygame.font.SysFont('comicsans', 80, 1, 1)
        text = font1.render('-5', 1, (255, 0, 0))
        # (text, anti-aliasing, color)
        win.blit(text, (250 - (text.get_width()/2), 250))
        display.update()
        i = 0
        if i < 300:
            time.delay(1000)  # Delays the game by 1 sec
            i += 1
        # self.hitbox = (self.x + 15, self.y + 12, 35, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        # display.update()


class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * self.facing
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy():
    Rightwalk = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    Leftwalk = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self, x, y, width, height, end, ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]      # horizontal starting and ending point of the elf
        self.walkcount = 0
        self.vel = 3
        self.hitbox = (self.x + 9, self.y + 1, 47, 63)
        self.health =  50
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 33:
                self.walkcount = 0
            if self.vel > 0:
                win.blit(self.Rightwalk[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
            else:
                win.blit(self.Leftwalk[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
            self.hitbox = (self.x + 7, self.y + 1, 40, 63)
            self.hitbox = (self.x + 9, self.y + 1, 47, 63)
            pygame.draw.rect(win, (0, 0, 255), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, self.health, 10))
        
       

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:    # so that the position is less than the end point
                self.x += self.vel
                self.vel += 0.01
            else:       # change the direction
                self.walkcount = 0
                self.vel = self.vel * -1
        else:
            if self.x + self.vel > self.path[0]:    # so that the position is greater than the leftmost pt
                self.x += self.vel
                self.vel -= 0.01
            else:
                self.walkcount = 0
                self.vel = self.vel * -1
    
    def hit(self):
        if self.health > 0:
            self.health -= 2
        else:
            self.visible = False

    def pl_hit(self):
        self.x = 0
        self.y = 400
        self.walkcount = 0
        
         

def boundary(x):
    if x > 440:
        x = 440 
    if x < 0:
        x = 0 
    return x 

def update_window():
    win.blit(bg, (0, 0))    # allows us to draw image to the screen
    text = font.render('Score: ' + str(score), 1, (255, 0, 0))
    win.blit(text, ((350, 15)))
    pl.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    en.draw(win)
    display.update()




# main loop
font = pygame.font.SysFont('monotype corsiva', 30, 1, 1)
# (font, size, bold, italics)
pl = Player(250, 400, 64, 64)
en = Enemy(0, 405, 64, 64, 430)
bullets = []
shootloop = 0
score = 0
run = True
while run:
    
    clock.tick(27)  # program will run at 27 fps
    keys = pygame.key.get_pressed() # returns the state of the keyboard
    # All of the event processes are below this comment
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False 
    
    if keys[pygame.K_LEFT]:
        pl.standing = False
        pl.x -= pl.vel
        pl.left = True
        pl.right = False
    elif keys[pygame.K_RIGHT]:
        pl.standing = False
        pl.x += pl.vel
        pl.right = True
        pl.left = False
    else:
        pl.standing = True
        pl.walkcount = 0
    
    if keys[pygame.K_UP]:
        pl.isjump = True
        
    if pl.isjump:    
        if pl.jump_count >= -10:
            neg = 1
            if pl.jump_count < 0:
                neg = -1
            pl.y -= (pl.jump_count ** 2) * 0.33 * neg
            pl.jump_count -= 1
        else:
            pl.isjump = False
            pl.jump_count = 10
    
    for bullet in bullets:
        if bullet.y - bullet.radius < en.hitbox[1] + en.hitbox[3] and bullet.y + bullet.radius > en.hitbox[1]:
            if bullet.x + bullet.radius > en.hitbox[0] and bullet.x - bullet.radius < en.hitbox[0] + en.hitbox[2]:
                score += 1
                en.hit()
                bullets.pop(bullets.index(bullet))  
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet)) # make the bullet disappear if it moves off the screen

    # to make the bullets not stick with each other
    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0
    
    if keys[pygame.K_SPACE] and shootloop == 0: 
        if pl.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:    # only 5 bullets can be displayed at the at a moment
            bullets.append(Projectile(round(pl.x + pl.width // 1.3), round(pl.y + (pl.height // 1.5)), 3, (0, 0, 200), facing))
                                                # (pos, radius, color, facing)
        shootloop = 1

    if en.visible:
        if pl.hitbox[1] + pl.hitbox[3] > en.hitbox[1] and pl.y - pl.hitbox[3] < en.hitbox[1] + en.hitbox[3]:
            if pl.hitbox[0] < en.hitbox[0] + en.hitbox[2] and pl.hitbox[0] + pl.hitbox[2] > en.hitbox[0]:
                score -= 5
                pl.hit()
                en.pl_hit()

    pl.x = boundary(pl.x)
    update_window() 

pygame.quit()