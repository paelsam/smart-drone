from queue import Queue
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
    def __init__(self, matriz, posicion, objetivos, padre=None, operador=None, profundidad=0, costo=0, objetivos_recolectados=[]):
        self.matriz = matriz
        self.padre = padre
        self.operador = operador
        self.profundidad = profundidad
        self.posicion = posicion
        self.costo = costo
        self.objetivos = objetivos
        self.objetivos_recolectados = objetivos_recolectados
        self.visitados = set()
        
    
    def ver_matriz(self):
        result = ""
        for i in self.matriz:
            for j in i:
                result += str(j) + " "
            result += "\n"
        return result

    def generar_hijos(self):
        
        hijos = []
                
        arriba = None if self.posicion[0] - 1 <= 0 else self.matriz[self.posicion[0] - 1][self.posicion[1]]
        derecha = None if self.posicion[1] + 1 >= len(self.matriz) else  self.matriz[self.posicion[0]][self.posicion[1] + 1]
        abajo = None if self.posicion[0] + 1 >= len(self.matriz) else self.matriz[self.posicion[0] + 1][self.posicion[1]]
        izquierda = None if self.posicion[1] - 1 <= 0 else self.matriz[self.posicion[0]][self.posicion[1] - 1]
        
        
        if arriba != 1 and arriba != None:
            hijo = Nodo(self.matriz, (self.posicion[0] - 1, self.posicion[1]), self.objetivos, self, 1, self.profundidad + 1, 0, self.objetivos_recolectados)
            hijos.append(hijo)
            
            # Añadir visitados del padre
            for visitado in self.visitados:
                hijo.visitados.add(visitado)
            
            
        if derecha != 1 and derecha != None:
            hijo = Nodo(self.matriz, (self.posicion[0], self.posicion[1] + 1), self.objetivos, self, 2, self.profundidad + 1, 0, self.objetivos_recolectados)
            hijos.append(hijo)
            
            # Añadir visitados del padre
            for visitado in self.visitados:
                hijo.visitados.add(visitado)

        if abajo != 1 and abajo != None:
            hijo = Nodo(self.matriz, (self.posicion[0] + 1, self.posicion[1]), self.objetivos, self, 3, self.profundidad + 1, 0, self.objetivos_recolectados)
            hijos.append(hijo)
            
            # Añadir visitados del padre
            for visitado in self.visitados:
                hijo.visitados.add(visitado)
        
        if izquierda != 1 and izquierda != None:
            hijo = Nodo(self.matriz, (self.posicion[0], self.posicion[1] - 1), self.objetivos, self, 0, self.profundidad + 1, 0, self.objetivos_recolectados)
            hijos.append(hijo)
            
            # Añadir visitados del padre
            for visitado in self.visitados:
                hijo.visitados.add(visitado)
            
            
        # if abajo != 1 and abajo != None:
        #     hijos.append(Nodo(self.matriz, (self.posicion[0] + 1, self.posicion[1]), self.objetivos, self, 3, self.profundidad + 1, 0, self.objetivos_recolectados))
        # if izquierda != 1 and izquierda != None:
        #     hijos.append(Nodo(self.matriz, (self.posicion[0], self.posicion[1] - 1), self.objetivos, self, 0, self.profundidad + 1, 0, self.objetivos_recolectados))
                
        return hijos
    
    def buscar_objetivos(self): 
        
        initial_objetivos = self.objetivos  # Guardar la cantidad inicial de objetivos
        cola = Queue()
        cola.put(self)
        self.visitados.add( ( tuple(self.posicion), 0) )  # Inicializar con 0 objetivos recolectados

        while not cola.empty():
            
            nodo = cola.get()
            

            # Verificar si la posición actual es un objetivo no recolectado
            if nodo.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4:
                if nodo.posicion not in nodo.objetivos_recolectados:                    
                    nodo.objetivos_recolectados.append(nodo.posicion)                    
                    print("Objetivos recolectados: ", nodo.todos_objetivos_obtenidos())
                    if nodo.todos_objetivos_obtenidos():
                        print(nodo)
                        break
                        return nodo

            # Generar hijos y procesar
            hijos = nodo.generar_hijos()
            # print(f"Hijos de {nodo.posicion}:", [hijo.posicion for hijo in hijos])

            
            for hijo in hijos:
                current_k = len(hijo.objetivos_recolectados) 
                estado = (tuple(hijo.posicion), current_k)
                if estado not in nodo.visitados:
                    hijo.visitados.add(estado)
                    cola.put(hijo)
            
            # print(nodo.obtener_ruta())
            # print(nodo.visitados)

                    
                
        return None

    def todos_objetivos_obtenidos(self):
        ruta = self.obtener_ruta()
        
        if len(self.objetivos_recolectados) != self.objetivos:
            return False
        
        # print("Objetivos recolectados: ", self.objetivos_recolectados)
        print("Ruta: ", ruta)
        
        for pos in self.objetivos_recolectados:
            if pos not in ruta:
                return False
        return True
            
            
    def obtener_ruta(self):
        ruta = []
        nodo = self
        while nodo.padre:
            ruta.append(nodo.posicion)
            nodo = nodo.padre
        ruta.append(nodo.posicion)
        return ruta[::-1]
        
        
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
print(objetivos.obtener_ruta())

print(objetivos)
print("Posición final del jugador: ", objetivos.posicion)
print("Objetivos recolectados: ", objetivos.objetivos_recolectados)


