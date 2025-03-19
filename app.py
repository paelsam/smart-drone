import pygame
from helpers.process_map import process_map
from helpers.prompt_file import prompt_file
from helpers.process_path import process_path
from helpers.sprite import Sprite
from classes.nodo import Nodo
from classes.nodoCU import NodoCU
from classes.nodoPD import NodoPD
from classes.nodoAV import NodoAvara


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
drone = ""
drone_position = (0, 0)
node_result = None

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
    
    global drone
    global drone_position

    for i in range(ROWS):
        for j in range(COLUMNS):
            if matrix[i][j] == 1:
                # Dibujar obstaculo
                wall = Sprite("./assets/img/wall.jpg", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                wall_sprites.add(wall)
            elif matrix[i][j] == 2:
                if not drone:  # Crear el dron solo si aún no existe
                    # Crear sprite de dron
                    drone = Sprite("./assets/img/drone.png", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                    drone_position = (i, j)
                    dinamic_sprites.add(drone)
            elif matrix[i][j] == 3:
                # Dibujar obstaculo pasable
                electric_wall = Sprite("./assets/img/electric-wall.png", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                electric_wall_sprites.add(electric_wall)
            elif matrix[i][j] == 4:
                # Dibujar objetivo
                package = Sprite("./assets/img/package.jpg", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                package_sprites.add(package)

            pygame.draw.rect(window, (0, 0, 0), (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 2)

def update_borders():
    for i in range(ROWS):
        for j in range(COLUMNS):
            pygame.draw.rect(window, (0, 0, 0), (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 2)
    
    
 
electric_wall_sprites = pygame.sprite.Group() 
wall_sprites = pygame.sprite.Group()
package_sprites = pygame.sprite.Group()
dinamic_sprites = pygame.sprite.Group()

# FPS
clock = pygame.time.Clock() 

# Evento para mover el drone
MOVE_EVENT = pygame.USEREVENT + 1
current_step = 0
ruta_finalizada = False  


while True:

    # Si el usuario selecciona un archivo
    if file:
        matrix = process_map(file)

        ROWS = len(matrix)
        COLUMNS = len(matrix[0])
        CELL_WIDTH = WIDTH // COLUMNS
        CELL_HEIGHT = HEIGHT // ROWS

        # Limpiar sprites y cargar la matriz y ruta solo cuando se carga el archivo
        electric_wall_sprites.empty()
        wall_sprites.empty()
        package_sprites.empty()
        
         
        node_result = process_path(matrix, NodoAvara)
        drone_position = node_result["player_position"]
        draw_matrix(matrix)  # Dibuja el fondo y crea el dron (si aún no existe)
        update_borders()
        file = ""
        current_step = 0  # Reinicia la ruta si se carga un nuevo archivo
        ruta_finalizada = False  
        
        # Iniciar el timer después de renderizar la pantalla inicial
        pygame.time.set_timer(MOVE_EVENT, 500)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                file = prompt_file()
        elif event.type == MOVE_EVENT and node_result:
            if current_step < len(node_result["ruta"]):
                # La matriz está indexada [fila, columna]
                pos = node_result["ruta"][current_step]
                drone.rect.x = pos[1] * CELL_WIDTH  # columna -> posición x
                drone.rect.y = pos[0] * CELL_HEIGHT   # fila -> posición y
                current_step += 1

                
                if matrix[pos[0]][pos[1]] == 4:
                    matrix[pos[0]][pos[1]] = 0
                    for package in package_sprites:
                        if package.rect.x == pos[1] * CELL_WIDTH and package.rect.y == pos[0] * CELL_HEIGHT:
                            package_sprites.remove(package)
                    
                    
            else:
                # Termina la animación
                pygame.time.set_timer(MOVE_EVENT, 0)
                ruta_finalizada = True 
    
    electric_wall_sprites.update()
    wall_sprites.update()
    package_sprites.update()
    dinamic_sprites.update()
    
    window.fill(background_color)
    
    
    
     # Si la animación terminó, dibuja la ruta tomada en color verde
    if ruta_finalizada and node_result:
        
        # Dibujar de rojo la posición inicial
        pygame.draw.rect(window, (255, 0, 0), (node_result["player_position"][1] * CELL_WIDTH, node_result["player_position"][0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        
        # Iterar en todos los pasos de la ruta menos el último
        for pos in node_result["ruta"][:-1]:
            pygame.draw.rect(window, (0, 255, 0), (pos[1] * CELL_WIDTH, pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
    
        # Dibujar de azul la posición final
        pygame.draw.rect(window, (0, 0, 255), (node_result["ruta"][-1][1] * CELL_WIDTH, node_result["ruta"][-1][0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        
    
    electric_wall_sprites.draw(window)
    wall_sprites.draw(window)
    package_sprites.draw(window)
    dinamic_sprites.draw(window)
    
    
    update_borders()
        
    pygame.display.flip()
    clock.tick(60)

