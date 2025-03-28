import pygame
from helpers.process_map import process_map
from helpers.process_path import process_path
from helpers.sprite import Sprite
from classes.nodo import Nodo
from classes.nodoCU import NodoCU
from classes.nodoPD import NodoPD
from classes.nodoAV import NodoAvara

# MOVE_EVENT = pygame.USEREVENT + 1

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
        "Avaro": NodoAvara,
        "A*": Nodo
    }
    
    
    # Mostrar pantalla de carga antes de calcular la ruta
    screen.fill((30, 30, 30))
    font = pygame.font.SysFont("Arial", 48, bold=True)
    text = font.render("Calculando ruta...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip() 
    
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
    
    # Configuración de movimiento 
    speed = 4  
    target_pos = None
    moving = False
    
    
    clock = pygame.time.Clock()
    running = True   
    while running:
        
        dt = clock.tick(24)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        if not moving and node_result and current_step < len(node_result["ruta"]):
            pos = node_result["ruta"][current_step]
            target_pos = (pos[1] * CELL_WIDTH, pos[0] * CELL_HEIGHT)
            moving = True
        elif current_step >= len(node_result["ruta"]) and not moving:
            ruta_finalizada = True
            
        # Movimiento suave hacia la posición objetivo
        if moving and target_pos:
            dx = target_pos[0] - drone.rect.x
            dy = target_pos[1] - drone.rect.y
            distance = (dx**2 + dy**2) ** 0.5

            if distance < speed:
                drone.rect.topleft = target_pos
                moving = False
                current_step += 1

                # Eliminar paquete si hay uno en la celda
                pos_matrix = (target_pos[1] // CELL_HEIGHT, target_pos[0] // CELL_WIDTH)
                if matrix[pos_matrix[0]][pos_matrix[1]] == 4:
                    matrix[pos_matrix[0]][pos_matrix[1]] = 0
                    for package in package_sprites:
                        if package.rect.collidepoint(target_pos[0] + CELL_WIDTH//2, target_pos[1] + CELL_HEIGHT//2):
                            package_sprites.remove(package)
            else:
                drone.rect.x += int(speed * dx / distance)
                drone.rect.y += int(speed * dy / distance)
        
        # Dibujar todo
        screen.fill((240, 235, 225)) 
        wall_sprites.draw(screen)
        package_sprites.draw(screen)
        electric_wall_sprites.draw(screen)
        dinamic_sprites.draw(screen)
        
        
        update_borders(ROWS, COLUMNS, CELL_WIDTH, CELL_HEIGHT, screen)
        
        if ruta_finalizada:
             # Dibujar de rojo la posición inicial
            pygame.draw.rect(screen, (220, 20, 60), (node_result["player_position"][1] * CELL_WIDTH, node_result["player_position"][0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        
            # Iterar en todos los pasos de la ruta menos el último
            for pos in node_result["ruta"][:-1]:
                pygame.draw.rect(screen, (60, 179, 113), (pos[1] * CELL_WIDTH, pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            
            # Pintar de amarillo la posición de los objetivos obtenidos
            for pos in node_result["resultado"].objetivos_posiciones:
                pygame.draw.rect(screen, (255, 215, 0), (pos[1] * CELL_WIDTH, pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        
            # Dibujar de azul la posición final
            pygame.draw.rect(screen, (65, 105, 225), (node_result["ruta"][-1][1] * CELL_WIDTH, node_result["ruta"][-1][0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                    
            update_borders(ROWS, COLUMNS, CELL_WIDTH, CELL_HEIGHT, screen)
            
            dinamic_sprites.draw(screen)
            
            pygame.display.flip()
                    
            return {
                'ruta': node_result["ruta"],
                'profundidad': node_result["resultado"].profundidad,
                'costo': node_result["resultado"].costo,
                'objetivos_posiciones': node_result["resultado"].objetivos_posiciones,
                'tiempo_computo': node_result["tiempo_computo"],
                'nodos_expandidos': node_result["resultado"].nodos_expandidos
            }
        
        pygame.display.flip()