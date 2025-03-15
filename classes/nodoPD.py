import heapq
from helpers.process_map import process_map
from helpers.determinar_operador import determinar_operador
from colorama import Fore, Style

class NodoPD:
    def __init__(self, matriz, posicion, objetivos, padre=None, operador=None):
        self.matriz = matriz
        self.padre = padre
        self.operador = operador
        self.profundidad = 0 if padre == None else padre.profundidad + 1
        self.posicion = posicion
        self.costo = 0 if padre == None else padre.costo + self.calcular_costo_casilla()
        self.objetivos = objetivos
        self.visitados = set(padre.visitados) if padre != None else set()
        self.objetivos_posiciones = []

    def calcular_costo_casilla(self):
        if self.matriz[self.posicion[0]][self.posicion[1]] == 3:
            return 8
        else:
            return 1

    def ver_matriz(self, matriz):
        result = ""
        for i in matriz:
            for j in i:
                result += str(j) + " "
            result += "\n"
        return result

    def generar_hijos(self):
        hijos = []
        direcciones = [(-1, 0, 1), (0, 1, 2), (1, 0, 3), (0, -1, 0)]
        for dx, dy, op in direcciones:
            x = self.posicion[0] + dx
            y = self.posicion[1] + dy
            if x >= 0 and x < len(self.matriz) and y >= 0 and y < len(self.matriz[0]):
                if self.matriz[x][y] != 1:
                    hijo = NodoPD(self.matriz, (x, y), self.objetivos, self, op)
                    hijo.objetivos_posiciones = self.objetivos_posiciones.copy()
                    hijos.append(hijo)
        return hijos

    def buscar_objetivos(self):
        cola_prioridad = []
        contador_global = 0  # Contador global para orden determinístico
        heapq.heappush(cola_prioridad, (-self.profundidad, self.operador, contador_global, self))
        contador_global += 1
        self.visitados.add((tuple(self.posicion), 0))

        while cola_prioridad:
            _, _, _, nodo = heapq.heappop(cola_prioridad)

            if nodo.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4 and nodo.posicion not in nodo.objetivos_posiciones:
                nodo.objetivos_posiciones.append(nodo.posicion)
                if len(nodo.objetivos_posiciones) == nodo.objetivos:
                    return nodo

            hijos = nodo.generar_hijos()
            for hijo in hijos:
                estado = (tuple(hijo.posicion), len(hijo.objetivos_posiciones))
                if estado not in nodo.visitados:
                    hijo.visitados.add(estado)
                    # Insertar en el heap con (-profundidad, operador, contador, self)
                    heapq.heappush(cola_prioridad, (-hijo.profundidad, hijo.operador, contador_global, hijo))
                    contador_global += 1

        return None

    def obtener_ruta(self):
        ruta = []
        nodo = self
        while nodo.padre != None:
            ruta.append(nodo.posicion)
            nodo = nodo.padre
        return ruta[::-1]

    def obtener_ruta_matriz(self, ruta):
        matriz = [fila[:] for fila in self.matriz]
        for i in ruta:
            matriz[i[0]][i[1]] = Fore.RED + "x" + Style.RESET_ALL
        return matriz

    def __str__(self):
        return f"Operador: {determinar_operador(self.operador)}\nProfundidad: {self.profundidad}\nObjetivos faltantes: {self.objetivos - len(self.objetivos_posiciones)}\nPosicion: {self.posicion}\nCosto: {self.costo}\n"


# Procesar matriz de texto
matrix = process_map("./assets/maps_files/matrix2.txt")
player_position = None
objetivos = 0

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 2:
            player_position = [i, j]
        if matrix[i][j] == 4:
            objetivos += 1

root = NodoPD(matrix, player_position, objetivos)
print("Posición inicial del jugador: ", root.posicion)
print("Cantidad de objetivos: ", root.objetivos)
objetivos = root.buscar_objetivos()

print(objetivos)
print(objetivos.obtener_ruta())

print(objetivos.ver_matriz(objetivos.obtener_ruta_matriz(objetivos.obtener_ruta())))