from Traduccion.Abstracta import abst

class Scanf(abst):

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def generar_C3D(self, ambito = None):
        return["", "read()"]