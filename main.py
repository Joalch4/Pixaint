import pygame
import sys
import os
from datetime import datetime
from tkinter import Tk, filedialog

class Pixaint:
    def __init__(self):
        pygame.init()
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

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Pixaint')

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BORDER_COLOR = self.BLACK
        self.BUTTON_COLORS = [
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
        self.BUTTON_SYMBOLS = [
            ".", ":", "-", "=", "¡", "&", "$", "%", "@", "+", "#"
        ]
        self.button_images = []
        for i in range(1, 18):
            image_path = f"Pixaint-main/imagenes_pixaint/boton_{i}.png"
            self.button_images.append(pygame.image.load(image_path))

        self.grid = [[self.WHITE] * self.COLS for _ in range(self.ROWS)]
        self.original_grid = [[self.WHITE] * self.COLS for _ in range(self.ROWS)]
        self.buttons = []
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET - self.BUTTON_SIZE - 10, self.GRID_Y_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING), self.BUTTON_SIZE, self.BUTTON_SIZE), "text": f"Botón {i+1}"})
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET + self.GRID_WIDTH + 10, self.GRID_Y_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING), self.BUTTON_SIZE, self.BUTTON_SIZE), "text": f"Botón {i+1+self.NUM_BUTTONS//4}"})
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING), self.GRID_Y_OFFSET - self.BUTTON_SIZE - 10, self.BUTTON_SIZE, self.BUTTON_SIZE), "text": f"Botón {i+1+self.NUM_BUTTONS//2}"})
        for i in range(self.NUM_BUTTONS // 4):
            self.buttons.append({"rect": pygame.Rect(self.GRID_X_OFFSET + i * (self.BUTTON_SIZE + self.BUTTON_PADDING), self.GRID_Y_OFFSET + self.GRID_HEIGHT + 10, self.BUTTON_SIZE, self.BUTTON_SIZE), "text": f"Botón {i+1+3*(self.NUM_BUTTONS//4)}"})
        self.selected_color = self.WHITE
        self.showing_numbers = False
        self.showing_symbols = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)

            self.draw()
            
        pygame.quit()
        sys.exit()

    def handle_mouse_click(self, mouse_pos):
        button_clicked = False
        for idx, button in enumerate(self.buttons[17:]):
            if button["rect"].collidepoint(mouse_pos):
                self.selected_color = self.BUTTON_COLORS[idx]
                button_clicked = True
                break
        if not button_clicked:
            for idx, button in enumerate(self.buttons):
                if button["rect"].collidepoint(mouse_pos):
                    if idx == 5:
                        self.save_grid()
                        button_clicked = True
                        break
                    elif idx == 2:
                        self.load_grid()
                        button_clicked = True
                        break
                    elif idx == 13:  
                        self.toggle_grid()
                        button_clicked = True
                        break
                    elif idx == 16:
                        self.toggle_symbols()
                        button_clicked = True
                        break
                    elif idx == 15:
                        self.clear_grid()
                        button_clicked = True
                        break
            if not button_clicked:
                grid_x = (mouse_pos[0] - self.GRID_X_OFFSET) // self.CELL_SIZE
                grid_y = (mouse_pos[1] - self.GRID_Y_OFFSET) // self.CELL_SIZE
                if 0 <= grid_x < self.COLS and 0 <= grid_y < self.ROWS:
                    self.grid[grid_y][grid_x] = self.selected_color

    def save_grid(self):
        if not os.path.exists('Pixaint-main/imagenes_guardadas'):
            os.makedirs('Pixaint-main/imagenes_guardadas')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join('Pixaint-main/imagenes_guardadas', f'pixaint_grid_{timestamp}.txt')
        with open(filename, 'w') as file:
            for row in self.grid:
                file.write(' '.join(str(self.color_to_number(cell)) for cell in row) + '\n')
        print(f"Cuadrícula guardada en {filename}")

    def load_grid(self):
        Tk().withdraw()
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
                        self.grid[row_idx][col_idx] = self.number_to_color(int(number))
        print(f"Cuadrícula cargada desde {filepath}")

    def draw(self):
        self.screen.fill(self.WHITE)
        for idx, button in enumerate(self.buttons):
            if idx < 17:
                self.screen.blit(self.button_images[idx], button["rect"].topleft)
            else:
                pygame.draw.rect(self.screen, self.BUTTON_COLORS[idx - 17], button["rect"], border_radius=5)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                rect = pygame.Rect(self.GRID_X_OFFSET + col * self.CELL_SIZE, self.GRID_Y_OFFSET + row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                color = self.grid[row][col]
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
        if color == self.WHITE:
            return 0
        for idx, col in enumerate(self.BUTTON_COLORS):
            if color == col:
                return idx + 1
        return -1

    def toggle_grid(self):
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
        if color == self.WHITE:
            return ""
        for idx, col in enumerate(self.BUTTON_COLORS):
            if color == col:
                return self.BUTTON_SYMBOLS[idx % len(self.BUTTON_SYMBOLS)]
        return "?"

    def toggle_symbols(self):
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
        self.showing_numbers = False
        self.showing_symbols = False
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.grid[row][col] = self.WHITE

    def symbol_to_color(self, symbol):
        if symbol == "":
            return self.WHITE
        for idx, sym in enumerate(self.BUTTON_SYMBOLS):
            if symbol == sym:
                return self.BUTTON_COLORS[idx]
        return self.WHITE

    def number_to_color(self, number):
        if number == 0:
            return self.WHITE
        elif 1 <= number <= len(self.BUTTON_COLORS):
            return self.BUTTON_COLORS[number - 1]
        return self.WHITE

    def symbol_to_number(self, symbol):
        if symbol == "":
            return 0
        for idx, sym in enumerate(self.BUTTON_SYMBOLS):
            if symbol == sym:
                return idx + 1
        return -1

    def number_to_symbol(self, number):
        if number == 0:
            return ""
        elif 1 <= number <= len(self.BUTTON_SYMBOLS):
            return self.BUTTON_SYMBOLS[number - 1]
        return "?"

if __name__ == "__main__":
    game = Pixaint()
    game.run()
