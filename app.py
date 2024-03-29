import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("flappy bird")
clock = pygame.time.Clock()

screen.fill("Pink")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()

    pygame.display.update()

    clock.tick(60)