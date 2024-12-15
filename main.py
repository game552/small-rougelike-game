from CONST import *
from functions import *
from player import *
import Level_generation
import pygame
import random
import sys
import room_generation
import queue


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

    def move(self, player_rect, current_room_player, list_of_rooms):
        """
        Перемещает врага в сторону игрока, если игрок находится в той же комнате.
        Враг проверяет коллизии с игроком.
        """
        # Проверяем, находится ли игрок в одной комнате с врагом
        if current_room_player == self.get_current_room(list_of_rooms):
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


sys.setrecursionlimit(3000)

# --- Генерация комнат ---
game_map = room_generation.Map()
game_map.set_cell(35, 'Start')
game_map.que.put(35)
game_map.conclusion.append(35)

while not game_map.que.empty():
    game_map.room_generation(game_map.que.get())
rooms = game_map.return_map()

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

level = Level_generation.CreateRooms(rooms, Level_generation.screen)
level.create_rooms()
level.create_doors()
wall_list = level.get_wall_group()
door_list = level.get_door_group()
rooms_list = level.get_room_group()
player = Player(rooms_list.sprites()[0].rect.center[0], rooms_list.sprites()[0].rect.center[1],
                Level_generation.screen,
                'priest1_v1_1.png')
player_rect = player.rect

# создание врагов

