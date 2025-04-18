import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from ttkbootstrap.dialogs.dialogs import Messagebox

from helpers.pygame_app import start_pygame
from helpers.tkinter_resultados import show_results_window



mapa_seleccionado = None

def prompt_file():
    file_name = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Text files", "*.txt")]
    )
    return file_name

def seleccionar_mapa():
    global mapa_seleccionado
    archivo = prompt_file()
    if archivo:
        mapa_seleccionado.set(archivo)
        mapa_label.config(text=archivo)

def start_selection():    
    global mapa_seleccionado
    
    def obtener_seleccion():
        algoritmo = algoritmo_var.get()
        mapa = mapa_seleccionado.get()
        
        if not algoritmo or mapa == "No seleccionado":
            Messagebox.show_error(
                message="Debes seleccionar un algoritmo y un mapa.",
                title="Error de selección",
                parent=root
            )
            return
        
        # Deshabilitar la ventana principal
        root.withdraw()

        nodo_result = start_pygame(algoritmo, mapa)
        
        if nodo_result:
            nodo_result['algoritmo'] = algoritmo 
            show_results_window(root, nodo_result, mapa)
        
        return algoritmo, mapa

    # Crear la ventana principal con tema de bootstrap
    root = ttk.Window(
        title="Smart Drone",
        themename="cosmo",
        size=(600, 600),
        resizable=(False, False)
    )
    
    # Variables
    algoritmo_var = ttk.StringVar(value="")
    mapa_seleccionado = ttk.StringVar(value="No seleccionado")

    # Frame principal
    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill=BOTH, expand=YES)
    
    # Título principal
    title_label = ttk.Label(
        main_frame, 
        text="Smart Drone", 
        font=("TkDefaultFont", 24, "bold"),
        bootstyle="primary"
    )
    title_label.pack(pady=10)

    subtitle_label = ttk.Label(
        main_frame, 
        text="Selecciona un algoritmo y un mapa para comenzar", 
        font=("TkDefaultFont", 12),
        bootstyle="secondary"
    )
    subtitle_label.pack(pady=(0, 20))
    
    # Frame para algoritmos con estilo
    frame_algoritmos = ttk.Labelframe(
        main_frame, 
        text="Seleccionar Algoritmo",
        padding=10,
        bootstyle="primary"
    )
    frame_algoritmos.pack(fill=X, padx=5, pady=10)

    # Sección No Informada
    ttk.Label(
        frame_algoritmos, 
        text="Búsqueda No Informada", 
        font=("TkDefaultFont", 10, "bold"),
        bootstyle="info"
    ).pack(anchor=W, pady=(5, 0))
    
    ttk.Radiobutton(
        frame_algoritmos, 
        text="Por Amplitud", 
        variable=algoritmo_var, 
        value="Amplitud",
        bootstyle="primary"
    ).pack(anchor=W, padx=15)
    
    ttk.Radiobutton(
        frame_algoritmos, 
        text="Por Reducción de Coste", 
        variable=algoritmo_var, 
        value="Reducción de Coste",
        bootstyle="primary"
    ).pack(anchor=W, padx=15)
    
    ttk.Radiobutton(
        frame_algoritmos, 
        text="Por Profundidad", 
        variable=algoritmo_var, 
        value="Profundidad",
        bootstyle="primary"
    ).pack(anchor=W, padx=15)

    # Sección Informada
    ttk.Label(
        frame_algoritmos, 
        text="Búsqueda Informada", 
        font=("TkDefaultFont", 10, "bold"),
        bootstyle="info"
    ).pack(anchor=W, pady=(10, 0))
    
    ttk.Radiobutton(
        frame_algoritmos, 
        text="Algoritmo Avaro", 
        variable=algoritmo_var, 
        value="Avaro",
        bootstyle="primary"
    ).pack(anchor=W, padx=15)
    
    ttk.Radiobutton(
        frame_algoritmos, 
        text="A* (A estrella)", 
        variable=algoritmo_var, 
        value="A*",
        bootstyle="primary"
    ).pack(anchor=W, padx=15)

    # Frame para selección de mapa
    frame_mapa = ttk.Labelframe(
        main_frame, 
        text="Seleccionar Mapa",
        padding=10,
        bootstyle="success"
    )
    frame_mapa.pack(fill=X, padx=5, pady=10)

    # Contenedor para la ruta del mapa y botón
    mapa_container = ttk.Frame(frame_mapa)
    mapa_container.pack(fill=X, expand=YES)
    
    global mapa_label
    mapa_label = ttk.Label(
        mapa_container, 
        text="No seleccionado",
        bootstyle="secondary"
    )
    mapa_label.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
    
    ttk.Button(
        mapa_container, 
        text="Seleccionar Archivo", 
        command=seleccionar_mapa,
        bootstyle="outline-success"
    ).pack(side=RIGHT)

    # Botón de iniciar
    ttk.Button(
        main_frame, 
        text="Iniciar Demostración", 
        command=obtener_seleccion,
        bootstyle="success",
        width=20
    ).pack(pady=20)
    
    # Footer - créditos
    footer = ttk.Label(
        main_frame, 
        text="Desarrollado por Elkin, Andrés, Miguel y Leo",
        bootstyle="secondary",
        font=("TkDefaultFont", 8)
    )
    footer.pack(side=BOTTOM, pady=5)
    
    root.place_window_center()
    root.mainloop()
    return algoritmo_var.get(), mapa_seleccionado.get()