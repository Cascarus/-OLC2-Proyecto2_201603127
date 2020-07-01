from Traduccion.Abstracta import abst
from Traduccion.Valores import new_nombre

class Scanf(abst):

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def generar_C3D(self, ambito = None):
        return["", "read()"]

    def generar_AST(self, dot, nombre):
        nombre_hijo = "scanf_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, "Scanf")