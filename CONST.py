import pygame

PLAYER_SIZE = 20
PLAYER_COLOR = (0, 0, 0)
SPEED = 5
FONT_NAME = pygame.font.match_font('arial')
state = True
GAME_OVER = False

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
WALL_WIDTH = SCREEN_WIDTH // 4
WALL_HEIGHT = SCREEN_HEIGHT // 3
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

clock = pygame.time.Clock()