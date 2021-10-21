import pygame
from pygame.locals import *
import sys
import random
import time
import pygame.freetype
 
pygame.init()
 
vec = pygame.math.Vector2 
HEIGHT = 500
WIDTH = 1000
ACC = 0.8
FRIC = -0.15
FPS = 60
floor = 30
jump = 7.5
bounce = 0.5
Gravity = 0.5

Status = 'Green'
GREEN = (0,200,0)
YELLOW = (240,255,0)
RED = (240,0,0)

green_init = 50
yellow_init = 80
yellow_count = yellow_init
yellow_var = 0.75
yellow_max = 100
green_count = green_init
green_var = 1
green_max = 100

global death, reset_time, reset_count
death = False
reset_count = 0
reset_time = 9000/FPS

FramePerSec = pygame.time.Clock()
GAME_FONT = pygame.freetype.SysFont('rockwell', 24)

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Light Green Light")

    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 60))
        self.surf.fill((0,150,165))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((25, HEIGHT- floor))
        self.vel = vec(0,0)
        self.acc = vec(0,Gravity)
        
 
    def move(self):
        if not death:
            self.acc = vec(0,Gravity)

            hits = pygame.sprite.spritecollide(P1 , platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = -self.vel.y*bounce

            pressed_keys = pygame.key.get_pressed()            
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.acc.x = -ACC
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.acc.x = ACC
            if pressed_keys[K_UP] or pressed_keys[K_w] or pressed_keys[K_SPACE]:
                ground = HEIGHT-floor+1
                if self.pos.y > ground-1 and self.pos.y < ground+1:
                    self.vel.y = -jump

            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            if self.pos.x > WIDTH:
                self.pos.x = WIDTH
            if self.pos.x < 0:
                self.pos.x = 0

            self.rect.midbottom = self.pos
        
        
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, floor))
        self.surf.fill((255,230,145))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - floor/2))

class lines(pygame.sprite.Sprite):
    def __init__(self, line_x_pos):
        super().__init__()
        self.surf = pygame.Surface((10, floor))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = (line_x_pos, HEIGHT-floor/2))

class timer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        h = 150
        w = 50
        self.surf = pygame.Surface((w, h))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center = (WIDTH-w/2, HEIGHT-floor-h/2))
        
    def update(self, status):
        if Status == 'Green':
            self.surf.fill(GREEN)            
            
        if Status == 'Yellow':
            self.surf.fill(YELLOW)
            
        if Status == 'Red':
            self.surf.fill(RED)
        


Ground = platform()
P1 = Player()
Timer = timer()
start_line = lines(55)
finish_line = lines(WIDTH-85)

platforms = pygame.sprite.Group()
platforms.add(Ground)
platforms.add(start_line)
platforms.add(finish_line)

all_sprites = pygame.sprite.Group()
all_sprites.add(Ground)
all_sprites.add(P1)
all_sprites.add(Timer)
all_sprites.add(start_line)
all_sprites.add(finish_line)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    displaysurface.fill((255,255,255))

    if Status == 'Green':
        green_count += random.uniform(0,green_var)
        if green_count > green_max:
            Status = 'Yellow'
            green_count = green_init
    if Status == 'Yellow':
        yellow_count += random.uniform(0,yellow_var)
        if yellow_count > yellow_max:
            Status = 'Red'
            yellow_count = yellow_init
    if Status =='Red':
        if abs(P1.vel.x) < 0.1 and abs(P1.vel.y - 0.33) < 0.1:
            reset_count += 1
        else:
            GAME_FONT.render_to(displaysurface, (WIDTH/2, HEIGHT/4),'Death!')
            death = True
            reset_count += 1
            
        if reset_count > reset_time:
            death = False
            reset_count = 0
            Status = 'Green'
            
            

    if abs(P1.vel.x) < 0.1 and abs(P1.pos.y - (HEIGHT-floor+1)) < 1:
        GAME_FONT.render_to(displaysurface, (WIDTH/2, HEIGHT/4),'Safe!')

    P1.move()
    Timer.update(Status)
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

