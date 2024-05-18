import pygame
import sys

pygame.init()

CELL_SIZE = 20
ROWS = 20
COLS = 20
BUTTON_COLS = 10
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
BUTTON_SIZE = 30
WIDTH = 500
HEIGHT = 500
GRID_X_OFFSET = (WIDTH - GRID_WIDTH) // 2
GRID_Y_OFFSET = (HEIGHT - GRID_HEIGHT) // 2
BUTTON_X_OFFSET = GRID_X_OFFSET + GRID_WIDTH + 5 
BUTTON_Y_OFFSET = GRID_Y_OFFSET + (GRID_HEIGHT - (BUTTON_COLS * BUTTON_SIZE + (BUTTON_COLS - 1) * 5)) // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pixaint')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_COLOR = BLACK

BUTTON_COLORS = [
    (255, 0, 0),    # Rojo
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarillo
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 128, 128),# Gris
    (255, 165, 0),  # Naranja
    (128, 0, 128),  # Púrpura
    (0, 128, 0),    # Verde oscuro
]

grid = [[0] * COLS for _ in range(ROWS)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i in range(BUTTON_COLS):
                button_rect = pygame.Rect(BUTTON_X_OFFSET + 5, BUTTON_Y_OFFSET + i * (BUTTON_SIZE + 5), BUTTON_SIZE, BUTTON_SIZE)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    print("Clic en el botón", i)

    screen.fill(WHITE)

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(GRID_X_OFFSET + col * CELL_SIZE, GRID_Y_OFFSET + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    for i in range(BUTTON_COLS):
        button_rect = pygame.Rect(BUTTON_X_OFFSET + 5, BUTTON_Y_OFFSET + i * (BUTTON_SIZE + 5), BUTTON_SIZE, BUTTON_SIZE)
        pygame.draw.rect(screen, BUTTON_COLORS[i], button_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
