import tkinter as tk
from tkinter import ttk

def show_results_window(nodo_result, mapa_path):
    def volver_seleccion():
        results_window.destroy()
        from main import main_flow
        main_flow()
    
    results_window = tk.Tk()
    results_window.title("Smart Drone - Resultados")
    results_window.geometry("400x500")
    results_window.resizable(False, False)
    
    
    # Frame principal
    main_frame = ttk.Frame(results_window)
    main_frame.pack(padx=20, pady=20, fill='both', expand=True)
    
    # Sección de información general
    info_frame = ttk.LabelFrame(main_frame, text="Información del Recorrido")
    info_frame.pack(fill='x', pady=10)
    
    labels = [
        f"Algoritmo utilizado: {nodo_result['algoritmo']}",
        f"Archivo de mapa: {mapa_path}",
        f"Profundidad: {nodo_result['profundidad']}",
        f"Costo total: {nodo_result['costo']}",
        f"Objetivos alcanzados: {len(nodo_result['objetivos_posiciones'])}"
    ]
    
    for label in labels:
        ttk.Label(info_frame, text=label).pack(anchor='w')
    
    # Sección de ruta
    ruta_frame = ttk.LabelFrame(main_frame, text="Ruta Tomada")
    ruta_frame.pack(fill='both', expand=True, pady=10)
    
    scrollbar = ttk.Scrollbar(ruta_frame)
    scrollbar.pack(side='right', fill='y')
    
    listbox = tk.Listbox(ruta_frame, yscrollcommand=scrollbar.set, width=50)
    for posicion in nodo_result['ruta']:
        listbox.insert('end', f"({posicion[0]}, {posicion[1]})")
    listbox.pack(fill='both', expand=True)
    scrollbar.config(command=listbox.yview)
    
    # Botón de regreso
    ttk.Button(main_frame, text="Volver a Selección", command=volver_seleccion).pack(pady=10)
    
    results_window.mainloop()