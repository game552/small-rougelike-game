from CONST import *
import pygame

FONT_NAME = pygame.font.match_font('arial')




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
    draw_text(screen, "Press R to restart", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
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
    draw_text(screen, "Press R to restart", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
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
