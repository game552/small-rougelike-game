import pygame
import random
import sys
import math

sys.setrecursionlimit(3000)

# --- Константы ---

PLAYER_SIZE = 20
PLAYER_COLOR = (0, 0, 0)
SPEED = 5
FONT_NAME = pygame.font.match_font('arial')
state = True


# --- Функции ---


def get_player_room(player_rect, rooms_group):
    """Определяет, в какой комнате находится игрок."""
    for room in rooms_group:
        if player_rect.colliderect(room.rect):
            return room  # Возвращаем объект комнаты игрока
    return None  # Если комната не найдена


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
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if pygame.key.get_pressed()[pygame.K_r]:
            waiting = False


def show_win_screen():
    draw_text(screen, "YOU WIN!!!!", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press a R to begin", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    screen.fill((0, 0, 0))
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
    """Возвращает точки прямой по оси x"""
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
    """Возвращает точки прямой на оси y"""
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


def room_is_clear(room_list, enemy_group, player_rect):
    room = get_player_room(player_rect, room_list)
    for enemy in enemy_group:
        if room.rect.colliderect(enemy.rect):
            return False
    return True


# --- Классы ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_player, filename):
        super().__init__()  # Инициализация базового класса
        self.image = pygame.image.load(filename).convert_alpha()
        self.screen = screen_player
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(center=(x, y))  # Установка центра игрока

    def update(self):
        """Обновление состояния игрока и отрисовка."""
        self.screen.blit(self.image, self.rect)  # Отрисовка изображения игрока

    def possibility_of_movement(self, direction_of_movement, walls_group, doors_group):
        """
        Проверяет возможность движения в указанном направлении.
        Игрок может двигаться через двери, несмотря на стены.
        """
        tester = self.rect.copy()  # Копируем текущий прямоугольник игрока

        # Определяем направление движения
        if direction_of_movement == 'right':
            tester.x += SPEED  # Перемещаем вправо
        elif direction_of_movement == 'left':
            tester.x -= SPEED  # Перемещаем влево
        elif direction_of_movement == 'up':
            tester.y -= SPEED  # Перемещаем вверх
        elif direction_of_movement == 'down':
            tester.y += SPEED  # Перемещаем вниз

        # Проверка столкновения с дверями
        for door in doors_group:
            door_collided = tester.colliderect(door.rect)
            if door_collided:
                # Игнорируем стены, если дверь найдена
                return True, True  # Возможность движения через дверь

        # Если дверь не найдена, проверяем стены
        if any(tester.colliderect(wall.rect) for wall in walls_group):
            return False, False  # Столкновение со стеной

        # Если нет стены и двери
        return True, False

    def shoot(self, target_pos: tuple[int, int], bullet_group):
        """Создает пулю и добавляет в группу спрайтов."""
        bullet = Bullet(self.rect.centerx, self.rect.centery, target_pos)
        bullet_group.add(bullet)

    def handle_collision_with_enemies(self, enemies_group):
        """Обрабатывает столкновение с врагами."""
        # Проверка на столкновение с врагами
        if pygame.sprite.spritecollide(self, enemies_group, False):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, speed, filename):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        """Отрисовка врага на экране."""
        self.screen.blit(self.image, self.rect)

    @staticmethod
    def can_move(tester, player_rect):
        """Проверяет, может ли враг двигаться, и не столкнется ли он с игроком."""
        if tester.colliderect(player_rect):
            global game_over
            game_over = True
            return False
        return True

    def move(self, player_rect, current_room_player):
        """
        Перемещает врага в сторону игрока, если игрок находится в той же комнате.
        Враг проверяет коллизии с игроком.
        """
        # Проверяем, находится ли игрок в одной комнате с врагом
        if current_room_player == self.get_current_room(rooms_list):
            dx = player_rect.x - self.rect.x
            dy = player_rect.y - self.rect.y

            # Нормализуем вектор движения, чтобы враг двигался одновременно по X и Y
            distance = math.hypot(dx, dy)  # Расстояние между врагом и игроком
            if distance == 0:
                return  # Если враг уже на игроке, не двигаемся

            direction_x = dx / distance
            direction_y = dy / distance

            # Создаем копию прямоугольника для тестирования движения
            tester = self.rect.copy()
            tester.x += direction_x * self.speed
            tester.y += direction_y * self.speed

            # Проверяем возможность движения
            if self.can_move(tester, player_rect):
                self.rect.x += direction_x * self.speed
                self.rect.y += direction_y * self.speed

    def handle_collision(self, direction):
        """Обрабатывает столкновение с препятствием, откатывая движение."""
        if direction == 'right':
            self.rect.x -= self.speed  # Откатываем назад
        elif direction == 'left':
            self.rect.x += self.speed
        elif direction == 'down':
            self.rect.y -= self.speed
        elif direction == 'up':
            self.rect.y += self.speed

    def get_current_room(self, rooms_group):
        """Определяет, в какой комнате находится враг."""
        for room in rooms_group:
            if self.rect.colliderect(room.rect):
                return room  # Возвращаем объект комнаты
        return None  # Если комната не найдена

    def death(self):
        """Обрабатывает смерть врага (анимация или эффекты могут быть добавлены)."""
        self.kill()  # Удаляет врага из всех групп


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)  # Цвет стены
        self.rect = self.image.get_rect(topleft=(x, y))
        self.center = self.rect.center

    def update(self):
        pass


