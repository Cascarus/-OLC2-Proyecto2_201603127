from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Valores import *
from Traduccion.Tipos import *


class clase_main(abst):
    def __init__(self, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.entorno = None

    def agregar_Tabla(self, actual, ambito_actual):
        sim = Simbolo("main", Tipo_dato.ENTERO, "Funcion", ambito_actual, None, 0, "main", self.fila, self.columna)
        add_sim_report(sim)
        entorno_temp = ambito(actual)
        for inst in self.instrucciones:
            resultado = inst.agregar_Tabla(entorno_temp, ambito_actual + str('_main'))
            if resultado is False:
                return False
        self.entorno = entorno_temp
        return True

    def verificar_tipo(self, ambito):
        for inst in self.instrucciones:
            resultado = inst.verificar_tipo(self.entorno)
            if resultado is False:
                return False
        return True


    def generar_C3D(self):
        augus = ""

        augus += "$s0 = array();\n"
        augus += "$s1 = array();\n"
        augus += "$sp = 0;\n"
        augus += "$ra = -1;\n"


        for instr in self.instrucciones:
            resultado = instr.generar_C3D()
            augus += resultado[0]
        return [augus, ""]


    def generar_AST(self, dot, nombre):
        nombre_hijo = "main_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, "Main")

        for inst in self.instrucciones:
            inst.generar_AST(dot, nombre_hijo)