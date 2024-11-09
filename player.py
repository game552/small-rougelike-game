import CONST
import functions
import Level_generation
import pygame
import math


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
            tester.x += Level_generation.SPEED  # Перемещаем вправо
        elif direction_of_movement == 'left':
            tester.x -= Level_generation.SPEED  # Перемещаем влево
        elif direction_of_movement == 'up':
            tester.y -= Level_generation.SPEED  # Перемещаем вверх
        elif direction_of_movement == 'down':
            tester.y += Level_generation.SPEED  # Перемещаем вниз

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
        if not Level_generation.screen.get_rect().contains(self.rect):
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
