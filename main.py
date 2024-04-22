import random
import pygame
from pygame.locals import QUIT

# Adjust dimensions for the rooms to fit within the screen
ROOM_WIDTH = 300
ROOM_HEIGHT = 200
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

rooms = [[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [random.randint(0, 1), 1, random.randint(0, 1)],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
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

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill((0, 0, 0))  # Fill the screen with black before drawing anything
    Create_rooms(rooms, screen).create()
    pygame.display.flip()  # Update the display to show changes
    clock.tick(24)

pygame.quit()
print(rooms)
