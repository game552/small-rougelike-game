import random
import pygame
from pygame.locals import QUIT

WALL_WIDTH = 300
WALL_HEIGHT = 200
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
speed = 3

rooms = [[1, random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [1, 1, 1, 1],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
         ]


class Player:
    def __init__(self, x1_size, y1_size, x2_size, y2_size, screen):
        self.screen = screen
        self.player = pygame.Rect(x1_size, y1_size, x2_size, y2_size)
        self.x = self

    def create_player(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.player, 0)

    def get_player(self):
        return self.player


class Enemy:
    def __init__(self, screen, y1, y2):
        self.y_top = y1
        self.y_bot = y2
        self.screen = screen

    def create_enemy(self):
        pygame.draw.rect(self.screen, (255, 0, 0),(self.y_top, self.y_bot, 10, 10), 0)

class Wall:
    def __init__(self, screen):
        self.screen = screen


class Create_rooms(Wall):
    def __init__(self, rooms, screen):
        super().__init__(screen)
        self.rect_list = []
        self.rooms = rooms
        self.doors = []
        self.rooms1 = []


    def create_rooms(self):
        y_top = 0
        y_bottom = 200
        x_left = 0

        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    # Draw top wall
                    pygame.draw.rect(self.screen, (145, 255, 255),
                                     (x * WALL_WIDTH, y_top, WALL_WIDTH, 15), 0)
                    top_wall = pygame.Rect(x * WALL_WIDTH, y_top, WALL_WIDTH, 15)
                    # Draw bottom wall
                    pygame.draw.rect(self.screen, (145, 255, 255),
                                     (x * WALL_WIDTH, y_bottom, WALL_WIDTH, 15), 0)
                    bottom_wall = pygame.Rect(x * WALL_WIDTH, y_bottom, WALL_WIDTH, 15)
                    # Draw left wall
                    pygame.draw.rect(self.screen, (255, 0, 255),
                                     (x * WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT), 0)
                    left_wall = pygame.Rect(x * WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT)
                    # Draw right wall
                    pygame.draw.rect(self.screen, (255, 0, 0),
                                     (x * WALL_WIDTH + WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT), 0)
                    right_wall = pygame.Rect(x * WALL_WIDTH + WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT)

                    self.rooms1.append(pygame.Rect(x * WALL_WIDTH, y * WALL_HEIGHT, WALL_WIDTH, WALL_HEIGHT))
                    self.rect_list.append(bottom_wall)
                    self.rect_list.append(left_wall)
                    self.rect_list.append(right_wall)
                    self.rect_list.append(top_wall)

            y_top += 200
            y_bottom += 200
            x_left += 300

    def create_doors(self):
        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    if x < len(self.rooms[y]) - 1 and self.rooms[y][x + 1]:
                        pygame.draw.rect(self.screen, (0, 40, 0),
                                         (
                                             x * WALL_WIDTH + WALL_WIDTH - 3.1, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 15,
                                             22,
                                             50), 0)
                        self.doors.append(
                            pygame.Rect(x * WALL_WIDTH + WALL_WIDTH - 2, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 5, 22,
                                        50))
                    if y < len(self.rooms) - 1 and self.rooms[y + 1][x]:
                        pygame.draw.rect(self.screen, (0, 255, 0),
                                         (x * WALL_WIDTH + WALL_WIDTH // 2 - 15, y * WALL_HEIGHT + WALL_HEIGHT - 5, 45,
                                          22), 0)
                        self.doors.append(
                            pygame.Rect(x * WALL_WIDTH + WALL_WIDTH // 2 - 15, y * WALL_HEIGHT + WALL_HEIGHT - 5, 45,
                                        22))

    def get_rect_list(self):
        return self.rect_list

    def get_rooms(self):
        return self.rooms1

    def get_door_list(self):
        return self.doors



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
telega = pygame.image.load('priest1_v1_1.png').convert_alpha()
clock = pygame.time.Clock()
player = Player(560, 290, 10, 10, screen)
rect = player.get_player()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    level = Create_rooms(rooms, screen)
    level.create_rooms()
    level.create_doors()
    rect_list = level.get_rect_list()
    door_list = level.get_door_list()
    rooms_list = level.get_rooms()
    for i in rooms_list:
        center = i.center
        Enemy(screen, center[0], center[1]).create_enemy()
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if rect.collidelistall(door_list):
            rect.x -= 37
        elif not rect.collidelistall(rect_list):
            rect.x -= speed
        else:
            rect.x += 20
    elif keys[pygame.K_d]:
        if rect.collidelistall(door_list):
            rect.x += 37
        elif not rect.collidelistall(rect_list):
            rect.x += speed
        else:
            rect.x -= 20
    elif keys[pygame.K_s]:
        if rect.collidelistall(door_list):
            rect.y += 37
        elif not rect.collidelistall(rect_list):
            rect.y += speed
        else:
            rect.y -= 20
    elif keys[pygame.K_w]:
        if rect.collidelistall(door_list):
            rect.y -= 37
        elif not rect.collidelistall(rect_list):
            rect.y -= speed
        else:
            rect.y += 20

    rect.x = max(0, min(rect.x, SCREEN_WIDTH - rect.width))
    rect.y = max(0, min(rect.y, SCREEN_HEIGHT - rect.height))

    for i in rooms_list:
        center = i.center
        Enemy(screen, center[0] + random.randint(0, 40), center[1] + random.randint(0, 40)).create_enemy()
    level.create_rooms()
    level.create_doors()
    player.create_player()
    screen.blit(telega, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
