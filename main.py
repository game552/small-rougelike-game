import random
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
WALL_WIDTH = SCREEN_WIDTH / 4
WALL_HEIGHT = SCREEN_HEIGHT / 3

speed = 5

rooms = [[1, random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [1, 1, 1, 1],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
         ]


class Player:
    def __init__(self, x1_size, y1_size, x2_size, y2_size, screen):
        self.screen = screen
        self.player = pygame.Rect(x1_size, y1_size, x2_size, y2_size)
        self.x = self.player.x
        self.y = self.player.y

    def create_player(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.player, 0)

    def get_player(self):
        return self.player

    @staticmethod
    def possibility_of_movement(directory_of_movement, rect_list, cord, rect_list2):
        if directory_of_movement == 'right':
            tester = pygame.Rect(cord[0] + 10, cord[1], 10, 10)
        elif directory_of_movement == 'left':
            tester = pygame.Rect(cord[0] - speed, cord[1], 10, 10)
        elif directory_of_movement == 'up':
            tester = pygame.Rect(cord[0], cord[1] - speed, 10, 10)
        else:
            tester = pygame.Rect(cord[0], cord[1] + 10, 10, 10)
        if tester.collidelistall(rect_list2):
            del tester
            return True, True
        elif tester.collidelistall(rect_list):
            del tester
            return False, False
        else:
            del tester
            return False, True


class Enemy:
    def __init__(self, screen, y1, y2, speed):
        self.y_top = y1
        self.speed = speed
        self.y_bot = y2
        self.screen = screen
        self.rect = pygame.Rect(self.y_top, self.y_bot, 10, 10)

    def create_enemy(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.y_top, self.y_bot, 10, 10), 0)

    def enemy_moving(self, player_dist_x, player_dist_y):
        dist_x = self.rect.x - player_dist_x
        dist_y = self.rect.y - player_dist_y
        if dist_x > 0 and dist_y > 0:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        elif dist_x > 0 > dist_y:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        elif dist_x < 0 < dist_y:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        elif dist_x < 0 and dist_y < 0:
            self.rect.x += self.speed
            self.rect.y += self.speed


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
                                             x * WALL_WIDTH + WALL_WIDTH - 3, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 15,
                                             22, 50), 0)
                        self.doors.append(
                            pygame.Rect(x * WALL_WIDTH + WALL_WIDTH - 2, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 15, 22,
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
enemy_list = []
enemy_dict = {}

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
    cord = (rect.topleft[0], rect.topleft[1], rect.bottomright[0], rect.bottomright[1])

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and player.possibility_of_movement("left", rect_list, (rect.x, rect.y), door_list)[1]:
        if player.possibility_of_movement("left", rect_list, (rect.x, rect.y), door_list)[0]:
            rect.x -= 40
        else:
            rect.x -= speed

    if keys[pygame.K_d] and player.possibility_of_movement("right", rect_list, (rect.x, rect.y), door_list)[1]:
        if player.possibility_of_movement("right", rect_list, (rect.x, rect.y), door_list)[0]:
            rect.x += 40
        else:
            rect.x += speed

    if keys[pygame.K_s] and player.possibility_of_movement("down", rect_list, (rect.x, rect.y), door_list)[1]:
        if player.possibility_of_movement("down", rect_list, (rect.x, rect.y), door_list)[0]:
            rect.y += 40
        else:
            rect.y += speed

    if keys[pygame.K_w] and player.possibility_of_movement("up", rect_list, (rect.x, rect.y), door_list)[1]:
        if player.possibility_of_movement("up", rect_list, (rect.x, rect.y), door_list)[0]:
            rect.y -= 40
        else:
            rect.y -= speed

    # rect.x = max(0, min(rect.x, SCREEN_WIDTH - rect.width))
    # rect.y = max(0, min(rect.y, SCREEN_HEIGHT - rect.height))

    for i in range(len(rooms_list)):
        if len(rooms_list) > len(enemy_list):
            center = rooms_list[i].center
            enemy = Enemy(screen, center[0] + random.randint(0, 60), center[1] + random.randint(0, 60), 1)
            enemy.create_enemy()
            enemy_dict[i] = enemy
            enemy_list.append((center[0] + random.randint(0, 60), center[1] + random.randint(0, 60)))
        else:
            Enemy(screen, enemy_list[i][0], enemy_list[i][1], 1).create_enemy()

    for i in range(10):
        enemy_dict[0].enemy_moving(rect.x, rect.y)
        enemy_dict[0].create_enemy()

    level.create_rooms()
    level.create_doors()
    player.create_player()
    screen.blit(telega, rect)
    pygame.display.flip()
    clock.tick(48)

pygame.quit()
