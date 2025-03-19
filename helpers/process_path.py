from queue import Queue

def process_path(matrix: list, algorithm) -> dict:
    player_position = None
    objetivos = 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 2:
                player_position = (i, j)
            elif matrix[i][j] == 4:
                objetivos += 1
    
    root = algorithm(matrix, player_position, objetivos)
    objetivos_obtenidos = root.buscar_objetivos()
    return {
        "root": root,
        "player_position": player_position,
        "resultado": objetivos_obtenidos,
        "objetivos": objetivos,
        "ruta": objetivos_obtenidos.obtener_ruta(),
        "matriz_ruta": objetivos_obtenidos.ver_matriz(objetivos_obtenidos.obtener_ruta_matriz(objetivos_obtenidos.obtener_ruta()))
    }
    
    
    