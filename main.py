import pygame
import random

import sys

sys.setrecursionlimit(3000)

# --- Константы ---

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
WALL_WIDTH = SCREEN_WIDTH // 4
WALL_HEIGHT = SCREEN_HEIGHT // 3
PLAYER_SIZE = 10
PLAYER_COLOR = (0, 0, 0)
SPEED = 5
FONT_NAME = pygame.font.match_font('arial')
state = True


# --- Функции ---

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_go_screen():
    draw_text(screen, "Press a R to begin", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(48)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if pygame.key.get_pressed()[pygame.K_r]:
            waiting = False


def get_line_equation(p1, p2):
    """Возвращает уравнение прямой, проходящей через две точки."""
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        return 0, x1  # Вертикальная линия
    else:
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope, intercept


def get_point_on_line_x(slope, intercept, x):
    """Возвращает точку на прямой с заданным x."""
    if slope == 0:
        return x, intercept  # Вертикальная линия
    else:
        return x, slope * x + intercept


def get_point_on_line_y(k: float, l: float, y: float) -> tuple:
    """Возвращает точку на прямой с заданным y"""
    if k == 0:
        return l, y  # Вертикальная линия
    else:
        if k != 0:
            return (y - l) / k, y  # Вычисляем x через уравнение прямой
        else:
            return 0, 0


def create_line_points_x(start_x: int, start_y: int, end_x: int, end_y: int, step_size=10) -> list:
    """возвращает точки прямой по оси x"""
    points = [(start_x, start_y)]
    k, l = get_line_equation((start_x, start_y), (end_x, end_y))
    if start_x < end_x:
        x = start_x + step_size
    else:
        x = start_x - step_size
    x, y = get_point_on_line_x(k, l, x)
    points.append((x, y))
    while abs(x) < SCREEN_WIDTH and abs(y) < SCREEN_HEIGHT:
        if start_x < end_x:
            x += step_size
        else:
            x -= step_size
        x, y = get_point_on_line_x(k, l, x)

        points.append((x, y))

    return points


def create_line_points_y(start_x: int, start_y: int, end_x: int, end_y: int, step_size=10) -> list:
    """возвращает точки прямой о оси y"""
    points = [(start_x, start_y)]
    k, l = get_line_equation((start_x, start_y), (end_x, end_y))
    if start_y < end_y:
        y = start_y + step_size
    else:
        y = start_y - step_size
    x, y = get_point_on_line_y(k, l, y)
    points.append((x, y))
    while abs(x) < SCREEN_WIDTH and abs(y) < SCREEN_HEIGHT:
        if start_y < end_y:
            y += step_size
        else:
            y -= step_size
        x, y = get_point_on_line_y(k, l, y)
        points.append((x, y))
    return points


# --- Классы ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_player, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.screen = screen_player
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def create_player(self):
        pygame.draw.rect(self.screen, PLAYER_COLOR, self.rect, 0)

    def get_rect(self):
        return self.rect

    @staticmethod
    def possibility_of_movement(directory_of_movement, rect_list, cord, rect_list2):
        if directory_of_movement == 'right':
            tester = pygame.Rect(cord[0] + 10, cord[1], 10, 10)
        elif directory_of_movement == 'left':
            tester = pygame.Rect(cord[0] - SPEED, cord[1], 10, 10)
        elif directory_of_movement == 'up':
            tester = pygame.Rect(cord[0], cord[1] - SPEED, 10, 10)
        else:
            tester = pygame.Rect(cord[0], cord[1] + 10, 10, 10)
        if tester.collidelistall(rect_list2) and state:
            del tester
            return True, True
        elif tester.collidelistall(rect_list) and state:
            del tester
            return False, False
        else:
            del tester
            return False, True

    def shoot(self, pos: tuple[int, int], wall_list3, enemy_list3):
        bullet = Bullet(self.rect.centerx, self.rect.centery, pos)
        bullet.create(wall_list3, enemy_list3)

    def update(self):
        if self.rect.collidelistall(enemy_list):
            self.kill()




class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, speed, filename):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def get_current_room(self, room_list):
        return self.rect.collidelistall(room_list)

    def create_enemy(self):
        self.screen.blit(self.image, self.rect)

    @staticmethod
    def can_move(tester, player_rect):
        if tester.colliderect(player_rect):
            global game_over
            game_over = True
            return False
        return True

    def move(self, target_x, target_y, current_room_player):
        """Перемещает врага в сторону цели, если это возможно."""
        if current_room_player == self.get_current_room(rooms_list):
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y

            if abs(dx) > abs(dy):  # Двигаемся по x, если он более значителен
                direction = 'right' if dx > 0 else 'left'
                tester = self.rect.copy()
                tester.x += self.speed if direction == 'right' else -self.speed
                if self.can_move(tester, player_rect):
                    self.rect.x += self.speed if direction == 'right' else -self.speed
            else:  # Двигаемся по y
                direction = 'down' if dy > 0 else 'up'
                tester = self.rect.copy()
                tester.y += self.speed if direction == 'down' else -self.speed
                if self.can_move(tester, player_rect):
                    self.rect.y += self.speed if direction == 'down' else -self.speed

    def death(self):
        self.kill()


