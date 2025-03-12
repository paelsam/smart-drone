from queue import Queue
from helpers.process_map import process_map

# Operadores
# 0: Izquierda
# 1: Arriba
# 2: Derecha
# 3: Abajo

class Nodo:
    def __init__(self, matriz, posicion, objetivos, padre=None, operador=None, profundidad=0, costo=0):
        self.matriz = matriz
        self.padre = padre
        self.operador = operador
        self.profundidad = profundidad
        self.posicion = posicion
        self.ruta = []
        self.costo = costo
        self.objetivos = objetivos
        
    
    def ver_matriz(self):
        for i in self.matriz:
            for j in i:
                print(j, end=" ")
            print("\n")

    def generar_hijos(self):
        
        print("Posicion actual: ", self.posicion)

        hijos = []
                
        arriba = None if self.posicion[0] - 1 <= 0 else self.matriz[self.posicion[0] - 1][self.posicion[1]]
        derecha = None if self.posicion[1] + 1 >= len(self.matriz) else  self.matriz[self.posicion[0]][self.posicion[1] + 1]
        abajo = None if self.posicion[0] + 1 >= len(self.matriz) else self.matriz[self.posicion[0] + 1][self.posicion[1]]
        izquierda = None if self.posicion[1] - 1 <= 0 else self.matriz[self.posicion[0]][self.posicion[1] - 1]
        
        
        if arriba != 1 and arriba != None:
            hijos.append(Nodo(self.matriz, (self.posicion[0] - 1, self.posicion[1]), self.objetivos, self, 1, self.profundidad + 1))
        if derecha != 1 and derecha != None:
            hijos.append(Nodo(self.matriz, (self.posicion[0], self.posicion[1] + 1), self.objetivos, self, 2, self.profundidad + 1))
        if abajo != 1 and abajo != None:
            hijos.append(Nodo(self.matriz, (self.posicion[0] + 1, self.posicion[1]), self.objetivos, self, 3, self.profundidad + 1))
        if izquierda != 1 and izquierda != None:
            hijos.append(Nodo(self.matriz, (self.posicion[0], self.posicion[1] - 1), self.objetivos, self, 0, self.profundidad + 1))
                
        return hijos
    
    def buscar_objetivos(self): 
        
        nodos_visitados = []
        cola = Queue()
        cola.put(self)
        
        
        while not cola.empty():
            nodo = cola.get()
            nodos_visitados.append(nodo.posicion)
            
            if self.objetivos == 0:
                return nodo

            if nodo.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4:
                print("Objetivo encontrado")
                nodo.objetivos -= 1
                        
            for hijo in nodo.generar_hijos():
                if hijo.posicion not in nodos_visitados:
                    cola.put(hijo)
            
            print("Nodo actual: ", nodo.posicion)
            print(self.obtener_ruta(nodo))
            print("Profundidad: ", nodo.profundidad)
            
            # print("Objetivos faltantes: ", nodo.objetivos)
            # print(queue.qsize())
            print("\n")
            
        
        return None
            
            
    def obtener_ruta(self, nodo):
        ruta = []
        while nodo.padre != None:
            self.ruta.append(nodo.posicion)
            nodo = nodo.padre
        return self.ruta[::-1]
        
        
            
            
            
            
            
            
            

    def __str__(self):
        return  f"Matriz: {self.matriz}\n Padre: {self.padre}\n Operador: {self.operador}\n Profundidad: {self.profundidad}\n Objetivos faltantes: {self.objetivos}\n Posicion: {self.posicion}\n Costo: {self.costo}\n"
    



# Procesar matriz de texto 

matrix = process_map("/home/paelsam/proyecto-ia-uv/assets/maps_files/matrix.txt")
player_position = None
objetivos = 0
queue = Queue()

# Buscar la posición del jugador (numero 2) y la cantidad de objetivos (numero 4)

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 2:
            player_position = [i, j]
        if matrix[i][j] == 4:
            objetivos += 1

# Crear nodo raíz
root = Nodo(matrix, player_position, objetivos)
# print(root.ver_matriz())
print(root.buscar_objetivos())


