from Traduccion.Tipos import *
from Traduccion.Abstracta import abst
from Traduccion.Valores import new_temp

class Op_relacional(abst):
    def __init__(self, dato1, dato2, operacion, fila, columna):
        self.dato1 = dato1
        self.dato2 = dato2
        self.operacion = operacion
        self.fila = fila
        self.columna = columna


    def verificar_tipo(self, ambito_actual):
        tipo1 = self.dato1.verificar_tipo(ambito_actual)
        tipo2 = self.dato2.verificar_tipo(ambito_actual)

        if tipo1 == Tipo_dato.ENTERO and tipo2 == Tipo_dato.ENTERO:
            return Tipo_dato.ENTERO
        else:
            return False

    def generar_C3D(self, tipo_A = None):
        augus = ""
        dato1 = self.dato1.generar_C3D(tipo_A)
        dato2 = self.dato2.generar_C3D(tipo_A)
        augus += dato1[0]
        augus += dato2[0]

        val = new_temp()

        if self.operacion == Operacion_logica.MAYOR:
            augus += str(val) + " = " + str(dato1[1]) + " > " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Operacion_logica.MENOR:
            augus += str(val) + " = " + str(dato1[1]) + " < " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Operacion_logica.MAYOR_IGUAL:
            augus += str(val) + " = " + str(dato1[1]) + " >= " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Operacion_logica.MENOR_IGUAL:
            augus += str(val) + " = " + str(dato1[1]) + " <= " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Operacion_logica.DIFERENTE:
            augus += str(val) + " = " + str(dato1[1]) + " != " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Operacion_logica.IGUAL_IGUAL:
            augus += str(val) + " = " + str(dato1[1]) + " == " + str(dato2[1]) + ";" + "\n"

        return [augus, val]

