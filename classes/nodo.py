from queue import Queue
from helpers.process_map import process_map

# Operadores
# 0: Izquierda
# 1: Arriba
# 2: Derecha
# 3: Abajo

class Nodo:
    def __init__(self, matriz, posicion, objetivos, padre=None, operador=None):
        self.matriz = matriz
        self.padre = padre
        self.operador = operador
        self.profundidad = 0 if padre == None else padre.profundidad + 1
        self.posicion = posicion
        self.costo = 0 if padre == None else padre.costo + 1
        self.objetivos = objetivos
        self.visitados = padre.visitados if padre != None else set()
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
        
        direcciones = [(-1,0,1), (0,1,2), (1,0,3), (0,-1,0)]
        
        for dx, dy, op in direcciones:
            x = self.posicion[0] + dx
            y = self.posicion[1] + dy
            if x >= 0 and x < len(self.matriz) and y >= 0 and y < len(self.matriz[0]):
                if self.matriz[x][y] != 1:
                    hijo = Nodo(self.matriz, (x, y), self.objetivos, self, op)
                    hijo.objetivos_posiciones = self.objetivos_posiciones.copy()
                    hijos.append(hijo)
        
        return hijos
        
    
    def buscar_objetivos(self): 
        
        cola = Queue()
        cola.put(self)
        self.visitados.add( ( tuple(self.posicion), 0) )  # Inicializar con 0 objetivos recolectados

        while not cola.empty():    
            
            nodo = cola.get()
            
            # Verificar si la posición actual es un objetivo no recolectado
            if nodo.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4 and nodo.posicion not in nodo.objetivos_posiciones:
                nodo.objetivos_posiciones.append(nodo.posicion)
                if len(nodo.objetivos_posiciones) == nodo.objetivos:
                        return nodo

            # Generar hijos y procesar
            hijos = nodo.generar_hijos()

            
            for hijo in hijos:
                estado = (tuple(hijo.posicion), len(hijo.objetivos_posiciones))
                if estado not in nodo.visitados:
                    hijo.visitados.add(estado)        
                    cola.put(hijo)       
            
            # print(nodo.ver_matriz(nodo.obtener_ruta_matriz(nodo.obtener_ruta()))  )
            
                
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
            matriz[i[0]][i[1]] = "x"
        return matriz
        
            
    def __str__(self):
        return  f"Operador: {self.operador}\n Profundidad: {self.profundidad}\n Objetivos faltantes: {self.objetivos - len(self.objetivos_posiciones)}\n Posicion: {self.posicion}\n Costo: {self.costo}\n"
    



# Procesar matriz de texto 

matrix = process_map("/home/paelsam/proyecto-ia-uv/assets/maps_files/matrix4.txt")
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
print(objetivos.obtener_ruta())


print(objetivos.ver_matriz(objetivos.obtener_ruta_matriz(objetivos.obtener_ruta())))
    
    

# print(objetivos)


