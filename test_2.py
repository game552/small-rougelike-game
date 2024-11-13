import pygame
import math

# --- Настройки ---

WIDTH = 600
HEIGHT = 400
RECT_SIZE = 20
RECT_COLOR = (255, 0, 0)  # Красный
SPEED = 2

# --- Функции ---

def get_line_equation(p1, p2):
    """Возвращает уравнение прямой, проходящей через две точки."""
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        return float("inf"), x1  # Вертикальная линия
    else:
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope, intercept

def get_point_on_line(slope, intercept, x):
    """Возвращает точку на прямой с заданным x."""
    if slope == float("inf"):
        return x, intercept  # Вертикальная линия
    else:
        return x, slope * x + intercept

# --- Инициализация ---

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Движение по траектории")
clock = pygame.time.Clock()

# --- Начальная позиция тела ---

rect_x = 100
rect_y = 100
rect = pygame.Rect(rect_x, rect_y, RECT_SIZE, RECT_SIZE)

# --- Траектория движения ---

trajectory_points = [(100, 100), (200, 200), (300, 100), (400, 200)]
current_point_index = 0

# --- Основной игровой цикл ---

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Очистка экрана

    # Отрисовка траектории
    for i in range(len(trajectory_points) - 1):
        pygame.draw.line(screen, (255, 255, 255), trajectory_points[i], trajectory_points[i + 1], 2)

    # Отрисовка тела
    pygame.draw.rect(screen, RECT_COLOR, rect)

    # Перемещение тела по траектории
    if current_point_index < len(trajectory_points) - 1:
        target_x, target_y = trajectory_points[current_point_index + 1]
        slope, intercept = get_line_equation((rect_x + RECT_SIZE // 2, rect_y + RECT_SIZE // 2),
                                             (target_x, target_y))

        if rect_x + RECT_SIZE // 2 < target_x:
            rect_x += SPEED
            rect.x = rect_x
            rect.y = get_point_on_line(slope, intercept, rect_x + RECT_SIZE // 2)[1] - RECT_SIZE // 2
        else:
            current_point_index += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()