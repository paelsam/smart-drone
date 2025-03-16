from helpers.process_map import process_map
from helpers.determinar_operador import determinar_operador
from colorama import Fore, Style

class Nodo:
    def __init__(self, matriz, posicion, objetivos, padre=None, operador=None):
        self.matriz = matriz
        self.padre = padre
        self.operador = operador
        self.profundidad = 0 if padre == None else padre.profundidad + 1
        self.posicion = posicion
        self.costo = 0 if padre == None else padre.costo + 1
        self.objetivos = objetivos
        self.visitados = set(padre.visitados) if padre != None else set() # Poniendo un set en el padre para evitar problemas de referencias
        self.objetivos_posiciones = []
        self.camino = padre.camino + [posicion] if padre else [posicion]  # Historial de posiciones en la rama

    def ver_matriz(self, matriz):
        result = ""
        for fila in matriz:
            result += " ".join(str(c) for c in fila) + "\n"
        return result

    def generar_hijos(self):
        hijos = []
        direcciones = [(-1, 0, 1), (0, 1, 2), (1, 0, 3), (0, -1, 0)]

        for dx, dy, op in direcciones:
            x, y = self.posicion[0] + dx, self.posicion[1] + dy
            
            if 0 <= x < len(self.matriz) and 0 <= y < len(self.matriz[0]):  # Verificar límites
                if self.matriz[x][y] != 1 and (x, y) not in self.camino:  # Evitar obstáculos y nodos visitados
                    hijo = Nodo(self.matriz, (x, y), self.objetivos, self, op)
                    hijo.objetivos_posiciones = self.objetivos_posiciones.copy()
                    hijos.append(hijo)
        
        return hijos

    def buscar_objetivos(self):
        pila = [(self, 0)]  # (nodo, nivel de profundidad)
        visitados = set()

        while pila:
            nodo, nivel = pila.pop()
            estado = (tuple(nodo.posicion), len(nodo.objetivos_posiciones))

            if estado in visitados:
                continue
            visitados.add(estado)

            # expansión del árbol
            print("    " * nivel + f"Profundidad: {nodo.profundidad}, Posicion: {nodo.posicion}")

            if self.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4 and nodo.posicion not in nodo.objetivos_posiciones:
                nodo.objetivos_posiciones.append(nodo.posicion)
                if len(nodo.objetivos_posiciones) == nodo.objetivos:
                    return nodo  
            
            hijos = nodo.generar_hijos() 
            for hijo in hijos:
                pila.append((hijo, nivel + 1))

        return None  

    def obtener_ruta(self):
        ruta = []
        nodo = self
        while nodo.padre is not None:
            ruta.append(nodo.posicion)
            nodo = nodo.padre
        return ruta[::-1]

    def obtener_ruta_matriz(self, ruta):
        matriz = [fila[:] for fila in self.matriz]
        for i in ruta:
            matriz[i[0]][i[1]] = Fore.RED + "x" + Style.RESET_ALL
        return matriz

    def __str__(self):
        return f"Operador: {determinar_operador(self.operador)}\nProfundidad: {self.profundidad}\n" \
               f"Objetivos faltantes: {self.objetivos - len(self.objetivos_posiciones)}\n" \
               f"Posicion: {self.posicion}\nCosto: {self.costo}\n"

# Procesar matriz de texto 

matrix = process_map("./assets/maps_files/matrix2.txt")
player_position = None
objetivos = 0

# Buscar la posición del jugador (numero 2) y la cantidad de objetivos (numero 4)

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 2:
            player_position = [i, j]
        if matrix[i][j] == 4:
            objetivos += 1

# Crear nodo raíz
root = Nodo(matrix, player_position, objetivos)
print("Posición inicial del jugador: ", root.posicion)
print("Cantidad de objetivos: ", root.objetivos)
objetivos = root.buscar_objetivos()

print(objetivos)
print(objetivos.obtener_ruta())


print(objetivos.ver_matriz(objetivos.obtener_ruta_matriz(objetivos.obtener_ruta())))