class Door(Wall):
    def __init__(self, x, y, width, height, color, target_room, *groups):
        super().__init__(x, y, width, height, color, *groups)
        self.target_room = target_room


class CreateRooms:
    def __init__(self, rooms, screen):
        self.screen = screen
        self.rooms = rooms
        self.wall_group = pygame.sprite.Group()  # Группа для стен
        self.door_group = pygame.sprite.Group()  # Группа для дверей
        self.room_group = pygame.sprite.Group()  # Группа для комнат (для коллизий или других целей)

    def create_rooms(self):
        y_top = 0
        y_bottom = WALL_HEIGHT
        x_left = 0

        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    # Создание и добавление стен в группу спрайтов
                    Wall(x * WALL_WIDTH, y_top, WALL_WIDTH, 15, (145, 255, 255), self.wall_group)  # Верхняя стена
                    Wall(x * WALL_WIDTH, y_bottom - 15, WALL_WIDTH, 15, (145, 255, 255),
                         self.wall_group)  # Нижняя стена
                    Wall(x * WALL_WIDTH, y * WALL_HEIGHT, 15, WALL_HEIGHT, (255, 0, 255),
                         self.wall_group)  # Левая стена
                    Wall(x * WALL_WIDTH + WALL_WIDTH - 15, y * WALL_HEIGHT, 15, WALL_HEIGHT, (255, 0, 0),
                         self.wall_group)  # Правая стена

                    # Создание комнаты как спрайт для коллизий
                    Wall(x * WALL_WIDTH, y * WALL_HEIGHT, WALL_WIDTH, WALL_HEIGHT, (0, 0, 0), self.room_group)

            y_top += WALL_HEIGHT
            y_bottom += WALL_HEIGHT
            x_left += WALL_WIDTH

    def create_doors(self):
        """Создает двери между комнатами."""
        for y, level in enumerate(self.rooms):
            for x, room in enumerate(level):
                if room:
                    if x < len(self.rooms[y]) - 1 and self.rooms[y][x + 1]:  # Справа
                        Door(x * WALL_WIDTH + WALL_WIDTH - 15, y * WALL_HEIGHT + WALL_HEIGHT // 2 - 25,
                             30, 50, (0, 255, 0), (y, x + 1), self.door_group)  # Исправлено
                    if y < len(self.rooms) - 1 and self.rooms[y + 1][x]:  # Внизу
                        Door(x * WALL_WIDTH + WALL_WIDTH // 2 - 15, y * WALL_HEIGHT + WALL_HEIGHT - 15,
                             50, 30, (0, 255, 0), (y + 1, x), self.door_group)  # Исправлено

    def get_wall_group(self):
        return self.wall_group

    def get_room_group(self):
        return self.room_group

    def get_door_group(self):
        return self.door_group


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target: tuple[int, int], speed=10):
        super().__init__()
        # Задание начальных координат пули
        self.x = x
        self.y = y
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))  # Красная пуля
        self.rect = self.image.get_rect(center=(x, y))

        # Вычисление направления на цель (вектор движения)
        self.x_target, self.y_target = target
        self.direction_x, self.direction_y = self.calculate_direction(x, y, self.x_target, self.y_target)
        self.speed = speed

    def calculate_direction(self, x_start, y_start, x_target, y_target):
        # Вычисление направления как нормализованный вектор
        dx = x_target - x_start
        dy = y_target - y_start
        distance = math.hypot(dx, dy)
        if distance == 0:
            return 0, 0  # Если расстояние 0, пуля никуда не двигается
        return dx / distance, dy / distance

    def update(self, wall_list, enemy_list):
        # Обновление позиции пули
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Проверка на выход за пределы экрана
        if not screen.get_rect().contains(self.rect):
            self.kill()  # Удаление пули, если она вышла за пределы экрана

        # Проверка на столкновение с врагами
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, True)
        if enemy_hit_list:
            for enemy in enemy_hit_list:
                enemy.kill()  # Удаление врага при попадании пули
            self.kill()  # Удаление пули после попадания

        # Проверка на столкновение со стенами
        if pygame.sprite.spritecollideany(self, wall_list):
            self.kill()  # Удаление пули при столкновении со стеной

    def draw(self, screen):
        # Отрисовка пули на экране
        screen.blit(self.image, self.rect)


