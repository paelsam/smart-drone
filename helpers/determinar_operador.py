# Operadores
# 0: Izquierda
# 1: Arriba
# 2: Derecha
# 3: Abajo

def determinar_operador(operador):
    if operador == 0:
        return "Izquierda"
    elif operador == 1:
        return "Arriba"
    elif operador == 2:
        return "Derecha"
    elif operador == 3:
        return "Abajo"
    else:
        return "Operador no válido"