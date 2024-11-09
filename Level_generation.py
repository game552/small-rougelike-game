from CONST import *
from functions import *
import pygame


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