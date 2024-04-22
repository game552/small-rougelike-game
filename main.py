import random
import pygame
from pygame.locals import QUIT

# Adjust dimensions for the rooms to fit within the screen
ROOM_WIDTH = 300
ROOM_HEIGHT = 200
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

rooms = [[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [random.randint(0, 1), 1, 1, 1],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
         ]


class Create_rooms:
    def __init__(self, rooms, screen):
        self.rooms = rooms
        self.screen = screen

    def create(self):
        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (x * ROOM_WIDTH, y * ROOM_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT), 1)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
rect = pygame.Rect(40, 40, 12, 12)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect.move_ip(-40, 0)
            elif event.key == pygame.K_RIGHT:
                rect.move_ip(40, 0)
            elif event.key == pygame.K_UP:
                rect.move_ip(0, -40)
            elif event.key == pygame.K_DOWN:
                rect.move_ip(0, 40)
            elif event.key == pygame.K_a:
                rect.move_ip(-40, 0)
            elif event.key == pygame.K_d:
                rect.move_ip(40, 0)
            elif event.key == pygame.K_w:
                rect.move_ip(0, -40)
            elif event.key == pygame.K_s:
                rect.move_ip(0, 40)

    screen.fill((0, 0, 0))  # Fill the screen with black before drawing anything
    Create_rooms(rooms, screen).create()
    pygame.draw.rect(screen, (255, 0, 0), rect, 0)
    pygame.display.flip()  # Update the display to show changes
    clock.tick(24)

pygame.quit()
print(rooms)
