Lista_errores = []

class Error():
    def __init__(self, token, tipo, desc, fila, columna):
        self.token = token
        self.tipo = tipo
        self.desc = desc
        self.fila = fila
        self.columna = columna
