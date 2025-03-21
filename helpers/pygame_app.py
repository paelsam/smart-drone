import pygame
from helpers.process_map import process_map
from helpers.process_path import process_path
from helpers.sprite import Sprite
from classes.nodo import Nodo
from classes.nodoCU import NodoCU
from classes.nodoPD import NodoPD
from classes.nodoAV import NodoAvara

MOVE_EVENT = pygame.USEREVENT + 1

def start_pygame(algoritmo, mapa_path):
    
    def update_borders(ROWS, COLUMNS, CELL_WIDTH, CELL_HEIGHT, window):
        for i in range(ROWS):
            for j in range(COLUMNS):
                pygame.draw.rect(window, (0, 0, 0), (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 2)
    
    # Configuración inicial de Pygame
    WIDTH, HEIGHT = 600, 600
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dron AI - Visualización")
    
    # Configurar clases según el algoritmo
    algoritmo_clases = {
        "Amplitud": Nodo,
        "Reducción de Coste": NodoCU,
        "Profundidad": NodoPD,
        "Avaro": NodoAvara,  # Actualizar con clases reales
        "A*": Nodo
    }
    
    # Procesar mapa y configurar visualización
    matrix = process_map(mapa_path)
    algoritmo_seleccionado = algoritmo_clases[algoritmo]
    
    # (Mantener aquí todo el código de visualización de Pygame)
    ROWS = len(matrix)
    COLUMNS = len(matrix[0])
    CELL_WIDTH = WIDTH // COLUMNS
    CELL_HEIGHT = HEIGHT // ROWS
    
    # Configurar sprites
    wall_sprites = pygame.sprite.Group()
    package_sprites = pygame.sprite.Group()
    dinamic_sprites = pygame.sprite.Group()
    electric_wall_sprites = pygame.sprite.Group()
    drone = None
    
    # Dibujar el mapa
    for i in range(ROWS):
        for j in range(COLUMNS):
            if matrix[i][j] == 1:
                wall = Sprite("./assets/img/wall.jpg", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                wall_sprites.add(wall)
            elif matrix[i][j] == 2 and not drone:
                drone = Sprite("./assets/img/drone.png", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                dinamic_sprites.add(drone)
            elif matrix[i][j] == 4:
                package = Sprite("./assets/img/package.jpg", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                package_sprites.add(package)
            elif matrix[i][j] == 3:
                electric_wall = Sprite("./assets/img/electric-wall.png", j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                electric_wall_sprites.add(electric_wall)
    
    # Calcular la ruta
    node_result = process_path(matrix, algoritmo_seleccionado)
    current_step = 0
    ruta_finalizada = False
    pygame.time.set_timer(MOVE_EVENT, 500)
    
    
   # Bucle principal de Pygame
    running = True   
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOVE_EVENT and node_result:
                if current_step < len(node_result["ruta"]):
                    pos = node_result["ruta"][current_step]
                    drone.rect.x = pos[1] * CELL_WIDTH
                    drone.rect.y = pos[0] * CELL_HEIGHT
                    current_step += 1
                    
                    if matrix[pos[0]][pos[1]] == 4:
                        matrix[pos[0]][pos[1]] = 0
                        for package in package_sprites:
                            if package.rect.x == pos[1] * CELL_WIDTH and package.rect.y == pos[0] * CELL_HEIGHT:
                                package_sprites.remove(package)
                else:
                    pygame.time.set_timer(MOVE_EVENT, 0)
                    ruta_finalizada = True
        
        # Dibujar todo
        screen.fill((255, 255, 255))
        wall_sprites.draw(screen)
        package_sprites.draw(screen)
        dinamic_sprites.draw(screen)
        electric_wall_sprites.draw(screen)
        
        update_borders(ROWS, COLUMNS, CELL_WIDTH, CELL_HEIGHT, screen)
        
        if ruta_finalizada:
             # Dibujar de rojo la posición inicial
            pygame.draw.rect(screen, (255, 0, 0), (node_result["player_position"][1] * CELL_WIDTH, node_result["player_position"][0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        
            # Iterar en todos los pasos de la ruta menos el último
            for pos in node_result["ruta"][:-1]:
                pygame.draw.rect(screen, (0, 255, 0), (pos[1] * CELL_WIDTH, pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            
            # Pintar de amarillo la posición de los objetivos obtenidos
            for pos in node_result["resultado"].objetivos_posiciones:
                pygame.draw.rect(screen, (255, 255, 0), (pos[1] * CELL_WIDTH, pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        
            # Dibujar de azul la posición final
            pygame.draw.rect(screen, (0, 0, 255), (node_result["ruta"][-1][1] * CELL_WIDTH, node_result["ruta"][-1][0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                    
            update_borders(ROWS, COLUMNS, CELL_WIDTH, CELL_HEIGHT, screen)
            
            pygame.display.flip()
            
            return {
                'ruta': node_result["ruta"],
                'profundidad': node_result["resultado"].profundidad,
                'costo': node_result["resultado"].costo,
                'objetivos_posiciones': node_result["resultado"].objetivos_posiciones,
                'tiempo_computo': node_result["tiempo_computo"]
            }
        
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    

if __name__ == "__main__":
    # Para pruebas independientes
    start_pygame("A*", "maps/mapa_ejemplo.txt")