# --- Инициализация игры ---

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
WALL_WIDTH = SCREEN_WIDTH // 4
WALL_HEIGHT = SCREEN_HEIGHT // 3
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

clock = pygame.time.Clock()

# --- Генерация комнат ---

rooms = [[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
         [1, 1, 1, 1],
         [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]]

# --- Создание игрока и врагов ---


bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
dead_list = []
visited_rooms = []
count_enemy = 0
enemy_dict = {}
score = 0
click_counter = 0
game_over = False
win_end = False
mouse_held = False

# Создание комнат и дверей

level = CreateRooms(rooms, screen)
level.create_rooms()
level.create_doors()
wall_list = level.get_wall_group()
door_list = level.get_door_group()
rooms_list = level.get_room_group()
player = Player(rooms_list.sprites()[0].rect.center[0], rooms_list.sprites()[0].rect.center[1], screen,
                'priest1_v1_1.png')
player_rect = player.rect

# создание врагов


for room in rooms_list:
    center = room.center
    if get_player_room(player_rect, rooms_list) != room:
        enemy = Enemy(screen, center[0], center[1], 3, "skeleton_v2_3.png")
        enemy_group.add(enemy)

# --- Основной игровой цикл ---


while state:
    if game_over or win_end:
        if game_over:
            show_go_screen()
        if win_end:
            show_win_screen()
        win_end = False
        game_over = False
        mouse_held = False
        click_counter = 0
        rooms = [[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],
                 [1, 1, 1, 1],
                 [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]]

        # --- Создание игрока и врагов ---

        bullet_list = []
        enemy_group = pygame.sprite.Group()
        dead_list = []
        enemy_dict = {}
        score = 0

        # Создание комнат и дверей

        level = CreateRooms(rooms, screen)
        level.create_rooms()
        level.create_doors()
        wall_list = level.get_wall_group()
        door_list = level.get_door_group()
        rooms_list = level.get_room_group()
        player = Player(rooms_list.sprites()[0].rect.center[0], rooms_list.sprites()[0].rect.center[1], screen,
                        'priest1_v1_1.png')
        player_rect = player.rect
        for room in rooms_list:
            center = room.center
            if get_player_room(player_rect, rooms_list) != room:
                enemy = Enemy(screen, center[0], center[1], 3, "skeleton_v2_3.png")
                enemy_group.add(enemy)
    if len(enemy_group) == 0:
        win_end = True

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()

    # Проверка нажатий клавиш для перемещения игрока
    if keys[pygame.K_a] and \
            player.possibility_of_movement("left", wall_list, door_list)[0]:
        if player.possibility_of_movement("left", wall_list, door_list)[1]:
            if room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.x -= 52
        else:
            player.rect.x -= SPEED

    if keys[pygame.K_d] and \
            player.possibility_of_movement("right", wall_list, door_list)[0]:
        if player.possibility_of_movement("right", wall_list, door_list)[1]:
            if room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.x += 52
        else:
            player.rect.x += SPEED

    if keys[pygame.K_s] and \
            player.possibility_of_movement("down", wall_list, door_list)[0]:
        if player.possibility_of_movement("down", wall_list, door_list)[1]:
            if room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.y += 52
        else:
            player.rect.y += SPEED

    if keys[pygame.K_w] and player.possibility_of_movement("up", wall_list, door_list)[
        0]:
        if player.possibility_of_movement("up", wall_list, door_list)[1]:
            if room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.y -= 52
        else:
            player.rect.y -= SPEED

    # Движение врагов
    for enemy in enemy_group:
        enemy.move(player.rect, get_player_room(player_rect, rooms_list))

    # В игровом цикле добавьте логику для обновления пуль:
    for bullet in bullet_group:
        bullet.update(wall_list, enemy_group)  # Обновляем состояние пули
        bullet.draw(screen)  # Отрисовываем пулю на экране

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    left_button, _, _ = pygame.mouse.get_pressed()

    mouse_pos = pygame.mouse.get_pos()

    if left_button:
        click_counter += 1
        if click_counter == 10:
            player.shoot(mouse_pos, bullet_group)  # Игрок стреляет только на 7-й клик
            click_counter = 0

    # Отрисовка
    level.wall_group.draw(screen)
    level.door_group.draw(screen)
    enemy_group.update()
    for room in rooms_list:
        if player.rect.colliderect(room.rect):
            pass
        else:
            screen.blit(room.image, room.rect)
    player.update()
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
