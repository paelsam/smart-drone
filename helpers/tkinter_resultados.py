import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk

def show_results_window(selection_window, nodo_result, mapa_path):
    def volver_seleccion():
        results_window.destroy()
        selection_window.deiconify() 
    
    
    results_window = ttk.Toplevel(resizable=(False, False))
    results_window.protocol("WM_DELETE_WINDOW", volver_seleccion)

    
    
    # Frame principal
    main_frame = ttk.Frame(results_window, padding=15)
    main_frame.pack(fill=BOTH, expand=YES)
    
    # Título de resultados
    title_label = ttk.Label(
        main_frame,
        text="Resultados de la Navegación",
        font=("TkDefaultFont", 18, "bold"),
        bootstyle="primary"
    )
    title_label.pack(pady=(0, 15))
    
    # Sección de información general
    info_frame = ttk.Labelframe(
        main_frame, 
        text="Información del Recorrido",
        padding=10,
        bootstyle="info"
    )
    info_frame.pack(fill=X, pady=10)
    
    # Crear grid para información más organizada
    info_grid = ttk.Frame(info_frame)
    info_grid.pack(fill=X, expand=YES)
    
    # Definir datos para la grid
    info_data = [
        ("Algoritmo utilizado:", nodo_result['algoritmo']),
        ("Archivo de mapa:", mapa_path),
        ("Profundidad:", str(nodo_result['profundidad'])),
        ("Nodos expandidos:", str(nodo_result['nodos_expandidos'])),
        ("Costo total:", str(nodo_result['costo'])),
        ("Objetivos alcanzados:", str(len(nodo_result['objetivos_posiciones']))),
        ("Tiempo de cómputo:", f"{nodo_result['tiempo_computo']:.4f} segundos")
    ]
    
    # Crear etiquetas en el grid
    for i, (label_text, value_text) in enumerate(info_data):
        label = ttk.Label(
            info_grid, 
            text=label_text,
            font=("TkDefaultFont", 10, "bold"),
            width=20,
            anchor=W
        )
        label.grid(row=i, column=0, sticky=W, pady=3)
        
        value = ttk.Label(
            info_grid,
            text=value_text,
            bootstyle="secondary"
        )
        value.grid(row=i, column=1, sticky=W, pady=3)
    
    # Sección de ruta con scrolled frame
    ruta_frame = ttk.Labelframe(
        main_frame, 
        text="Ruta Tomada",
        padding=10,
        bootstyle="primary"
    )
    ruta_frame.pack(fill=BOTH, expand=YES, pady=10)
    
    # Frame con scroll (sin usar el componente Meter que causaba problemas)
    scrolled = ScrolledFrame(ruta_frame, autohide=True)
    scrolled.pack(fill=BOTH, expand=YES)
    
    # Listado de coordenadas con estilo alternante para mejor legibilidad
    for i, posicion in enumerate(nodo_result['ruta']):
        row_style = "primary" if i % 2 == 0 else "secondary"
        pos_frame = ttk.Frame(scrolled, bootstyle=row_style)
        pos_frame.pack(fill=X, pady=1)
        
        ttk.Label(
            pos_frame,
            text=f"Paso {i+1}:",
            width=8,
            bootstyle=row_style
        ).pack(side=LEFT, padx=5, pady=3)
        
        ttk.Label(
            pos_frame,
            text=f"({posicion[0]}, {posicion[1]})",
            bootstyle=row_style
        ).pack(side=LEFT, padx=5, pady=3)
    
    # Botón de regreso con icono
    action_frame = ttk.Frame(main_frame)
    action_frame.pack(fill=X, pady=(10, 0))
    
    ttk.Button(
        action_frame, 
        text="Volver a Selección",
        command=volver_seleccion,
        bootstyle="outline-secondary",
        width=20
    ).pack(side=RIGHT)
    
    # Footer - créditos
    footer = ttk.Label(
        main_frame, 
        text="Smart Drone - Análisis de Resultados",
        bootstyle="secondary",
        font=("TkDefaultFont", 8)
    )
    footer.pack(side=BOTTOM, pady=5)
    
    # Centrar ventana
    results_window.place_window_center()
    
    results_window.mainloop()