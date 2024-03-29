import pygame
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # animation
        frame_1 = pygame.image.load("sprites/yellowbird-upflap.png")
        frame_2 = pygame.image.load("sprites/yellowbird-midflap.png")
        frame_3 = pygame.image.load("sprites/yellowbird-downflap.png")
        self.frames = [frame_1, frame_2, frame_3]
        self.animation_index = 0
        # gravity 
        self.gravity = 0
        # player 
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (140, 5))
    def animations(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def physics(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.top <= 620: self.gravity = -7 
    def update(self):
        self.physics()
        self.jump()
        self.animations()

pygame.init()

screen = pygame.display.set_mode((280, 510))
pygame.display.set_caption("asfour stah")
clock = pygame.time.Clock()

# bg image
bg_image = pygame.image.load("sprites/background-day.png")

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()

    screen.blit(bg_image, (0,0))

    player.draw(screen)
    player.update()

    pygame.display.update()

    clock.tick(60)