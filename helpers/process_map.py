

def process_map(file_path):
    with open(file_path, "r") as file:
        # Crear la matriz correspondiente al archivo
        matrix = []
        data = file.readlines()
        for line in data:
            matrix.append([int(x) for x in line.split()])
    return matrix