class Wall:
    def __init__(self, screen):
        self.screen = screen


class CreateRooms(Wall):
    def __init__(self, rooms, screen):
        super().__init__(screen)
        self.rect_list = []
        self.rooms = rooms
        self.doors = []
        self.rooms_rects = []

    def create_rooms(self):
        y_top = 0
        y_bottom = WALL_HEIGHT
        x_left = 0

        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    # Отрисовка стен
                    pygame.draw.rect(self.screen, (145, 255, 255),
                                     (x * WALL_WIDTH, y_top, WALL_WIDTH, 15), 0)  # Верхняя
                    pygame.draw.rect(self.screen, (145, 255, 255),
                                     (x * WALL_WIDTH, y_bottom, WALL_WIDTH, 15), 0)  # Нижняя
                    pygame.draw.rect(self.screen, (255, 0, 255),
                                     (x * WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT), 0)  # Левая
                    pygame.draw.rect(self.screen, (255, 0, 0),
                                     (x * WALL_WIDTH + WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT), 0)  # Правая

                    # Добавление прямоугольников стен в список
                    self.rect_list.append(pygame.Rect(x * WALL_WIDTH, y_top, WALL_WIDTH, 15))
                    self.rect_list.append(pygame.Rect(x * WALL_WIDTH, y_bottom, WALL_WIDTH, 15))
                    self.rect_list.append(pygame.Rect(x * WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT))
                    self.rect_list.append(pygame.Rect(x * WALL_WIDTH + WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT))

                    # Добавление прямоугольника комнаты в список
                    self.rooms_rects.append(pygame.Rect(x * WALL_WIDTH, y * WALL_HEIGHT, WALL_WIDTH, WALL_HEIGHT))

            y_top += WALL_HEIGHT
            y_bottom += WALL_HEIGHT
            x_left += WALL_WIDTH

    def create_doors(self):
        """Создает двери между комнатами."""
        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    if x < len(self.rooms[y]) - 1 and self.rooms[y][x + 1]:
                        # Отрисовка двери справа
                        pygame.draw.rect(self.screen, (0, 40, 0),
                                         (x * WALL_WIDTH + WALL_WIDTH - 3, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 15,
                                          22, 50), 0)
                        self.doors.append(pygame.Rect(
                            x * WALL_WIDTH + WALL_WIDTH - 2, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 15, 22, 50))

                    if y < len(self.rooms) - 1 and self.rooms[y + 1][x]:
                        # Отрисовка двери снизу
                        pygame.draw.rect(self.screen, (0, 255, 0),
                                         (x * WALL_WIDTH + WALL_WIDTH // 2 - 15, y * WALL_HEIGHT + WALL_HEIGHT - 5, 45,
                                          22), 0)
                        self.doors.append(pygame.Rect(
                            x * WALL_WIDTH + WALL_WIDTH // 2 - 15, y * WALL_HEIGHT + WALL_HEIGHT - 5, 45, 22))

    def get_rect_list(self):
        return self.rect_list

    def get_rooms(self):
        return self.rooms_rects

    def get_door_list(self):
        return self.doors


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.x_target = target[0]
        self.y_target = target[1]
        self.image = pygame.Surface((42, 42))
        self.image.fill((255, 255, 255))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 5, 5)
        self.room = self.rect.collidelistall(rooms_list)
        self.speedy = 10
        bullet_list.append(self)

    def create(self, wall_list2: list, enemy_list2: list):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)
        self.update(wall_list2, enemy_list2)

    def update(self, wall_list2: list, enemy_list2: list):
        line = create_line_points_x(self.x, self.y, self.x_target, self.y_target)
        line2 = create_line_points_y(self.x, self.y, self.x_target, self.y_target)
        line.extend(j for j in line2 if j not in line)
        for re in line:
            rect = pygame.Rect(re[0], re[1], 5, 5)
            if rect.collidelistall(rooms_list) == self.room:
                if rect.collidelistall(enemy_list2):
                    enemy_list.remove(enemy_list2[rect.collidelistall(enemy_list2)[0]])
                    self.kill()
                    return
                else:
                    pygame.draw.rect(screen, (255, 0, 0), rect, 4)


