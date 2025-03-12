import tkinter
from tkinter import filedialog

def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # Ocultar la ventana principal
    file_name = filedialog.askopenfilename(
        parent=top,
        title="Seleccionar archivo",
        filetypes=[("Text files", "*.txt")],  # Restringir a archivos .txt
    )
    top.destroy()
    return file_name