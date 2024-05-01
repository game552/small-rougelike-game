import random
import pygame
from pygame.locals import QUIT

WALL_WIDTH = 300
WALL_HEIGHT = 200
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
speed = 5
rect_list = []

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


class Wall:
    def __init__(self, screen):
        self.screen = screen


class Create_rooms(Wall):
    def __init__(self, rooms, screen):
        super().__init__(screen)
        self.rect_list = []
        self.rooms = rooms

    def create(self):
        y_top = 0
        y_bottom = 200
        x_left = 0

        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    # Draw top wall
                    pygame.draw.rect(self.screen, (145, 255, 255),
                                     (x * WALL_WIDTH, y_top, WALL_WIDTH, 15), 0)
                    # Draw bottom wall
                    pygame.draw.rect(self.screen, (145, 255, 255),
                                     (x * WALL_WIDTH, y_bottom, WALL_WIDTH, 15), 0)
                    # Draw left wall
                    pygame.draw.rect(self.screen, (255, 0, 255),
                                     (x * WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT), 0)
                    # Draw right wall
                    pygame.draw.rect(self.screen, (255, 0, 0),
                                     (x * WALL_WIDTH + WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT), 0)

                    room_rect = pygame.Rect(x * WALL_WIDTH, y * WALL_HEIGHT, WALL_WIDTH, WALL_HEIGHT)
                    self.rect_list.append(room_rect)

                    if x < len(self.rooms[y]) - 1 and self.rooms[y][x + 1]:
                        pygame.draw.rect(self.screen, (0, 255, 0),
                                         (x * WALL_WIDTH + WALL_WIDTH - 15, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 5, 15,
                                          10), 0)
                    if y < len(self.rooms) - 1 and self.rooms[y + 1][x]:
                        pygame.draw.rect(self.screen, (0, 255, 0),
                                         (x * WALL_WIDTH + WALL_WIDTH // 2 - 5, y * WALL_HEIGHT + WALL_HEIGHT - 15, 10,
                                          15), 0)

            # Update positions for next row of rooms
            y_top += 200
            y_bottom += 200
            x_left += 300


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
    if keys[pygame.K_a] and rect.collidelistall():
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
