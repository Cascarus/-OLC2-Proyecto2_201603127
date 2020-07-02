from Traduccion.Abstracta import abst
from Traduccion.Variables import variables
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Valores import *
from Traduccion.Tipos import Tipo_dato


class Goto(abst):
    def __init__(self, etiqueta, fila, columna):
        self.etiqueta = etiqueta
        self.fila = fila
        self.columna = columna

    def generar_C3D(self):
        augus = "goto " + str(self.etiqueta) + ";\n"
        return [augus, ""]

    def generar_AST(self, dot, nombre):
        nombre_hijo = "etiqueta_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, "Etiqueta\n" + str(self.etiqueta))
