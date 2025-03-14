from queue import Queue
import copy
from helpers.process_map import process_map

# Operadores
# 0: Izquierda
# 1: Arriba
# 2: Derecha
# 3: Abajo

def convert_operador(operador):
    if operador == 0:
        return "Izquierda"
    if operador == 1:
        return "Arriba"
    if operador == 2:
        return "Derecha"
    if operador == 3:
        return "Abajo"

class Nodo:
    def __init__(self, matriz, posicion, objetivos, padre=None, operador=None, profundidad=0, costo=0):
        self.matriz = matriz
        self.padre = padre
        self.operador = operador
        self.profundidad = profundidad
        self.posicion = posicion
        self.costo = costo
        self.objetivos = objetivos
        self.objetivos_obtenidos = 0
        self.visitados = set()
        
    
    def ver_matriz(self, matriz):
        result = ""
        for i in matriz:
            for j in i:
                result += str(j) + " "
            result += "\n"
        return result

    def generar_hijos(self):
        
        hijos = []
                
        arriba = None if self.posicion[0] - 1 < 0 else self.matriz[self.posicion[0] - 1][self.posicion[1]]
        derecha = None if self.posicion[1] + 1 >= len(self.matriz) else  self.matriz[self.posicion[0]][self.posicion[1] + 1]
        abajo = None if self.posicion[0] + 1 >= len(self.matriz) else self.matriz[self.posicion[0] + 1][self.posicion[1]]
        izquierda = None if self.posicion[1] - 1 < 0 else self.matriz[self.posicion[0]][self.posicion[1] - 1]
        
        
        if arriba != 1 and arriba != None:
            nueva_matriz = copy.deepcopy(self.matriz)
            hijo = Nodo(nueva_matriz, (self.posicion[0] - 1, self.posicion[1]), self.objetivos, self, 1, self.profundidad + 1)
            hijo.objetivos_obtenidos = self.objetivos_obtenidos
            hijo.visitados = self.visitados
            hijos.append(hijo)
        if derecha != 1 and derecha != None:
            nueva_matriz = copy.deepcopy(self.matriz)
            hijo = Nodo(nueva_matriz, (self.posicion[0], self.posicion[1] + 1), self.objetivos, self, 2, self.profundidad + 1)
            hijo.objetivos_obtenidos = self.objetivos_obtenidos
            hijo.visitados = self.visitados
            hijos.append(hijo)
        if abajo != 1 and abajo != None:
            nueva_matriz = copy.deepcopy(self.matriz)
            hijo = Nodo(nueva_matriz, (self.posicion[0] + 1, self.posicion[1]), self.objetivos, self, 3, self.profundidad + 1)
            hijo.objetivos_obtenidos = self.objetivos_obtenidos
            hijo.visitados = self.visitados
            hijos.append(hijo)
        if izquierda != 1 and izquierda != None:
            nueva_matriz = copy.deepcopy(self.matriz)
            hijo = Nodo(nueva_matriz, (self.posicion[0], self.posicion[1] - 1), self.objetivos, self, 0, self.profundidad + 1)
            hijo.objetivos_obtenidos = self.objetivos_obtenidos
            hijo.visitados = self.visitados
            hijos.append(hijo)
                
        return hijos
    
    def buscar_objetivos(self): 
        
        cola = Queue()
        cola.put(self)
        self.visitados.add( ( tuple(self.posicion), 0) )  # Inicializar con 0 objetivos recolectados

        while not cola.empty():    
            
            nodo = cola.get()
            
            # Verificar si la posición actual es un objetivo no recolectado
            if nodo.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4:
                nodo.objetivos_obtenidos += 1
                nodo.matriz[nodo.posicion[0]][nodo.posicion[1]] = 0
                if nodo.objetivos_obtenidos == nodo.objetivos:
                        return nodo

            # Generar hijos y procesar
            hijos = nodo.generar_hijos()

            
            for hijo in hijos:
                estado = (tuple(hijo.posicion), hijo.objetivos_obtenidos)
                if estado not in nodo.visitados:
                    hijo.visitados.add(estado)        
                    cola.put(hijo)       
            
            print(nodo.obtener_ruta())  
            
                
        return None
            
            
    def obtener_ruta(self):
        ruta = []
        nodo = self
        while nodo.padre != None:
            ruta.append(nodo.posicion)
            nodo = nodo.padre
        return ruta[::-1]

    def obtener_ruta_matriz(self, ruta):
        # Hacer una matriz que muestre con flechas ascii la ruta a seguir
        matriz = copy.deepcopy(self.matriz)
        for i in ruta:
            matriz[i[0]][i[1]] = "x"
        return matriz
        
            
        
        
        
    def __str__(self):
        return  f"Operador: {self.operador}\n Profundidad: {self.profundidad}\n Objetivos faltantes: {self.objetivos}\n Posicion: {self.posicion}\n Costo: {self.costo}\n"
    



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
print("Posición inicial del jugador: ", root.posicion)
print("Cantidad de objetivos: ", root.objetivos)
objetivos = root.buscar_objetivos()

print(objetivos)

# print(objetivos.ver_matriz(objetivos.obtener_ruta_matriz(objetivos.obtener_ruta())))
    
    

# print(objetivos)