# --- Инициализация игры ---

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

# --- Генерация комнат ---

rooms = [[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [1, 1, 1, 1],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]]

# --- Создание игрока и врагов ---

player = Player(560, 290, screen, 'priest1_v1_1.png')
player_rect = player.get_rect()
bullet_list = []
enemy_list = []
dead_list = []
visited_rooms = []
count_enemy = 0
enemy_dict = {}
score = 0
game_over = False

level = CreateRooms(rooms, screen)
level.create_rooms()
level.create_doors()
rect_list = level.get_rect_list()
door_list = level.get_door_list()
rooms_list = level.get_rooms()

for i in range(len(rooms_list)):
    center = rooms_list[i].center
    enemy = Enemy(screen, center[0], center[1], 2, "skeleton_v2_3.png")
    enemy_list.append(enemy)

# --- Основной игровой цикл ---


while state:
    if game_over:
        show_go_screen()
        game_over = False
        rooms = [[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
                 [1, 1, 1, 1],
                 [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]]

        # --- Создание игрока и врагов ---

        player = Player(560, 290, screen, 'priest1_v1_1.png')
        player_rect = player.get_rect()
        bullet_list = []
        enemy_list = []
        dead_list = []
        enemy_dict = {}
        score = 0

        level = CreateRooms(rooms, screen)
        level.create_rooms()
        level.create_doors()
        rect_list = level.get_rect_list()
        door_list = level.get_door_list()
        rooms_list = level.get_rooms()

        for i in range(len(rooms_list)):
            center = rooms_list[i].center
            enemy = Enemy(screen, center[0], center[1], 2, "skeleton_v2_3.png")
            enemy_list.append(enemy)



    # Очистка экрана
    screen.fill((0, 0, 0))

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and \
            player.possibility_of_movement("left", rect_list, (player.rect.x, player.rect.y), door_list)[1]:
        if player.possibility_of_movement("left", rect_list, (player.rect.x, player.rect.y), door_list)[0]:
            player.rect.x -= 40
        else:
            player.rect.x -= SPEED

    if keys[pygame.K_d] and \
            player.possibility_of_movement("right", rect_list, (player.rect.x, player.rect.y), door_list)[1]:
        if player.possibility_of_movement("right", rect_list, (player.rect.x, player.rect.y), door_list)[0]:
            player.rect.x += 40
        else:
            player.rect.x += SPEED

    if keys[pygame.K_s] and \
            player.possibility_of_movement("down", rect_list, (player.rect.x, player.rect.y), door_list)[1]:
        if player.possibility_of_movement("down", rect_list, (player.rect.x, player.rect.y), door_list)[0]:
            player.rect.y += 40
        else:
            player.rect.y += SPEED

    if keys[pygame.K_w] and player.possibility_of_movement("up", rect_list, (player.rect.x, player.rect.y), door_list)[
        1]:
        if player.possibility_of_movement("up", rect_list, (player.rect.x, player.rect.y), door_list)[0]:
            player.rect.y -= 40
        else:
            player.rect.y -= SPEED

    # Движение врагов
    for enemy in enemy_list:
        enemy.move(player.rect.x, player.rect.y, player.rect.collidelistall(rooms_list))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot(event.pos, rect_list, enemy_list)
        if event.type == pygame.QUIT:
            pygame.quit()



    # Отрисовка
    level.create_rooms()
    level.create_doors()
    player.create_player()
    for en in enemy_list:
        screen.blit(en.image, en.rect)
    screen.blit(player.image, player.get_rect())
    pygame.display.flip()
    clock.tick(48)

pygame.quit()
