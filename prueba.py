import pygame
import sys
import os
from datetime import datetime
from tkinter import Tk, filedialog


class Pixaint:
    def __init__(self):
        # Inicialización de Pygame y definición de constantes
        pygame.init()
        self.drawing_circle = False
        self.using_eraser = False
        self.circle_center = None
        self.circle_radius = 0
        self.showing_white_cells = True
        self.drawing_square = False
        self.zoom_level = 1
        self.zoomed_grid = None
        self.zoom_active = False
        self.zoom_pos = (0, 0)
        self.CELL_SIZE = 20
        self.ROWS = 20
        self.COLS = 20
        self.BUTTON_SIZE = 50
        self.BUTTON_PADDING = 5
        self.NUM_BUTTONS = 28
        self.GRID_WIDTH = self.COLS * self.CELL_SIZE
        self.GRID_HEIGHT = self.ROWS * self.CELL_SIZE
        self.WIDTH = self.GRID_WIDTH + 2 * (self.BUTTON_SIZE + 10)
        self.HEIGHT = self.GRID_HEIGHT + 2 * (self.BUTTON_SIZE + 10)
        self.GRID_X_OFFSET = (self.WIDTH - self.GRID_WIDTH) // 2
        self.GRID_Y_OFFSET = (self.HEIGHT - self.GRID_HEIGHT) // 2

        # Configuración de la pantalla y título de la ventana
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Pixaint')

        # Definición de colores y símbolos de los botones
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BORDER_COLOR = self.BLACK
        self.BUTTON_COLORS = [
            (255, 0, 0),  # Rojo (Botón 18)
            (152, 251, 152),  # Verde claro (Botón 19)
            (0, 0, 255),  # Azul (Botón 20)
            (255, 255, 0),  # Amarillo (Botón 21)
            (255, 192, 203),  # Rosado (Botón 22)
            (0, 255, 255),  # Celeste (Botón 23)
            (128, 128, 128),  # Gris (Botón 24)
            (255, 165, 0),  # Naranja (Botón 25)
            (128, 0, 128),  # Morado (Botón 26)
            (0, 128, 0),  # Verde oscuro (Botón 27)
            (255, 0, 255),  # Blanco (Botón 28)
        ]
        self.BUTTON_SYMBOLS = [
            ".", ":", "-", "=", "¡", "&", "$", "%", "@", "+", "#"
        ]
        self.button_images = []
        for i in range(1, 18):
            image_path = f"Pixaint-main/imagenes_pixaint/boton_{i}.png"
            self.button_images.append(pygame.image.load(image_path))

        # Creación de la cuadrícula y lista de botones
        self.grid = [[self.WHITE] * self.COLS for _ in range(self.ROWS)]
        self.original_grid = [[self.WHITE] * self.COLS for _ in range(self.ROWS)]
        self.buttons = []
        # Creamos los rectángulos para los botones y su texto asociado
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET - self.BUTTON_SIZE - 10,
                                                     self.GRID_Y_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING),
                                                     self.BUTTON_SIZE, self.BUTTON_SIZE), "text": f"Botón {i + 1}"})
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET + self.GRID_WIDTH + 10,
                                                     self.GRID_Y_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING),
                                                     self.BUTTON_SIZE, self.BUTTON_SIZE),
                                 "text": f"Botón {i + 1 + self.NUM_BUTTONS // 4}"})
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING),
                                                     self.GRID_Y_OFFSET - self.BUTTON_SIZE - 10, self.BUTTON_SIZE,
                                                     self.BUTTON_SIZE),
                                 "text": f"Botón {i + 1 + self.NUM_BUTTONS // 2}"})
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING),
                                                     self.GRID_Y_OFFSET + self.GRID_HEIGHT + 10, self.BUTTON_SIZE,
                                                     self.BUTTON_SIZE),
                                 "text": f"Botón {i + 1 + 3 * (self.NUM_BUTTONS // 4)}"})
        self.selected_color = self.WHITE
        self.showing_numbers = False
        self.showing_symbols = False
        self.showing_high_contrast = False
        self.showing_negative = False

    def run(self):
        # Bucle principal del juego
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    self.eraser()

            self.draw()

        pygame.quit()
        sys.exit()

    def handle_mouse_click(self, mouse_pos):
        button_clicked = False
        for idx, button in enumerate(self.buttons[17:]):
            if button["rect"].collidepoint(mouse_pos):
                self.selected_color = self.BUTTON_COLORS[idx]
                if self.using_eraser:
                    self.using_eraser = False
                button_clicked = True
                break
        if not button_clicked:
            for idx, button in enumerate(self.buttons):
                if button["rect"].collidepoint(mouse_pos):
                    if idx == 0:  # Botón 1 para zoom in
                        if self.zoom_level > 1:
                            self.zoom_level -= 1
                        else:
                            self.zoom_level = 2
                        self.zoom_active = True
                        self.handle_zoom(mouse_pos)
                        button_clicked = True
                        break
                    elif idx == 1:  # Botón 2 para zoom out
                        if self.zoom_level < 1:
                            self.zoom_level = 1
                        else:
                            self.zoom_level -= 1
                        self.zoom_active = True
                        self.handle_zoom(mouse_pos)
                        button_clicked = True
                        break
                    elif idx == 2: # Boton 3 para dibujar circulo
                        self.drawing_circle = not self.drawing_circle
                        self.circle_center = None
                        button_clicked = True
                        break
                    elif idx == 3:  # Botón 4 para dibujar cuadrado
                        self.drawing_square = not self.drawing_square
                        self.square_start = None
                        self.square_end = None
                        button_clicked = True
                        break
                    elif idx == 4: # Boton 5 para usar borrador
                        while not (self.showing_numbers or self.showing_symbols or self.showing_high_contrast):
                            self.using_eraser = not self.using_eraser
                            self.eraser()
                            button_clicked = True
                            break
                    elif idx == 5: # Boton 6 para limpiar la cuadricula
                        self.clear_grid()
                        button_clicked = True
                        break
                    elif idx == 6: # Boton 7 para guardar imagen
                        self.save_grid()
                        button_clicked = True
                        break
                    elif idx == 7: # Boton 8 para cargar imagen
                        self.load_grid()
                        button_clicked = True
                        break
                    elif idx == 8: # Boton 9 para rotar a la derecha
                        self.rotate_right()
                        button_clicked = True
                        break
                    elif idx == 9: # Boton 10 para rotar a la izquierda
                        self.rotate_left()
                        button_clicked = True
                        break
                    elif idx == 10: # Boton 11 para alternar a alto contraste
                        self.toggle_high_contrast()
                        button_clicked = True
                        break
                    elif idx == 11: # Boton 12 para alternar a colores negativos
                        self.toggle_negative()
                        button_clicked = True
                        break
                    elif idx == 12: # Boton 13 para reflejo horizontal
                        self.reflect_horiz()
                        button_clicked = True
                        break
                    elif idx == 13: # Boton 14 para reflejo vertical
                        self.reflect_vert()
                        button_clicked = True
                        break
                    elif idx == 14: # Boton 15 para mostrar solo el dibujo
                        self.toggle_white_cells()
                        button_clicked = True
                        break
                    elif idx == 15: # Boton 16 para cambiar los colores a numeros
                        self.toggle_grid()
                        button_clicked = True
                        break
                    elif idx == 16: # Boton 17 para cambiar los colores a simbolos
                        self.toggle_symbols()
                        button_clicked = True
                        break
            if not button_clicked and not self.using_eraser:
                if self.zoom_active:
                    self.handle_zoom(mouse_pos)
                else:
                    grid_x = (mouse_pos[0] - self.GRID_X_OFFSET) // self.CELL_SIZE
                    grid_y = (mouse_pos[1] - self.GRID_Y_OFFSET) // self.CELL_SIZE
                    if 0 <= grid_x < self.COLS and 0 <= grid_y < self.ROWS:
                        if self.drawing_circle:
                            if self.circle_center is None:
                                self.circle_center = (grid_x, grid_y)
                            else:
                                dx = grid_x - self.circle_center[0]
                                dy = grid_y - self.circle_center[1]
                                self.circle_radius = int((dx ** 2 + dy ** 2) ** 0.5)
                                self.draw_circle()
                                self.drawing_circle = False
                                self.circle_center = None
                                self.circle_radius = 0
                        elif self.drawing_square:
                            if self.square_start is None:
                                self.square_start = (grid_x, grid_y)
                            else:
                                self.square_end = (grid_x, grid_y)
                                self.draw_square()
                                self.drawing_square = False
                                self.square_start = None
                                self.square_end = None
                        else:
                            self.grid[grid_y][grid_x] = self.selected_color

    def save_grid(self):
        # Función para guardar la cuadrícula en un archivo de texto
        if not os.path.exists('Pixaint-main/imagenes_guardadas'):
            os.makedirs('Pixaint-main/imagenes_guardadas')
        # Generar el nombre del archivo basado en la fecha y hora actuales
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join('Pixaint-main/imagenes_guardadas', f'pixaint_grid_{timestamp}.txt')
        with open(filename, 'w') as file:
            for row in self.grid:
                file.write(' '.join(str(self.color_to_number(cell)) for cell in row) + '\n')
        print(f"Cuadrícula guardada en {filename}")

    def load_grid(self):
        # Función para cargar la cuadrícula desde un archivo de texto usando un diálogo de selección de archivos
        Tk().withdraw()  # Oculta la ventana principal de Tkinter
        filepath = filedialog.askopenfilename(
            initialdir="Pixaint-main/imagenes_guardadas",
            title="Seleccione el archivo de cuadrícula",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not filepath:
            print("No se seleccionó ningún archivo.")
            return
        with open(filepath, 'r') as file:
            for row_idx, line in enumerate(file):
                numbers = line.strip().split(' ')
                for col_idx, number in enumerate(numbers):
                    if row_idx < self.ROWS and col_idx < self.COLS:
                        self.grid[row_idx][col_idx] = self.number_to_color(int(number))  # Convertir número a color
        print(f"Cuadrícula cargada desde {filepath}")

    def handle_zoom(self, mouse_pos):
        # Función para manejar el zoom de la cuadrícula
        grid_x = (mouse_pos[0] - self.GRID_X_OFFSET) // self.CELL_SIZE
        grid_y = (mouse_pos[1] - self.GRID_Y_OFFSET) // self.CELL_SIZE
        if 0 <= grid_x < self.COLS and 0 <= grid_y < self.ROWS:
            self.zoom_pos = (grid_x, grid_y)
            self.update_zoomed_grid()

    def update_zoomed_grid(self):
        # Actualizar la cuadrícula en la ventana de zoom
        if self.zoom_level == 1:
            self.zoom_active = False
            self.zoomed_grid = None
            return

        zrows = self.ROWS // self.zoom_level
        zcols = self.COLS // self.zoom_level
        zx, zy = self.zoom_pos
        start_row = max(0, zy - zrows // 2)
        end_row = min(self.ROWS, zy + zrows // 2)
        start_col = max(0, zx - zcols // 2)
        end_col = min(self.COLS, zx + zcols // 2)

        self.zoomed_grid = [row[start_col:end_col] for row in self.grid[start_row:end_row]]

    def draw(self):
        # Dibujar la cuadrícula en la ventana
        self.screen.fill(self.WHITE)
        for idx, button in enumerate(self.buttons):
            if idx < 17:
                self.screen.blit(self.button_images[idx], button["rect"].topleft)
            else:
                color = self.BUTTON_COLORS[idx - 17]
                if idx == 3 and self.drawing_circle:  # Botón 4 resaltado cuando está activo
                    color = (color[0] // 2, color[1] // 2, color[2] // 2)
                pygame.draw.rect(self.screen, color, button["rect"], border_radius=5)
        if self.zoom_active and self.zoomed_grid:
            for row in range(len(self.zoomed_grid)):
                for col in range(len(self.zoomed_grid[0])):
                    rect = pygame.Rect(self.GRID_X_OFFSET + col * self.CELL_SIZE, self.GRID_Y_OFFSET + row * self.CELL_SIZE,
                                    self.CELL_SIZE * self.zoom_level, self.CELL_SIZE * self.zoom_level)
                    color = self.zoomed_grid[row][col]
                    if color == self.WHITE and not self.showing_white_cells:
                        continue  # Si la opción de mostrar celdas blancas está desactivada, se omite el dibujo de la celda
                    if self.showing_numbers and isinstance(color, int):
                        text_surface = pygame.font.SysFont(None, 24).render(str(color), True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    elif self.showing_symbols and isinstance(color, str):
                        text_surface = pygame.font.SysFont(None, 24).render(color, True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    else:
                        pygame.draw.rect(self.screen, color if not isinstance(color, int) else self.WHITE, rect)
                        pygame.draw.rect(self.screen, self.BORDER_COLOR, rect, 1)
        else:
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    rect = pygame.Rect(self.GRID_X_OFFSET + col * self.CELL_SIZE, self.GRID_Y_OFFSET + row * self.CELL_SIZE,
                                    self.CELL_SIZE, self.CELL_SIZE)
                    color = self.grid[row][col]
                    if color == self.WHITE and not self.showing_white_cells:
                        continue  # Si la opción de mostrar celdas blancas está desactivada, se omite el dibujo de la celda
                    if self.showing_numbers and isinstance(color, int):
                        text_surface = pygame.font.SysFont(None, 24).render(str(color), True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    elif self.showing_symbols and isinstance(color, str):
                        text_surface = pygame.font.SysFont(None, 24).render(color, True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    else:
                        pygame.draw.rect(self.screen, color if not isinstance(color, int) else self.WHITE, rect)
                        pygame.draw.rect(self.screen, self.BORDER_COLOR, rect, 1)

        pygame.display.flip()

    def color_to_number(self, color):
        # Función para convertir un color en su número correspondiente
        if color == self.WHITE:
            return 0
        for idx, col in enumerate(self.BUTTON_COLORS):
            if color == col:
                return idx + 1
        return -1

    def toggle_grid(self):
        # Alterna entre colores, numeros o simbolos
        if self.showing_symbols:
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    self.grid[row][col] = self.symbol_to_number(self.grid[row][col])
            self.showing_symbols = False
            self.showing_numbers = True
        else:
            self.showing_numbers = not self.showing_numbers
            if self.showing_numbers:
                self.original_grid = [row[:] for row in self.grid]
                for row in range(self.ROWS):
                    for col in range(self.COLS):
                        self.grid[row][col] = self.color_to_number(self.grid[row][col])
            else:
                self.grid = [row[:] for row in self.original_grid]

    def color_to_symbol(self, color):
        # Convertir colores a símbolos
        if color == self.WHITE:
            return ""
        for idx, col in enumerate(self.BUTTON_COLORS):
            if color == col:
                return self.BUTTON_SYMBOLS[idx % len(self.BUTTON_SYMBOLS)]
        return "?"

    def toggle_symbols(self):
        # Alterna entre colores, numeros o simbolos
        if self.showing_numbers:
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    self.grid[row][col] = self.number_to_symbol(self.grid[row][col])
            self.showing_numbers = False
            self.showing_symbols = True
        else:
            self.showing_symbols = not self.showing_symbols
            if self.showing_symbols:
                for row in range(self.ROWS):
                    for col in range(self.COLS):
                        self.grid[row][col] = self.color_to_symbol(self.grid[row][col])
            else:
                for row in range(self.ROWS):
                    for col in range(self.COLS):
                        self.grid[row][col] = self.symbol_to_color(self.grid[row][col])

    def clear_grid(self):
        # Limpia la cuadrícula
        self.showing_numbers = False
        self.showing_symbols = False
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.grid[row][col] = self.WHITE

    def symbol_to_color(self, symbol):
        # Función para convertir un símbolo en su color correspondiente
        if symbol == "":
            return self.WHITE
        for idx, sym in enumerate(self.BUTTON_SYMBOLS):
            if symbol == sym:
                return self.BUTTON_COLORS[idx]
        return self.WHITE

    def number_to_color(self, number):
        # Función para convertir un número en su color correspondiente
        if number == 0:
            return self.WHITE
        elif 1 <= number <= len(self.BUTTON_COLORS):
            return self.BUTTON_COLORS[number - 1]
        return self.WHITE

    def rotate_right(self):
        # Rota la matriz hacia la derecha
        transposed_grid = [[self.grid[col][row] for col in range(self.ROWS)] for row in range(self.COLS)]
        for row in range(self.ROWS):
            transposed_grid[row] = transposed_grid[row][::-1]
        self.grid = transposed_grid

    def rotate_left(self):
        # Rota la matriz a la izquierda
        for col in range(self.COLS):
            self.grid[col] = self.grid[col][::-1]
        self.grid = [[self.grid[row][col] for row in range(self.COLS)] for col in range(self.ROWS)]

    def reflect_vert(self):
        # Refleja el dibujo a partir del eje vertical
        for row in range(self.ROWS):
            for col in range(self.COLS // 2):
                self.grid[row][col], self.grid[row][self.COLS - 1 - col] = self.grid[row][self.COLS - 1 - col], \
                self.grid[row][col]

    def reflect_horiz(self):
        # Refleja el dibujo a partir del eje horizontal
        for col in range(self.COLS):
            for row in range(self.ROWS // 2):
                self.grid[row][col], self.grid[self.ROWS - 1 - row][col] = self.grid[self.ROWS - 1 - row][col], \
                self.grid[row][col]

    def symbol_to_number(self, symbol):
        # Alterna entre simbolo y numero
        if symbol == "":
            return 0
        for idx, sym in enumerate(self.BUTTON_SYMBOLS):
            if symbol == sym:
                return idx + 1
        return -1

    def number_to_symbol(self, number):
        # Alterna entre numero y simbolo
        if number == 0:
            return ""
        elif 1 <= number <= len(self.BUTTON_SYMBOLS):
            return self.BUTTON_SYMBOLS[number - 1]
        return "?"

    def draw_circle(self):
        # Dibuja un circulo
        if self.circle_center is None or self.circle_radius == 0:
            return
        cx, cy = self.circle_center
        for row in range(self.ROWS):
            for col in range(self.COLS):
                dx = col - cx
                dy = row - cy
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance <= self.circle_radius:
                    self.grid[row][col] = self.selected_color

    def eraser(self):
        # Activa el borrador, cuando pasemos por encima del dibujo se iran borrando los colores
        if not self.using_eraser:
            return
        mouse_pos = pygame.mouse.get_pos()
        grid_x = (mouse_pos[0] - self.GRID_X_OFFSET) // self.CELL_SIZE
        grid_y = (mouse_pos[1] - self.GRID_Y_OFFSET) // self.CELL_SIZE
        if 0 <= grid_x < self.COLS and 0 <= grid_y < self.ROWS:
            self.grid[grid_y][grid_x] = self.WHITE

    def high_contrast(self, color):
        # Cambia el color a un color de contraste alto
        if color == self.WHITE:
            return self.WHITE
        elif color in self.BUTTON_COLORS[:5]:
            return self.BUTTON_COLORS[0]
        elif color in self.BUTTON_COLORS[5:11]:
            return self.BUTTON_COLORS[6]
        else:
            return color

    def toggle_high_contrast(self):
        # Alterna entre contraste alto y normal
        if self.showing_high_contrast:
            self.grid = [row[:] for row in self.original_grid]
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = False
        else:
            self.original_grid = [row[:] for row in self.grid]
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    self.grid[row][col] = self.high_contrast(self.grid[row][col])
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = True

    def negative(self, color):
        # Cambia el color a su negativo
        if color == self.WHITE:
            return self.WHITE

        mapping = {self.BUTTON_COLORS[i]: self.BUTTON_COLORS[-(i + 1)] for i in range(len(self.BUTTON_COLORS))}

        return mapping.get(color, color)

    def toggle_negative(self):
        # Alterna entre negativo y positivo
        if self.showing_negative:
            self.grid = [row[:] for row in self.original_grid]
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = False
            self.showing_negative = False
        else:
            self.original_grid = [row[:] for row in self.grid]
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    self.grid[row][col] = self.negative(self.grid[row][col])
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = False
            self.showing_negative = True

    def toggle_white_cells(self):
        # Alterna entre mostrar y no mostrar las celdas en blanco para mostrar el dibujo
        self.showing_white_cells = not self.showing_white_cells

    def draw_square(self):
        # Dibuja un cuadrado
        if self.square_start is None or self.square_end is None:
            return
        x1, y1 = self.square_start
        x2, y2 = self.square_end
        start_col = min(x1, x2)
        end_col = max(x1, x2)
        start_row = min(y1, y2)
        end_row = max(y1, y2)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                self.grid[row][col] = self.selected_color

if __name__ == "__main__":
    game = Pixaint()
    game.run()
