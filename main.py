import random
import pygame
from pygame.locals import QUIT


class Node:
    def __init__(self, points):
        self.value = sum(points)
        self.left = None
        self.right = None


def insert(screen, value):
    a = random.randint(0, 1)
    if a:
        i = random.uniform(0, 1200)
        pygame.draw.line(screen, (255, 255, 255), (i, 0), (i, 600), width=6)
    else:
        i = random.uniform(0, 600)
        pygame.draw.line(screen, (255, 255, 255), (0, i), (1200, i), width=6)
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    for _ in range(5):
        insert(screen, (1200, 600))
    screen.fill((0, 0, 0))
    clock.tick(24)

pygame.quit()
