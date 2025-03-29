from queue import Queue
from helpers.process_map import process_map
from helpers.determinar_operador import determinar_operador
from helpers.process_path import process_path
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
        self.nodos_expandidos = 0
        
    
    def ver_matriz(self, matriz) -> str:
        result = ""
        for i in matriz:
            for j in i:
                result += str(j) + " "
            result += "\n"
        return result

    def generar_hijos(self) -> list:
        
        hijos = []
        
        direcciones = [(-1, 0, 0), (0, -1, 1), (1, 0, 2), (0, 1, 3)]  # (dy, dx, operador)
        
        for dy, dx, op in direcciones:
            y = self.posicion[0] + dy  # Mueve la fila
            x = self.posicion[1] + dx  # Mueve la columna
            if 0 <= y < len(self.matriz) and 0 <= x < len(self.matriz[0]):
                if self.matriz[y][x] != 1:
                    hijo = Nodo(self.matriz, (y, x), self.objetivos, self, op)
                    hijo.objetivos_posiciones = self.objetivos_posiciones.copy()
                    hijos.append(hijo)
        
        return hijos
        
    
    def buscar_objetivos(self) -> object | None: 
        
        cola = Queue()
        cola.put(self)
        self.visitados.add( ( tuple(self.posicion), 0) )  # Inicializar con 0 objetivos recolectados
        nodos_expandidos = 0

        while not cola.empty():    
            
            nodo = cola.get()
            
            # Verificar si la posición actual es un objetivo no recolectado
            if nodo.matriz[nodo.posicion[0]][nodo.posicion[1]] == 4 and nodo.posicion not in nodo.objetivos_posiciones:
                nodo.objetivos_posiciones.append(nodo.posicion)
                if len(nodo.objetivos_posiciones) == nodo.objetivos:
                        nodo.nodos_expandidos = nodos_expandidos
                        return nodo

            # Generar hijos y procesar
            hijos = nodo.generar_hijos()
            
            
            for hijo in hijos:
                estado = (tuple(hijo.posicion), len(hijo.objetivos_posiciones))
                # print("Estado: ", estado)   
                if estado not in nodo.visitados:
                    hijo.visitados.add(estado)        
                    cola.put(hijo)     
            
            nodos_expandidos += 1
               
                
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
        return  f"Operador: {determinar_operador(self.operador)}\nProfundidad: {self.profundidad}\nObjetivos faltantes: {self.objetivos - len(self.objetivos_posiciones)}\nPosicion: {self.posicion}\nCosto: {self.costo}\n"
