from Traduccion.Abstracta import abst
from Traduccion.Tipos import Tipo_dato
from Traduccion.Valores import *

class Primitivo(abst):
    def __init__(self, valor, tipo, fila, columna):
        self.valor = valor
        self.tipo = tipo
        self.fila = fila
        self.columna = columna


    def verificar_tipo(self, ambito_actual):
        if self.tipo == None:
            return False
        return self.tipo

    def generar_C3D(self, tipo_A = None):

        if tipo_A == "print":
            if self.tipo == Tipo_dato.CARACTER:
                return ["", "\'" + str(self.valor) + "\'"]
            elif self.tipo == Tipo_dato.CADENA:
                return ["", "\"" + str(self.valor) + "\""]
            else:
                return["", self.valor]

        if not isinstance(tipo_A, Tipo_dato):
            return ["", self.valor]

        if self.tipo == Tipo_dato.ENTERO:
            if tipo_A == Tipo_dato.DECIMAL:
                val1 = new_temp()
                val2 = new_temp()
                aug = str(val1) + " = " + str(self.valor) + ";\n"
                aug += str(val2) + " = (float)" + str(val1) + ";\n"
                return [aug, val2]
            elif tipo_A == Tipo_dato.CADENA:
                val1 = new_temp()
                val2 = new_temp()
                aug = str(val1) + " = " + str(self.valor) + ";\n"
                aug += str(val2) + " = (char)" + str(val1) + ";\n"
                return [aug, val2]
            else:
                return ["", self.valor]

        elif self.tipo == Tipo_dato.DECIMAL:
            if tipo_A == Tipo_dato.ENTERO:
                val1 = new_temp()
                val2 = new_temp()
                aug = str(val1) + " = " + str(self.valor) + ";\n"
                aug += str(val2) + " = (int)" + str(val1) + ";\n"
                return [aug, val2]
            elif tipo_A == Tipo_dato.CADENA:
                val1 = new_temp()
                val2 = new_temp()
                aug = str(val1) + " = " + str(self.valor) + ";\n"
                aug += str(val2) + " = (char)" + str(val1) + ";\n"
                return [aug, val2]
            else:
                return ["", self.valor]
        elif self.tipo == Tipo_dato.CARACTER:#dejar solo char
            if tipo_A == Tipo_dato.ENTERO:
                val1 = new_temp()
                val2 = new_temp()
                aug = str(val1) + " = \'" + str(self.valor) + "\';\n"#agregar comillas simples
                aug += str(val2) + " = (int)" + str(val1) + ";\n"
                return [aug, val2]
            elif tipo_A == Tipo_dato.DECIMAL:
                val1 = new_temp()
                val2 = new_temp()
                aug = str(val1) + " = \'" + str(self.valor) + "\';\n"#agregar comillas simples
                aug += str(val2) + " = (float)" + str(val1) + ";\n"
                return [aug, val2]
            else:
                return ["", "\'" + str(self.valor) + "\'"]