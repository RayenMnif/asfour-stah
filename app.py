import pygame
from random import randint
from sys import exit
from time import sleep

""" to do 
- add a working score
"""

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # animation
        frame_1 = pygame.image.load("sprites/yellowbird-upflap.png").convert_alpha()
        frame_2 = pygame.image.load("sprites/yellowbird-midflap.png").convert_alpha()
        frame_3 = pygame.image.load("sprites/yellowbird-downflap.png").convert_alpha()
        self.frames = [frame_1, frame_2, frame_3]
        self.animation_index = 0
        # gravity 
        self.gravity = 0
        # player 
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (140, 360)) 
    def animations(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def physics(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.top <= 490: self.gravity = -7 
    def update(self):
        global game_active 
        if game_active:
            self.physics()
            self.jump()
            if self.rect.y >= 450 : game_active = False
        if not game_active: self.rect.center = (140, 360)
        self.animations()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.image = pygame.image.load("sprites/pipe-green.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (randint(280, 350), randint(570, 700)))
        if type == "down":
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(center = (randint(280, 350), randint(-40, 20)))
    def update(self):
        self.rect.x -= 5
        if self.rect.x <= -200: self.kill() 

def get_score():
    return 

pygame.init()

screen = pygame.display.set_mode((280, 510))
pygame.display.set_caption("asfour stah")
clock = pygame.time.Clock()

game_active = False

font = pygame.font.Font("FlappyBirdy.ttf", 12)

# game image
bg_image = pygame.image.load("sprites/background-day.png").convert_alpha()
ground_image = pygame.image.load("sprites/base.png").convert_alpha()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

# Obstacles timer
obstacles_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacles_timer, 800)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        if game_active:
            if event.type == obstacles_timer: 
                if randint(0,1):
                    obstacles.add(Obstacles("normal"))
                else:
                    obstacles.add(Obstacles("down"))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
        """"if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos()) # for debugging """

    screen.blit(bg_image, (0,0))

    player.draw(screen)
    player.update()
    
    if game_active:
        obstacles.draw(screen)
        obstacles.update()
        game_active = not (pygame.sprite.spritecollide(player.sprite, obstacles, False))
    else:
        obstacles.empty()
        screen.blit(pygame.image.load("sprites/message.png").convert_alpha(),pygame.image.load("sprites/message.png").get_rect(center = (140,255)))

    screen.blit(ground_image, (0, 450))

    pygame.display.update()

    clock.tick(60)