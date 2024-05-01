import random
import pygame
from pygame.locals import QUIT

WALL_WIDTH = 300
WALL_HEIGHT = 200
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
speed = 5

rooms = [[1, random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [1, 1, 1, 1],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
         ]
rooms_test = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]


class Player:
    def __init__(self, x1_size, y1_size, x2_size, y2_size, screen):
        self.screen = screen
        self.player = pygame.Rect(x1_size, y1_size, x2_size, y2_size)
        self.x = self

    def create_player(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.player, 0)

    def get_player(self):
        return self.player


class Wall:
    def __init__(self, screen):
        self.screen = screen


class Create_rooms(Wall):
    def __init__(self, rooms, screen):
        super().__init__(screen)
        self.rooms = rooms

    def create(self):
        s = 200
        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    pygame.draw.rect(self.screen, (145, 255, 255),
                                     (x * WALL_WIDTH, s, WALL_WIDTH, 15), 0)
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (x * WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT), 0)
            s += 200


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
telega = pygame.image.load('priest1_v1_1.png').convert_alpha()
clock = pygame.time.Clock()
player = Player(580, 290, 10, 10, screen)
rect = player.get_player()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        rect.x -= speed
    if keys[pygame.K_d]:
        rect.x += speed
    if keys[pygame.K_s]:
        rect.y += speed
    if keys[pygame.K_w]:
        rect.y -= speed

    rect.x = max(0, min(rect.x, SCREEN_WIDTH - rect.width))
    rect.y = max(0, min(rect.y, SCREEN_HEIGHT - rect.height))

    Create_rooms(rooms, screen).create()
    player.create_player()
    screen.blit(telega, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
