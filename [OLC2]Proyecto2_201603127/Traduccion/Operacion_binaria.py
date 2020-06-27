from Traduccion.Tipos import *
from Traduccion.Abstracta import abst
from Traduccion.Valores import new_temp

class Operacion_binaria(abst):
    def __init__(self, dato1, dato2, operacion, fila, columna):
        self.dato1 = dato1
        self.dato2 = dato2
        self.operacion = operacion
        self.fila = fila
        self.columna = columna


    def verificar_tipo(self, ambito_actual):
        tipo1 = self.dato1.verificar_tipo(ambito_actual)
        tipo2 = self.dato2.verificar_tipo(ambito_actual)

        if tipo1 != False and tipo2 != False:
            #combinaciones
            if tipo1 == Tipo_dato.ENTERO and tipo2 == Tipo_dato.ENTERO:
                return Tipo_dato.ENTERO
            elif (tipo1 == Tipo_dato.ENTERO and tipo2 == Tipo_dato.DECIMAL) or (tipo1 == Tipo_dato.DECIMAL and tipo2 == Tipo_dato.ENTERO):
                return Tipo_dato.DECIMAL
            elif tipo1 == Tipo_dato.DECIMAL and tipo2 == Tipo_dato.DECIMAL:
                return Tipo_dato.DECIMAL

        else:
            return False#agregar error

    def generar_C3D(self, tipo_A = None):#(self, tipo_A)
        augus = ""
        dato1 = self.dato1.generar_C3D(tipo_A)
        dato2 = self.dato2.generar_C3D(tipo_A)
        augus += dato1[0]
        augus += dato2[0]

        val = new_temp()

        if self.operacion == Tipo_operacion.SUMA:
            #verificar los tipos y hacer el cast de una
            augus += str(val) + " = " + str(dato1[1]) + " + " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Tipo_operacion.RESTA:
            augus += str(val) + " = " + str(dato1[1]) + " - " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Tipo_operacion.POR:
            augus += str(val) + " = " + str(dato1[1]) + " * " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Tipo_operacion.DIVICION:
            augus += str(val) + " = " + str(dato1[1]) + " / " + str(dato2[1]) + ";" + "\n"
        else:
            augus += str(val) + " = " + str(dato1[1]) + " % " + str(dato2[1]) + ";" + "\n"

        return [augus, val]

