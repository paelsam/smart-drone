from helpers.tkinter_app import start_selection
from helpers.pygame_app import start_pygame
from helpers.tkinter_resultados import show_results_window


def main_flow():
    algoritmo, mapa = start_selection()
    
    if algoritmo and mapa:
        # Ejecutar Pygame y obtener resultados
        nodo_result = start_pygame(algoritmo, mapa)
        
        if nodo_result:
            nodo_result['algoritmo'] = algoritmo 
            show_results_window(nodo_result, mapa)

if __name__ == "__main__":
    main_flow()