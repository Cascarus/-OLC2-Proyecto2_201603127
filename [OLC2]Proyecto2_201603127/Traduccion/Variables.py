from Traduccion.Abstracta import abst
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Tipos import Tipo_dato
from Traduccion.Valores import *

class variables(abst):
    def __init__(self, id, fila, columna):
        self.id = id
        self.fila = fila
        self. columna = columna
        self.entorno = None

    def verificar_tipo(self, actual):
        simbolo = actual.get_simbol(self.id)

        if simbolo != False:
            self.entorno = actual
            return simbolo.tipo
        print("ERROR: NO EXISTE LA VARIABLE " + str(self.id))
        return False

    def generar_C3D(self, ambt = None):
        simbolo = self.entorno.get_simbol(self.id)
        return ["", simbolo.var_aug]

    def get_tipo(self,ambt = None):
        simbolo = self.entorno.get_simbol(self.id)
        return simbolo.tipo

    def generar_AST(self, dot, nombre):
        nombre_hijo = str(self.id) + "_" + str(new_nombre())
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, self.id)



