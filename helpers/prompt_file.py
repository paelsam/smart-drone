import tkinter as tk
from tkinter import filedialog

def prompt_file():
    top = tk.Tk()
    top.withdraw()  # Ocultar la ventana principal
    file_name = filedialog.askopenfilename(
        parent=top,
        title="Seleccionar archivo",
        filetypes=[("Text files", "*.txt")],  # Restringir a archivos .txt
    )
    top.destroy()
    return file_name

def obtener_seleccion():
    seleccion = {
        "algoritmo": algoritmo_var.get(),
        "mapa": mapa_seleccionado.get()
    }
    print(seleccion)  # Puedes modificar esto para manejar la salida según necesites

def seleccionar_mapa():
    archivo = prompt_file()
    if archivo:
        mapa_seleccionado.set(archivo)

# Crear ventana principal
root = tk.Tk()
root.title("Selección de Algoritmo de Búsqueda")

# Variables
algoritmo_var = tk.StringVar(value="")
mapa_seleccionado = tk.StringVar(value="No seleccionado")

# Sección de selección de algoritmo
frame_algoritmos = tk.LabelFrame(root, text="Seleccionar Algoritmo")
frame_algoritmos.pack(padx=10, pady=10, fill="both")

# Opciones de búsqueda no informada
tk.Label(frame_algoritmos, text="Búsqueda No Informada").pack(anchor="w")
tk.Radiobutton(frame_algoritmos, text="Por Amplitud", variable=algoritmo_var, value="Amplitud").pack(anchor="w")
tk.Radiobutton(frame_algoritmos, text="Por Reducción de Coste", variable=algoritmo_var, value="Reducción de Coste").pack(anchor="w")
tk.Radiobutton(frame_algoritmos, text="Por Profundidad", variable=algoritmo_var, value="Profundidad").pack(anchor="w")

# Opciones de búsqueda informada
tk.Label(frame_algoritmos, text="Búsqueda Informada").pack(anchor="w")
tk.Radiobutton(frame_algoritmos, text="Algoritmo Avaro", variable=algoritmo_var, value="Avaro").pack(anchor="w")
tk.Radiobutton(frame_algoritmos, text="A* (A estrella)", variable=algoritmo_var, value="A*").pack(anchor="w")

# Sección de selección de mapa
frame_mapa = tk.LabelFrame(root, text="Seleccionar Mapa")
frame_mapa.pack(padx=10, pady=10, fill="both")

mapa_label = tk.Label(frame_mapa, textvariable=mapa_seleccionado)
mapa_label.pack()
mapa_boton = tk.Button(frame_mapa, text="Seleccionar Archivo", command=seleccionar_mapa)
mapa_boton.pack()

# Botón para comenzar la demostración
boton_iniciar = tk.Button(root, text="Iniciar Demostración", command=obtener_seleccion)
boton_iniciar.pack(pady=10)

root.mainloop()
