from helpers.process_map import process_map
from helpers.determinar_operador import determinar_operador
from colorama import Fore, Style
from queue import LifoQueue

class NodoPD:
    def __init__(self, matriz, posicion, objetivos, padre=None, operador=None):
        self.matriz = matriz
        self.padre = padre
        self.operador = operador
        self.profundidad = 0 if padre is None else padre.profundidad + 1
        self.posicion = posicion
        self.costo = 0 if padre is None else padre.costo + 1
        self.objetivos = objetivos
        self.visitados = set() if padre is None else set(padre.visitados)
        self.objetivos_posiciones = []

    def ver_matriz(self, matriz):
        result = ""
        for i in matriz:
            for j in i:
                result += str(j) + " "
            result += "\n"
        return result

    def generar_hijos(self):
        hijos = []
        direcciones = [(-1, 0, 0), (0, -1, 1), (1, 0, 2), (0, 1, 3)]  # (dy, dx, operador)
        
        for dy, dx, op in direcciones:
            y = self.posicion[0] + dy  # Mueve la fila
            x = self.posicion[1] + dx  # Mueve la columna
            if 0 <= y < len(self.matriz) and 0 <= x < len(self.matriz[0]):
                if self.matriz[y][x] != 1:
                    hijo = NodoPD(self.matriz, (y, x), self.objetivos, self, op)
                    hijo.objetivos_posiciones = self.objetivos_posiciones.copy()
                    hijo.visitados.add((y, x))
                    hijos.append(hijo)
        
        return hijos

    def buscar_objetivos(self):
        pila = LifoQueue()
        pila.put(self)
        self.visitados.add((tuple(self.posicion), 0))

        while not pila.empty():
            nodo = pila.get()

            if self.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4 and nodo.posicion not in nodo.objetivos_posiciones:
                nodo.objetivos_posiciones.append(nodo.posicion)
                if len(nodo.objetivos_posiciones) == nodo.objetivos:
                    return nodo

            hijos = nodo.generar_hijos()
            for hijo in reversed(hijos):
                estado = (tuple(hijo.posicion), len(hijo.objetivos_posiciones))
                if estado not in nodo.visitados:
                    hijo.visitados.add(estado)
                    pila.put(hijo)

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