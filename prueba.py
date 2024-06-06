import pygame
import sys
import os
from datetime import datetime
from tkinter import Tk, filedialog

class Pixaint:
    def __init__(self):
        # Inicialización de Pygame, definición de constantes y definicion de estados iniciales de variables
        pygame.init()
        # Variables de dibujo de cuadriculas y edicion en general
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
        # Constantes que definen la interfaz como tamaño de ventana, celdas, cuadricula, posiciones, etc
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

        # Configuración de la pantalla, título de la ventana e iconno de la ventana
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('PIXAINT')
        icono = pygame.image.load("Pixaint-main/imagenes_pixaint/icono.png")
        pygame.display.set_icon(icono)

        # Colores de la interfaz 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BORDER_COLOR = self.BLACK
        # Colores de los botones para pintar
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
        # Simbolos asignados a los numeros
        self.BUTTON_SYMBOLS = [
            ".", ":", "-", "=", "¡", "&", "$", "%", "@", "+", "#"
        ]
        # Imagenes de los botones
        self.button_images = []
        for i in range(1, 18):
            image_path = f"Pixaint-main/imagenes_pixaint/boton_{i}.png"
            self.button_images.append(pygame.image.load(image_path))

        # Inicializa la cuadricula como una matriz con las celdas en color blanco
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
        # Estado inicial de algunas variables
        self.selected_color = self.WHITE
        self.showing_numbers = False
        self.showing_symbols = False
        self.showing_high_contrast = False
        self.showing_negative = False

    def run(self):
        # Bucle principal del programa
        running = True
        while running:
            # Recorre todos los eventos que suceden a lo largo del programa (clics del mouse, botones presionados etc)
            for event in pygame.event.get():
                # Cuando running es falso termina el loop y llama a pygame.quit()
                if event.type == pygame.QUIT:
                    running = False
                # Cuando se presiona el click izquierdo del mouse se llama el metodo
                # handle_mouse_click con la posicion del evento como argumento
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)
                # Cuando el click izquierdo esta siendo presionado se llama a eraser y si es verdadero
                # borra todas las celdas por donde pasa el cursor, si es falso se ignora
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    self.eraser()
            # Llama el metodo draw para actualizar el estado de la cuadricula
            self.draw()
        # Finaliza la bilbioteca de Pygame y termina el programa
        pygame.quit()
        # Sale del interprete de python y termina el programa
        sys.exit()

    def handle_mouse_click(self, mouse_pos):
        # Manejo de los clicks de botones, el break en cada boton es para que no se siga haciendo la accion, o sea que para volver a realizar la accion se debe presionar el boton otra vez
        button_clicked = False
        # Se enumeran todos los colores del 1 al 11 [el 0 seria el blanco (vacio)]
        for idx, button in enumerate(self.buttons[17:]):
            # Toma la posicion del click y si esta seleccionado un color pinta la celda
            if button["rect"].collidepoint(mouse_pos):
                self.selected_color = self.BUTTON_COLORS[idx]
                if self.using_eraser:
                    self.using_eraser = False
                button_clicked = True
                break
        # Si no se selecciono ninguna celda verifica si fue seleccionado algun boton
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
            # Si no esta seleccionado ningun boton, no esta activado el borrador y no esta activado el zoom
            # toma la posicion del click para dibujar un circulo o cuadrado
            if not button_clicked and not self.using_eraser:
                if self.zoom_active:
                    self.handle_zoom(mouse_pos)
                else:
                    grid_x = (mouse_pos[0] - self.GRID_X_OFFSET) // self.CELL_SIZE
                    grid_y = (mouse_pos[1] - self.GRID_Y_OFFSET) // self.CELL_SIZE
                    if 0 <= grid_x < self.COLS and 0 <= grid_y < self.ROWS:
                        # Manejo de la creacion de un ciruclo
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
                        # Manejo de la creacion de un cuadrado/rectangulo
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
        # Si la carpeta imagenes_guardadas no existe se crea
        if not os.path.exists('Pixaint-main/imagenes_guardadas'):
            os.makedirs('Pixaint-main/imagenes_guardadas')
        # Genera el nombre del archivo basado en la fecha y hora actuales
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join('Pixaint-main/imagenes_guardadas', f'pixaint_grid_{timestamp}.txt')
        # Abre el archivo en modo escritura
        with open(filename, 'w') as file:
            # Convierte cada celda en su numero asignado y lo escribe en el archivo txt
            for row in self.grid:
                file.write(' '.join(str(self.color_to_number(cell)) for cell in row) + '\n')
        # Manda mensaje de exito
        print(f"Cuadrícula guardada en {filename}")

    def load_grid(self):
        # Función para cargar la cuadrícula desde un archivo de texto usando un diálogo de selección de archivos
        Tk().withdraw()  # Oculta la ventana principal de Tkinter
        # Abre la aplicacion de archivos para seleccionar una imagen
        filepath = filedialog.askopenfilename(
            initialdir="Pixaint-main/imagenes_guardadas",
            title="Seleccione el archivo de cuadrícula",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        # Si no selecciona un archivo manda mensaje de que no se selecciono ninguno
        if not filepath:
            print("No se seleccionó ningún archivo.")
            return
        # Abre el archivo en modo lectura
        with open(filepath, 'r') as file:
            # Lee el valor de cada celda de la fila y columna por separado
            for row_idx, line in enumerate(file):
                numbers = line.strip().split(' ')
                for col_idx, number in enumerate(numbers):
                    # Convierte el valor de la celda al color asignado
                    if row_idx < self.ROWS and col_idx < self.COLS:
                        self.grid[row_idx][col_idx] = self.number_to_color(int(number))
        # Manda mensaje de exito
        print(f"Cuadrícula cargada desde {filepath}")

    def handle_zoom(self, mouse_pos):
        # Obtiene la posicion del click del mouse
        grid_x = (mouse_pos[0] - self.GRID_X_OFFSET) // self.CELL_SIZE
        grid_y = (mouse_pos[1] - self.GRID_Y_OFFSET) // self.CELL_SIZE
        # Calcula si el click del mouse fue dentro de la cuadricula y si es verdadero llama al metodo update_zoomed_grid
        if 0 <= grid_x < self.COLS and 0 <= grid_y < self.ROWS:
            self.zoom_pos = (grid_x, grid_y)
            self.update_zoomed_grid()

    def update_zoomed_grid(self):
        # Si el zoom_level es 1 devuelve a los estado iniciales del zoom
        if self.zoom_level == 1:
            self.zoom_active = False
            self.zoomed_grid = None
            return
        # calcula cantidad de filas y columnas que se deben mostrar en el zoom basado en el zoom_level
        zrows = self.ROWS // self.zoom_level
        zcols = self.COLS // self.zoom_level
        zx, zy = self.zoom_pos
        # Calcula el comienzo y el final de la cuadricula cuando esta en zoom basado en la posicion del zoom y el zoom_level
        start_row = max(0, zy - zrows // 2)
        end_row = min(self.ROWS, zy + zrows // 2)
        start_col = max(0, zx - zcols // 2)
        end_col = min(self.COLS, zx + zcols // 2)
        # Crea la cuadricula con zoom 
        self.zoomed_grid = [row[start_col:end_col] for row in self.grid[start_row:end_row]]

    def draw(self):
        # Dibujar la cuadrícula en la ventana
        self.screen.fill(self.WHITE)
        # Dibuja los botones
        for idx, button in enumerate(self.buttons):
            # Para los botones en posicion menor que 17 toma las imagenes que estan definidas en button_images
            if idx < 17:
                self.screen.blit(self.button_images[idx], button["rect"].topleft)
            else:
                # Si la posicion es mayor a 17 toma los colores de button_colors para dibujarlos
                color = self.BUTTON_COLORS[idx - 17]
                if idx == 3 and self.drawing_circle:
                    color = (color[0] // 2, color[1] // 2, color[2] // 2)
                pygame.draw.rect(self.screen, color, button["rect"], border_radius=5)
        # Si el zoom esta activo y el zoomed_grid no esta vacio hace zoom en la posicion de la cuadricula que yo presione
        if self.zoom_active and self.zoomed_grid:
            for row in range(len(self.zoomed_grid)):
                for col in range(len(self.zoomed_grid[0])):
                    rect = pygame.Rect(self.GRID_X_OFFSET + col * self.CELL_SIZE, self.GRID_Y_OFFSET + row * self.CELL_SIZE,
                                    self.CELL_SIZE * self.zoom_level, self.CELL_SIZE * self.zoom_level)
                    color = self.zoomed_grid[row][col]
                    # Si la opción de mostrar celdas blancas está desactivada, se omite el dibujo de la celda
                    if color == self.WHITE and not self.showing_white_cells:
                        continue
                    # Si esta activado la opcion de mostrar numeros o simbolos renderiza el zoom para mostrar estos
                    if self.showing_numbers and isinstance(color, int):
                        text_surface = pygame.font.SysFont(None, 24).render(str(color), True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    elif self.showing_symbols and isinstance(color, str):
                        text_surface = pygame.font.SysFont(None, 24).render(color, True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    else:
                        pygame.draw.rect(self.screen, color if not isinstance(color, int) else self.WHITE, rect)
                        pygame.draw.rect(self.screen, self.BORDER_COLOR, rect, 1)
        # Si el zoom no esta activo dibuja la cuadricula normal con los colores, simbolos o numeros en la posicion original
        else:
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    rect = pygame.Rect(self.GRID_X_OFFSET + col * self.CELL_SIZE, self.GRID_Y_OFFSET + row * self.CELL_SIZE,
                                    self.CELL_SIZE, self.CELL_SIZE)
                    color = self.grid[row][col]
                    # Si la opción de mostrar celdas blancas está desactivada, se omite el dibujo de la celda
                    if color == self.WHITE and not self.showing_white_cells:
                        continue
                    if self.showing_numbers and isinstance(color, int):
                        text_surface = pygame.font.SysFont(None, 24).render(str(color), True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    elif self.showing_symbols and isinstance(color, str):
                        text_surface = pygame.font.SysFont(None, 24).render(color, True, self.BLACK)
                        self.screen.blit(text_surface, rect.topleft)
                    else:
                        pygame.draw.rect(self.screen, color if not isinstance(color, int) else self.WHITE, rect)
                        pygame.draw.rect(self.screen, self.BORDER_COLOR, rect, 1)
        # Actualiza la ventana
        pygame.display.flip()

    def color_to_number(self, color): # Función para convertir un color en su número correspondiente
        # Si la celda es blanca (vacia) retorna 0
        if color == self.WHITE:
            return 0
        # Si la celda no esta vacia llama a BUTTON_COLORS y enumera los colores
        for idx, col in enumerate(self.BUTTON_COLORS):
            # Para cada color el metodo verifica si el color es igual a col, si lo es se suma 1 al index
            # por lo tanto esto dice que cada color tiene un valor asignado empezando por el 1
            if color == col:
                return idx + 1

    def toggle_grid(self): # Funcion que alterna entre simbolos, numeros y colores
        # Si showing_symbols es true ejecuta esta parte
        if self.showing_symbols:
            # Recorre cada celda con bucles anidados
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    # Convierte cada simbolo a su numero asignado
                    self.grid[row][col] = self.symbol_to_number(self.grid[row][col])
            # Despues de convertir todos los numeros a simbolos pone showing_symbols en false y showing_number en true
            self.showing_symbols = False
            self.showing_numbers = True
        else:
            # Si showing_symbols es false ejecuta esta parte y alterna el estado de showing_numbers (si estaba false ahora estara en true y viceversa)
            self.showing_numbers = not self.showing_numbers
            # Si showing_numbers esta en true despues de alternarlo se guarda una copia de la cuadricula en self.original_grid para restaurarla luego
            if self.showing_numbers:
                self.original_grid = [row[:] for row in self.grid]
                # Recorre cada celda
                for row in range(self.ROWS):
                    for col in range(self.COLS):
                        # Convierte cada color en su numero asignado utilizando color_to_number
                        self.grid[row][col] = self.color_to_number(self.grid[row][col])
            else:
                # Si showing_numbers esta en false despues de alternarlo reinicia la cuadricula desde self.grid
                # Recorre todas las celdas para convertir el numero a su color asignado usando number_to_color
                for row in range(self.ROWS):
                    for col in range(self.COLS):
                        self.grid[row][col] = self.number_to_color(self.grid[row][col])

    def color_to_symbol(self, color): # Funcion que convierte los colores en simbolos
        # Si la celda esta en blanco (vacia) retorna vacio, esto significa que el blanco no tiene color asignado por lo tanto se muestra un tipo de ASCII art
        if color == self.WHITE:
            return ""
        # Recorre la lista con enumerate que le proporciona el idx y el col
        for idx, col in enumerate(self.BUTTON_COLORS):
            # Si el color es igual al col, se devuelve el simbolo correspondiente
            if color == col:
                # Si el idx es mayor a la longitud de BUTTON_COLORS este se ajusta usando el modulo % para obtener un indice valido
                return self.BUTTON_SYMBOLS[idx % len(self.BUTTON_SYMBOLS)]

    def toggle_symbols(self): # Alterna entre colores, numeros o simbolos
        # Si showing_numbers es true se ejecuta esta parte
        if self.showing_numbers:
            # Recorre cada celda con bucles anidados
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    # Convierte cada numero a su simbolo asignado
                    self.grid[row][col] = self.number_to_symbol(self.grid[row][col])
            # Despues de convertir los numeros a sus simbolos asignados establece showing_numbers en false y showing_symbols en true
            self.showing_numbers = False
            self.showing_symbols = True
        else:
            # Si showing_numbers es false se ejecuta esta parte y alterna el estado de showing_symbols (si estaba en false ahora estara en true y viceversa)
            self.showing_symbols = not self.showing_symbols
            # Si showing_symbols esta en true despues de alternarlo se guarda una copia de la cuadricula en self.grid para restaurarla luego
            if self.showing_symbols:
                # Recorre cada celda
                for row in range(self.ROWS):
                    for col in range(self.COLS):
                        # Convierte cada numero a su simbolo asignado utilizando color_to_symbol
                        self.grid[row][col] = self.color_to_symbol(self.grid[row][col])
            else:
                # Si showing_symbols esta en false despues de alternarlo reinicia la cuadricula desde self.grid
                # Recorre todas las celdas para convertir el simbolo a su color asignado usando symbol_to_color
                for row in range(self.ROWS):
                    for col in range(self.COLS):
                        self.grid[row][col] = self.symbol_to_color(self.grid[row][col])

    def clear_grid(self): # Limpia la cuadricula
        # Establece showing_numbers y showing_symbols a false
        self.showing_numbers = False
        self.showing_symbols = False
        # Recorre las celdas
        for row in range(self.ROWS):
            for col in range(self.COLS):
                # Establece cada celda en blanco (vacia)
                self.grid[row][col] = self.WHITE

    def symbol_to_color(self, symbol): # Función para convertir un símbolo en su color correspondiente
        # Si el simbolo es "" (vacio) retorna la celda en blanco
        if symbol == "":
            return self.WHITE
        # El metodo busca en BUTTON_SYMBOLS usando enumerate los cual retorna el idx y el valor de cada elemento
        for idx, sym in enumerate(self.BUTTON_SYMBOLS):
            # Si symbol es igual a sym el metodo retorna el color asignado a cada idx en BUTTON_COLORS
            if symbol == sym:
                return self.BUTTON_COLORS[idx]

    def number_to_color(self, number): # Función para convertir un número en su color correspondiente
        # Si el numero es igual a 0 retorn la celda en blanco (vacia)
        if number == 0:
            return self.WHITE
        # Verifica si el numero esta entre 1 o la longitud de la lista BUTTON_COLORS
        elif 1 <= number <= len(self.BUTTON_COLORS):
            # Si esta entre este rango retorna el color asginado al idx correspondiente en BUTTON_COLORS
            return self.BUTTON_COLORS[number - 1]

    def rotate_right(self): # Rota la matriz hacia la derecha
        # Crea una nueva cuadricula llamada transposed_grid cambiando self.grid permutando los indices de las filas y columnas de cada elemento en la cuadricula
        transposed_grid = [[self.grid[col][row] for col in range(self.ROWS)] for row in range(self.COLS)]
        for row in range(self.ROWS):
            # El metodo cambia cada fila 90 grados hacia la derecha
            transposed_grid[row] = transposed_grid[row][::-1]
        # Actualiza la cuadricula para mostrarla rotada hacia la derecha
        self.grid = transposed_grid

    def rotate_left(self): # Rota la matriz a la izquierda
        # Recorre cada columna
        for col in range(self.COLS):
            # Cada columna se gira 90 grados hacia la izquierda
            self.grid[col] = self.grid[col][::-1]
        # Actualiza la cuadricula para mostrarla rotada hacia la izquierda
        self.grid = [[self.grid[row][col] for row in range(self.COLS)] for col in range(self.ROWS)]

    def reflect_vert(self): # Refleja el dibujo a partir del eje vertical
        # Recorre cada fila
        for row in range(self.ROWS):
            # Por cada fila itera cada columna hasta la mitad de la fila
            for col in range(self.COLS // 2):
                # Intercambia cada elemento de la columna actual y la columna correspondiente desde el final de la fila, esto da el efecto del reflejo vertical
                self.grid[row][col], self.grid[row][self.COLS - 1 - col] = self.grid[row][self.COLS - 1 - col], \
                self.grid[row][col]
                # Los cambios se hacen en la cuadricula original

    def reflect_horiz(self): # Refleja el dibujo a partir del eje horizontal
        # Recorre cada columna
        for col in range(self.COLS):
            # Por cada columna itera cada fila hasta la mitad de la columna
            for row in range(self.ROWS // 2):
                # Intercambia cada elemento de la fila actual y la fila correspondiente desde el final de la columna, esto da el efecto de reflejo horizontal
                self.grid[row][col], self.grid[self.ROWS - 1 - row][col] = self.grid[self.ROWS - 1 - row][col], \
                self.grid[row][col]
                # Los cambios se hacen en la cuadricula original

    def symbol_to_number(self, symbol): # Alterna entre simbolo y numero
        # Si el simbolo es igual "" (vacio) retorna 0 (vacio)
        if symbol == "":
            return 0
        # Recorre la lista BUTTON_SYMBOLS usando enumerate lo cual retorna el idx y el sym de cada elemento en la lista
        for idx, sym in enumerate(self.BUTTON_SYMBOLS):
            # Por cada simbolo en la lista BUTTON_SYMBOLS verifica si symbol es igual sym, si lo es retorna idx + 1
            if symbol == sym:
                return idx + 1

    def number_to_symbol(self, number): # Alterna entre numero y simbolo
        # Si el numero es igual a 0 (vacio) retorna "" (vacio)
        if number == 0:
            return ""
        # Si el numero esta entre 1 y la longitud de BUTTON_SYMBOLS retorna el simbolo asignado al numero - 1
        elif 1 <= number <= len(self.BUTTON_SYMBOLS):
            return self.BUTTON_SYMBOLS[number - 1]

    def draw_circle(self): # Dibuja un circulo
        # Verifica si circle_center no es None y si circle_radius es mayor a 0
        if self.circle_center is None or self.circle_radius == 0:
            return
        # Si ninguno de los dos cumple el metodo finaliza sin hacer nada
        cx, cy = self.circle_center
        # Recorre cada celda con bucles anidados
        for row in range(self.ROWS):
            for col in range(self.COLS):
                # Por cada celda, se calcula la distancia desde el centro del circulo usando teorema de pitagoras
                # cx y cy son el centro del circulo
                dx = col - cx
                dy = row - cy
                distance = (dx ** 2 + dy ** 2) ** 0.5
                # Si la distancia es menor o igual al circle_raidus significa que la celda esta dentro del circulo,
                # lo cual debe de colorear la celda del color seleccionado
                if distance <= self.circle_radius:
                    # Actualiza la cuadricula
                    self.grid[row][col] = self.selected_color

    def eraser(self): # Activa el borrador, cuando pasemos por encima del dibujo se iran borrando los colores
        # Verifica si using_eraser es false
        # Si es false finaliza el metodo sin hacer nada
        if not self.using_eraser:
            return
        # Obtiene posicion del mouse
        mouse_pos = pygame.mouse.get_pos()
        # Calcula la cordinada en x del mouse, esto lo hace sustrayendo GRID_X_OFFSET de la coordenada x del mouse, y lo divide por CELL_SIZE
        grid_x = (mouse_pos[0] - self.GRID_X_OFFSET) // self.CELL_SIZE
        # Calcula la cordinada en y del mouse, esto lo hace sustrayendo GRID_Y_OFFSET de la coordenada y del mouse, y lo divide por CELL_SIZE
        grid_y = (mouse_pos[1] - self.GRID_Y_OFFSET) // self.CELL_SIZE
        # Calcula si las coordenadas del mouse estan dentro de la cuadricula
        if 0 <= grid_x < self.COLS and 0 <= grid_y < self.ROWS:
            # Si las coordenadas estan dentro de la cuadricula pinta la celda a blanco para parecer que se borra
            self.grid[grid_y][grid_x] = self.WHITE

    def high_contrast(self, color): # Cambia el color a un color de contraste alto
        # Si la celda esta en blanco no se cambia
        if color == self.WHITE:
            return self.WHITE
        # Si la celda es de un color de los primeros 5 se cambia al color 0 (rojo)
        elif color in self.BUTTON_COLORS[:5]:
            return self.BUTTON_COLORS[0]
        # Si la celda es de un color que esta entre la posicion 6 y 11 se cambia al color 6 (gris)
        elif color in self.BUTTON_COLORS[5:11]:
            return self.BUTTON_COLORS[6]

    def toggle_high_contrast(self): # Alterna entre contraste alto y normal
        # Si showing_high_contrast es true ejecuta esta parte
        if self.showing_high_contrast:
            # Esta linea reinicia la cuadricula a su estado original copiando original_grid, esto nos dice que la cuadricula fue modificada
            self.grid = [row[:] for row in self.original_grid]
            # Establece showing_numbers, showing_symbols y showing_high_contrast en false lo cual dice que esta desactivado
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = False
        # Si showing_high_contrast es false ejecuta esta parte
        else:
            # Se guarda el estado actual de la cuadricula en origina_grid
            self.original_grid = [row[:] for row in self.grid]
            # Recorre todas las celdas con un bucle anidado
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    # Aplica el metodo high_contrast para cada celda de la cuadricula
                    self.grid[row][col] = self.high_contrast(self.grid[row][col])
            # Establec showing_numbers, showing_symbols en false y showing_high_contrast en true lo cual indica que esta activado
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = True

    def negative(self, color): # Cambia el color a su negativo
        # Si el color de la celda es blanco (vacio) retorna blanco (vacio)
        if color == self.WHITE:
            return self.WHITE
        # Crea un diccionario que asigna cada color en BUTTON_COLORS a su color negativo, esto lo hace con BUTTON_COLORS al reves
        mapping = {self.BUTTON_COLORS[i]: self.BUTTON_COLORS[-(i + 1)] for i in range(len(self.BUTTON_COLORS))}
        # Retorna el color negativo de cada color en la lista
        return mapping.get(color, color)

    def toggle_negative(self): # Alterna entre negativo y positivo
        # Si showing_negatives es true ejecuta esta parte del codigo
        if self.showing_negative:
            # Reinicia la cuadricula a su estado original, lo cual nos dice que la cuadricula fue modificada
            self.grid = [row[:] for row in self.original_grid]
            # Establece showing_numbers, showing_symbols, showing_high_contrast y showing_negative en false lo cual nos dice que esta desactivado
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = False
            self.showing_negative = False
        # Si showing_negative es false ejecuta esta parte del codigo
        else:
            # Guarda el estado de la cuadricula en original_grid
            self.original_grid = [row[:] for row in self.grid]
            # Se recorre cada celda con bucle anidado
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    # Aplica el metodo negative a cada celda
                    self.grid[row][col] = self.negative(self.grid[row][col])
            # Establece showing_numbers, showing_symbols, showing_high_contrast en false y showing_negative en true lo cual indica que esta activado
            self.showing_numbers = False
            self.showing_symbols = False
            self.showing_high_contrast = False
            self.showing_negative = True

    def toggle_white_cells(self): # Alterna entre mostrar y no mostrar las celdas en blanco para mostrar el dibujo
        # Si showing_white_cells es true ahora sera establecido en false lo cual escondera todas las celdas en blanco (vacias) y viceversa
        self.showing_white_cells = not self.showing_white_cells

    def draw_square(self): # Dibuja un cuadrado/rectangulo
        # Verifica si square_star o square_end es None
        if self.square_start is None or self.square_end is None:
            # Si los dos se cumplen finaliza el metodo sin dibujar nada
            return
        # Posicion de la primera esquina del cuadrado/rectangulo
        x1, y1 = self.square_start
        # Posicion de la segunda esquina del cuadrado/rectangulo
        x2, y2 = self.square_end
        # Calcula el incio de la columna del cuadrado/ rectangulo tomando el valor minimo de x1, x2
        start_col = min(x1, x2)
        # Calcula el final de la columna del cuadrado/rectangulo tomando el valor maximo de x1, x2
        end_col = max(x1, x2)
        # Calcula el inicio de la fila del cuadrado/rectangulo tomando el valor minimo de x1, x2
        start_row = min(y1, y2)
        # Calculo el final de la fila del cuadrado/rectangulo tomando el valor maximo de x1, x2
        end_row = max(y1, y2)
        # Recorre cada fila y columna del cuadrado para pintar todas las celdas
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                # Toma el color seleccionado y pinta todas las celdas donde se selecciono el cuadrado y actualiza la cuadricula
                self.grid[row][col] = self.selected_color

if __name__ == "__main__": # Mientras sea true se correra el programa
    game = Pixaint()
    game.run()
