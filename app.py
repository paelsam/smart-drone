import pygame
from helpers.process_map import process_map
from helpers.prompt_file import prompt_file
from helpers.sprite import Sprite

WIDTH = 600
HEIGHT = 600 

# Iniciando pygame 
pygame.init()

pygame.display.set_caption("Dron AI")

icon = pygame.image.load("./assets/img/drone.png")
window = pygame.display.set_mode((WIDTH, HEIGHT))
background_color = (255, 255, 255)

pygame.display.set_icon(icon)


# Proximamente, dejar que el usuario seleccione el archivo
# y mostrar la matriz en la ventana de pygame
matrix = None
file = ""

ROWS = 0
COLUMNS = 0
CELL_WIDTH = 0
CELL_HEIGHT = 0


# Dibujando la matriz en la ventana
# 0: Camino
# 1: Obstaculo
# 2: Inicio
# 3: Obtaculo pasable
# 4: Objetivos
def draw_matrix(matrix):

    for i in range(ROWS):
        for j in range(COLUMNS):
            if matrix[i][j] == 0:
                pygame.draw.rect(window, (255, 255, 255), (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            elif matrix[i][j] == 1:
                # Dibujar obstaculo
                wall = Sprite("./assets/img/wall.jpg", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                all_sprites_list.add(wall)
            elif matrix[i][j] == 2:
                # Crear sprite de dron
                dron = Sprite("./assets/img/drone.png", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                all_sprites_list.add(dron)
                drone_position = (i, j)
            elif matrix[i][j] == 3:
                # Dibujar obstaculo pasable
                electric_wall = Sprite("./assets/img/electric-wall.png", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                all_sprites_list.add(electric_wall)
            elif matrix[i][j] == 4:
                # Dibujar objetivo
                package = Sprite("./assets/img/package.jpg", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                all_sprites_list.add(package)

            pygame.draw.rect(window, (0, 0, 0), (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 2)
    
    
    
 
all_sprites_list = pygame.sprite.Group() 

# FPS
clock = pygame.time.Clock() 



while True:

    # Si el usuario selecciona un archivo
    if file:
        matrix = process_map(file)

        ROWS = len(matrix)
        COLUMNS = len(matrix[0])
        CELL_WIDTH = WIDTH // COLUMNS
        CELL_HEIGHT = HEIGHT // ROWS

        # Antes de dibunjdar la matriz, limpiar los sprites
        all_sprites_list.empty()

        draw_matrix(matrix)
        file = ""
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                file = prompt_file()
    
    all_sprites_list.update() 
    window.fill(background_color)
    all_sprites_list.draw(window)
    draw_matrix(matrix)
    pygame.display.flip()
    clock.tick(60)

