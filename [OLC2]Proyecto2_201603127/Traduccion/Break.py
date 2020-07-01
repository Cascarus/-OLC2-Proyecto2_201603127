from Traduccion.Abstracta import abst
from Traduccion.Valores import new_nombre

class Break(abst):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def generar_AST(self, dot, nombre):
        nombre_hijo = "break_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, "Break")