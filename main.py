import random
import pygame
from pygame.locals import QUIT

ROOM_WIDTH = 300
ROOM_HEIGHT = 200
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

rooms = [[1, random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [1, 1, 1, random.randint(0, 1)],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
         ]


class Player:
    def __init__(self, x1_size, y1_size, x2_size, y2_size, screen):
        self.screen = screen
        self.player = pygame.Rect(x1_size, y1_size, x2_size, y2_size)
        self.x = self

    def create_player(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.player, 0)

    def get_player(self):
        return self.player



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
player = Player(580, 290, 10, 10, screen)
rect = player.get_player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and rect.x - 20 >= 0 and rect.contains(rect):
                rect.move_ip(-20, 0)
            elif event.key == pygame.K_RIGHT and rect.x + 20 < SCREEN_WIDTH:
                rect.move_ip(20, 0)
            elif event.key == pygame.K_UP and rect.y - 20 >= 0:
                rect.move_ip(0, -20)
            elif event.key == pygame.K_DOWN and rect.y + 20 < SCREEN_HEIGHT:
                rect.move_ip(0, 20)
            elif event.key == pygame.K_a and rect.x - 20 >= 0:
                rect.move_ip(-20, 0)
            elif event.key == pygame.K_d and rect.x + 20 < SCREEN_WIDTH:
                rect.move_ip(20, 0)
            elif event.key == pygame.K_w and rect.y - 20 >= 0:
                rect.move_ip(0, -20)
            elif event.key == pygame.K_s and rect.y + 20 < SCREEN_HEIGHT:
                rect.move_ip(0, 20)
    screen.fill((0, 0, 0))
    Create_rooms(rooms, screen).create()
    player.create_player()
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