a = random.randint(1, 10)
# Генерация врагов для каждой комнаты
for room in rooms_list:
    center = room.center
    room_doors = [door for door in door_list if door.rect.colliderect(room.rect)]  # Двери в комнате

    # Проверяем, что комната действительно существует и находится в области уровня
    if not room or not room.rect.colliderect(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
        continue

    # Пропускаем комнату, где находится игрок
    if Level_generation.get_player_room(player_rect, rooms_list) == room:
        continue

    # Проверяем, достаточно ли большая комната для спавна врагов
    if room.rect.width < 100 or room.rect.height < 100:
        continue

    # Рассчитываем количество врагов
    difficulty = 1.5  # Например, уровень сложности
    num_enemies = calculate_enemy_count(room, difficulty)

    for _ in range(num_enemies):
        attempts = 0
        while attempts < 100:
            min_x = room.rect.left + 10
            max_x = room.rect.right - 10
            min_y = room.rect.top + 10
            max_y = room.rect.bottom - 10

            # Генерируем координаты врага внутри области (ширина и высота комнаты уменьшены на 20)
            enemy_x = random.randint(min_x + 10, max_x - 10)
            enemy_y = random.randint(min_y + 10, max_y - 10)

            # Проверяем расстояние до дверей
            if is_far_enough_from_doors(enemy_x, enemy_y, room_doors, 100):
                enemy = Enemy(
                    screen,
                    enemy_x, enemy_y,
                    SPEED / 1.5,
                    "skeleton_v2_3.png"
                )
                enemy_group.add(enemy)
                break

            attempts += 1

# --- Основной игровой цикл ---

while Level_generation.state:
    if game_over or win_end:
        if game_over:
            Level_generation.show_go_screen()
        if win_end:
            Level_generation.show_win_screen()
        win_end = False
        game_over = False
        mouse_held = False
        click_counter = 0
        # --- Генерация комнат ---
        game_map = room_generation.Map()
        game_map.set_cell(35, 'Start')
        game_map.que.put(35)
        game_map.conclusion.append(35)

        while not game_map.que.empty():
            game_map.room_generation(game_map.que.get())
        rooms = game_map.return_map()

        # --- Создание игрока и врагов ---

        bullet_list = []
        enemy_group = pygame.sprite.Group()
        dead_list = []
        enemy_dict = {}
        score = 0

        # Создание комнат и дверей

        level = Level_generation.CreateRooms(rooms, Level_generation.screen)
        level.create_rooms()
        level.create_doors()
        wall_list = level.get_wall_group()
        door_list = level.get_door_group()
        rooms_list = level.get_room_group()
        player = Player(rooms_list.sprites()[0].rect.center[0], rooms_list.sprites()[0].rect.center[1],
                        Level_generation.screen,
                        'priest1_v1_1.png')
        player_rect = player.rect
        a = random.randint(1, 10)
        # Генерация врагов для каждой комнаты
        for room in rooms_list:
            center = room.center
            room_doors = [door for door in door_list if door.rect.colliderect(room.rect)]  # Двери в комнате

            # Проверяем, что комната действительно существует и находится в области уровня
            if not room or not room.rect.colliderect(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
                continue

            # Пропускаем комнату, где находится игрок
            if Level_generation.get_player_room(player_rect, rooms_list) == room:
                continue

            # Проверяем, достаточно ли большая комната для спавна врагов
            if room.rect.width < 100 or room.rect.height < 100:
                continue

            # Рассчитываем количество врагов
            difficulty = 0.5  # Например, уровень сложности
            num_enemies = calculate_enemy_count(room, difficulty)

            for _ in range(num_enemies):
                attempts = 0
                while attempts < num_enemies:
                    min_x = room.rect.left + 10
                    max_x = room.rect.right - 10
                    min_y = room.rect.top + 10
                    max_y = room.rect.bottom - 10

                    # Генерируем координаты врага внутри области (ширина и высота комнаты уменьшены на 20)
                    enemy_x = random.randint(min_x + 10, max_x - 10)
                    enemy_y = random.randint(min_y + 10, max_y - 10)

                    # Проверяем расстояние до дверей
                    if is_far_enough_from_doors(enemy_x, enemy_y, room_doors, 100):
                        enemy = Enemy(
                            screen,
                            enemy_x, enemy_y,
                            SPEED / 1.5,
                            "skeleton_v2_3.png"
                        )
                        enemy_group.add(enemy)
                        break

                    attempts += 1

    if len(enemy_group) == 0:
        win_end = True

    # Очистка экрана
    Level_generation.screen.fill((0, 0, 0))

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()

    # Проверка нажатий клавиш для перемещения игрока
    if keys[pygame.K_a] and \
            player.possibility_of_movement("left", wall_list, door_list)[0]:
        if player.possibility_of_movement("left", wall_list, door_list)[1]:
            if Level_generation.room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.x -= 52
        else:
            player.rect.x -= Level_generation.SPEED

    if keys[pygame.K_d] and \
            player.possibility_of_movement("right", wall_list, door_list)[0]:
        if player.possibility_of_movement("right", wall_list, door_list)[1]:
            if Level_generation.room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.x += 52
        else:
            player.rect.x += Level_generation.SPEED

    if keys[pygame.K_s] and \
            player.possibility_of_movement("down", wall_list, door_list)[0]:
        if player.possibility_of_movement("down", wall_list, door_list)[1]:
            if Level_generation.room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.y += 52
        else:
            player.rect.y += Level_generation.SPEED

    if keys[pygame.K_w] and player.possibility_of_movement("up", wall_list, door_list)[
        0]:
        if player.possibility_of_movement("up", wall_list, door_list)[1]:
            if Level_generation.room_is_clear(rooms_list, enemy_group, player_rect):
                player.rect.y -= 52
        else:
            player.rect.y -= Level_generation.SPEED

    # Движение врагов
    for enemy in enemy_group:
        enemy.move(player.rect, Level_generation.get_player_room(player_rect, rooms_list), rooms_list)

    # В игровом цикле добавьте логику для обновления пуль:
    for bullet in bullet_group:
        bullet.update(wall_list, enemy_group)  # Обновляем состояние пули
        bullet.draw(Level_generation.screen)  # Отрисовываем пулю на экране

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot(event.pos, bullet_group)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    left_button, _, _ = pygame.mouse.get_pressed()
    # dadad
    mouse_pos = pygame.mouse.get_pos()

    if left_button:
        click_counter += 1
        if click_counter == 10:
            player.shoot(mouse_pos, bullet_group)  # Игрок стреляет только на 10-й клик
            click_counter = 0

    # Отрисовка
    level.wall_group.draw(Level_generation.screen)
    level.door_group.draw(Level_generation.screen)
    enemy_group.update()
    for room in rooms_list:
        if player.rect.colliderect(room.rect):
            pass
        else:
            Level_generation.screen.blit(room.image, room.rect)
    player.update()
    Level_generation.screen.blit(player.image, player.rect)
    pygame.display.flip()
    Level_generation.clock.tick(60)

pygame.quit()
