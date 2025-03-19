import tkinter as tk
from tkinter import filedialog, messagebox

mapa_seleccionado = None

def prompt_file():
    top = tk.Tk()
    top.withdraw()
    file_name = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Text files", "*.txt")]
    )
    top.destroy()
    return file_name

def seleccionar_mapa():
    global mapa_seleccionado
    archivo = prompt_file()
    if archivo:
        mapa_seleccionado.set(archivo)

def start_selection():    
    global mapa_seleccionado
    
    def obtener_seleccion():
        algoritmo = algoritmo_var.get()
        mapa = mapa_seleccionado.get()
        
        if not algoritmo or mapa == "No seleccionado":
            messagebox.showerror("Error", "Debes seleccionar un algoritmo y un mapa.")
            return
        
        root.destroy()
        return algoritmo, mapa

    root = tk.Tk()
    root.title("Smart Drone - Selección de Algoritmo y Mapa")
    root.geometry("400x400")
    root.resizable(False, False)

    # Variables
    algoritmo_var = tk.StringVar(value="")
    mapa_seleccionado = tk.StringVar(value="No seleccionado")

    # Interfaz
    frame_algoritmos = tk.LabelFrame(root, text="Seleccionar Algoritmo")
    frame_algoritmos.pack(padx=10, pady=10, fill="both")

    tk.Label(frame_algoritmos, text="Búsqueda No Informada").pack(anchor="w")
    tk.Radiobutton(frame_algoritmos, text="Por Amplitud", variable=algoritmo_var, value="Amplitud").pack(anchor="w")
    tk.Radiobutton(frame_algoritmos, text="Por Reducción de Coste", variable=algoritmo_var, value="Reducción de Coste").pack(anchor="w")
    tk.Radiobutton(frame_algoritmos, text="Por Profundidad", variable=algoritmo_var, value="Profundidad").pack(anchor="w")

    tk.Label(frame_algoritmos, text="Búsqueda Informada").pack(anchor="w")
    tk.Radiobutton(frame_algoritmos, text="Algoritmo Avaro", variable=algoritmo_var, value="Avaro").pack(anchor="w")
    tk.Radiobutton(frame_algoritmos, text="A* (A estrella)", variable=algoritmo_var, value="A*").pack(anchor="w")

    frame_mapa = tk.LabelFrame(root, text="Seleccionar Mapa")
    frame_mapa.pack(padx=10, pady=10, fill="both")

    mapa_label = tk.Label(frame_mapa, textvariable=mapa_seleccionado)
    mapa_label.pack()
    tk.Button(frame_mapa, text="Seleccionar Archivo", command=seleccionar_mapa).pack()

    tk.Button(root, text="Iniciar Demostración", command=obtener_seleccion).pack(pady=10)
    
    root.mainloop()
    return algoritmo_var.get(), mapa_seleccionado.get()

if __name__ == "__main__":
    algoritmo, mapa = start_selection()
    print(f"Selección guardada: Algoritmo: {algoritmo}, Mapa: {mapa}")