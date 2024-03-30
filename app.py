import pygame
from random import randint
from sys import exit

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
        if keys[pygame.K_SPACE] and self.rect.top <= 490: 
            self.gravity = -6 
            wing_sound.play()
    def update(self):
        global game_active 
        if game_active:
            self.physics()
            self.jump()
            if self.rect.y >= 450 : 
                hit_sound.play()
                game_active = False
        if not game_active: self.rect.center = (140, 360)
        self.animations()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type, ypos):
        super().__init__()
        self.image = pygame.image.load("sprites/pipe-green.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (280, ypos))
        if type == "down":
            self.image = pygame.transform.rotate(self.image, 180).convert_alpha()
            self.rect = self.image.get_rect(bottomleft = (280, ypos - 80))
    def update(self):
        self.rect.x -= 5
        if self.rect.x <= -200: self.kill() 

pygame.init()

screen = pygame.display.set_mode((280, 510))
pygame.display.set_caption("asfour stah")
clock = pygame.time.Clock()

game_active = False

font = pygame.font.Font("font.otf", 16)

score = 0

# sound effect
wing_sound = pygame.mixer.Sound("audio/action_jump.mp3")
wing_sound.set_volume(0.3)
hit_sound = pygame.mixer.Sound("audio/hit.mp3")
point_sound = pygame.mixer.Sound("audio/point.mp3")

# game image
bg_image = pygame.image.load("sprites/background-day.png").convert_alpha() 
ground_image = pygame.image.load("sprites/base.png").convert_alpha()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

# Obstacles timer
obstacles_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacles_timer, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        if game_active:
            if event.type == obstacles_timer: 
                    ypos = randint(200, 400)       
                    obstacles.add(Obstacles("normal", ypos))
                    obstacles.add(Obstacles("down", ypos))
                    score += 1
                    if score > 0: point_sound.play()
        else:
            score = -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

    screen.blit(bg_image, (0,0))

    player.draw(screen)
    player.update()

    tmp_score = score

    if game_active:
        if tmp_score == -1 : tmp_score = 0
        score_surf = font.render(f"score : {int(tmp_score)}", True, "black").convert_alpha()
        score_rect = score_surf.get_rect(topleft = (5, 5)) 
        obstacles.draw(screen)
        obstacles.update()
        screen.blit(score_surf, score_rect)
        if pygame.sprite.spritecollide(player.sprite, obstacles, False):
            hit_sound.play()
            game_active = False
    else:
        obstacles.empty()
        screen.blit(pygame.image.load("sprites/message.png").convert_alpha(),pygame.image.load("sprites/message.png").get_rect(center = (140,255)))
        if tmp_score != -1:
            score_surf = font.render("your last score", True, "black").convert_alpha()
            score_surf_1 = font.render(f"{tmp_score}", True, "black").convert_alpha()
            score_rect = score_surf.get_rect(center = (140, 415)) 
            score_rect_1 = score_surf_1.get_rect(center = (140, 432)) 
            screen.blit(score_surf, score_rect)
            screen.blit(score_surf_1, score_rect_1)
        

    screen.blit(ground_image, (0, 450))

    pygame.display.update()

    clock.tick(60)