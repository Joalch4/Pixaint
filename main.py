import pygame
import sys

pygame.init()

CELL_SIZE = 20
ROWS = 20
COLS = 20
BUTTON_SIZE = 50
BUTTON_PADDING = 5
NUM_BUTTONS = 28

GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
WIDTH = GRID_WIDTH + 2 * (BUTTON_SIZE + 10)
HEIGHT = GRID_HEIGHT + 2 * (BUTTON_SIZE + 10)
GRID_X_OFFSET = (WIDTH - GRID_WIDTH) // 2
GRID_Y_OFFSET = (HEIGHT - GRID_HEIGHT) // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pixaint')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_COLOR = BLACK

BUTTON_COLORS = [
    (255, 0, 0),    # Rojo (Botón 18)
    (152, 251, 152),# Verde claro (Botón 19)
    (0, 0, 255),    # Azul (Botón 20)
    (255, 255, 0),  # Amarillo (Botón 21)
    (255, 192, 203),# Rosado (Botón 22)
    (0, 255, 255),  # Celeste (Botón 23)
    (128, 128, 128),# Gris (Botón 24)
    (255, 165, 0),  # Naranja (Botón 25)
    (128, 0, 128),  # Morado (Botón 26)
    (0, 128, 0),    # Verde oscuro (Botón 27)
    (255, 0, 255),  # Blanco (Botón 28)
]

button_images = []
for i in range(1, 18):
    image_path = f"imagenes_pixaint/boton_{i}.png"
    button_images.append(pygame.image.load(image_path))

grid = [[WHITE] * COLS for _ in range(ROWS)]

buttons = []

for i in range(NUM_BUTTONS // 4):
    buttons.append({"rect": pygame.Rect(GRID_X_OFFSET - BUTTON_SIZE - 10, GRID_Y_OFFSET + i * (BUTTON_SIZE + BUTTON_PADDING), BUTTON_SIZE, BUTTON_SIZE), "text": f"Botón {i+1}"})

for i in range(NUM_BUTTONS // 4):
    buttons.append({"rect": pygame.Rect(GRID_X_OFFSET + GRID_WIDTH + 10, GRID_Y_OFFSET + i * (BUTTON_SIZE + BUTTON_PADDING), BUTTON_SIZE, BUTTON_SIZE), "text": f"Botón {i+1+NUM_BUTTONS//4}"})

for i in range(NUM_BUTTONS // 4):
    buttons.append({"rect": pygame.Rect(GRID_X_OFFSET + i * (BUTTON_SIZE + BUTTON_PADDING), GRID_Y_OFFSET - BUTTON_SIZE - 10, BUTTON_SIZE, BUTTON_SIZE), "text": f"Botón {i+1+NUM_BUTTONS//2}"})

for i in range(NUM_BUTTONS // 4):
    buttons.append({"rect": pygame.Rect(GRID_X_OFFSET + i * (BUTTON_SIZE + BUTTON_PADDING), GRID_Y_OFFSET + GRID_HEIGHT + 10, BUTTON_SIZE, BUTTON_SIZE), "text": f"Botón {i+1+3*(NUM_BUTTONS//4)}"})

selected_color = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            button_clicked = False
            for idx, button in enumerate(buttons[17:]):
                if button["rect"].collidepoint(mouse_pos):
                    selected_color = BUTTON_COLORS[idx]
                    button_clicked = True
                    break
            if not button_clicked:
                grid_x = (mouse_pos[0] - GRID_X_OFFSET) // CELL_SIZE
                grid_y = (mouse_pos[1] - GRID_Y_OFFSET) // CELL_SIZE
                if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
                    grid[grid_y][grid_x] = selected_color

    screen.fill(WHITE)
    for idx, button in enumerate(buttons):
        if idx < 17:
            screen.blit(button_images[idx], button["rect"].topleft)
        else:
            pygame.draw.rect(screen, BUTTON_COLORS[idx - 17], button["rect"], border_radius=5)

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(GRID_X_OFFSET + col * CELL_SIZE, GRID_Y_OFFSET + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, grid[row][col], rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    pygame.display.flip()

pygame.quit()
sys.exit()
