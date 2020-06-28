from Traduccion.Tipos import *
from Traduccion.Abstracta import abst
from Traduccion.Valores import new_temp

class Operacion_unaria(abst):
    def __init__(self, dato, operacion, fila, columna):
        self.dato = dato
        self.operacion = operacion
        self.fila = fila
        self.columna = columna


    def verificar_tipo(self, ambito_actual):
        tipo1 = self.dato.verificar_tipo(ambito_actual)

        if tipo1 != False:
            #combinaciones
            if tipo1 == Tipo_dato.ENTERO:
                return Tipo_dato.ENTERO
            elif tipo1 == Tipo_dato.DECIMAL:
                return Tipo_dato.DECIMAL
        else:
            return False#agregar error

    def generar_C3D(self, tipo_A = None):#(self, tipo_A)
        augus = ""
        dato1 = self.dato1.generar_C3D(tipo_A)
        augus += dato1[0]

        val = new_temp()

        if self.operacion == tipo_unaria.MENOS:
            augus += str(val) + " = -" + str(dato1[1]) + ";\n"
        elif self.operacion == tipo_unaria.EXCLAMA:
            augus += str(val) + " = !" + str(dato1[1]) + ";\n"
        elif self.operacion == tipo_unaria.NOT:
            augus += str(val) + " = ~" + str(dato1[1]) +  ";\n"
        else:
            augus += str(val) + " = &" + str(dato1[1]) + ";\n"

        return [augus, val]