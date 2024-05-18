import pygame
import sys

pygame.init()

CELL_SIZE = 20
ROWS = 20
COLS = 20
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
WIDTH = 550
HEIGHT = 530
GRID_X_OFFSET = (WIDTH - GRID_WIDTH) // 2
GRID_Y_OFFSET = (HEIGHT - GRID_HEIGHT) // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pixaint')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_COLOR = BLACK

grid = [[0] * COLS for _ in range(ROWS)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if pygame.Rect(10, 50, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Borrador")
            if pygame.Rect(10, 110, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Selección Rectangulo")
            if pygame.Rect(10, 170, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Circulo")
            if pygame.Rect(10, 230, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Guardar ")
            if pygame.Rect(10, 290, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Cargar")
            if pygame.Rect(10, 350, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Matriz")
            if pygame.Rect(10, 410, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Matriz Numerica")
            if pygame.Rect(10, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Selección Limpiar")
            if pygame.Rect(70, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Zoom In")
            if pygame.Rect(130, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Zoom Out")
            if pygame.Rect(190, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Rotar Derecha")
            if pygame.Rect(250, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Rotar Izquierda")
            if pygame.Rect(310, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Selección Reflejo Horizontal")
            if pygame.Rect(370, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Reflejo Vertical")
            if pygame.Rect(430, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Contraste")
            if pygame.Rect(490, 470, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion Negativo")
            if pygame.Rect(70, 6, 50, 50).collidepoint(pygame.mouse.get_pos()):
                print("Seleccion ASCII")


    screen.fill(WHITE)
    screen.blit(pygame.image.load("boton_borrador.png"), (10,50))
    screen.blit(pygame.image.load("boton_rect.png"), (10, 110))
    screen.blit(pygame.image.load("boton_circulo.png"), (10, 170))
    screen.blit(pygame.image.load("boton_guardar.png"), (10, 230))
    screen.blit(pygame.image.load("boton_cargar.png"), (10, 290))
    screen.blit(pygame.image.load("boton_matriz.png"), (10, 350))
    screen.blit(pygame.image.load("boton_matriznum.png"), (10, 410))
    screen.blit(pygame.image.load("boton_limpiar.png"), (10, 470))
    screen.blit(pygame.image.load("boton_zoomin.png"), (70, 470))
    screen.blit(pygame.image.load("boton_zoomout.png"), (130, 470))
    screen.blit(pygame.image.load("boton_rotard.png"), (190, 470))
    screen.blit(pygame.image.load("boton_rotari.png"), (250, 470))
    screen.blit(pygame.image.load("boton_reflejhor.png"), (310, 470))
    screen.blit(pygame.image.load("boton_reflejvert.png"), (370, 470))
    screen.blit(pygame.image.load("boton_contraste.png"), (430, 470))
    screen.blit(pygame.image.load("boton_negativo.png"), (490, 470))
    screen.blit(pygame.image.load("boton_ascii.png"), (70, 6))
    

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(GRID_X_OFFSET + col * CELL_SIZE, GRID_Y_OFFSET + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    pygame.display.flip()

pygame.quit()
sys.exit()
