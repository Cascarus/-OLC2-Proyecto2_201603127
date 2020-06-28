from Traduccion.Tipos import *
from Traduccion.Abstracta import abst
from Traduccion.Valores import new_temp
from Traduccion.Variables import variables
from Traduccion.Primitivos import Primitivo

class Op_logica(abst):
    def __init__(self, dato1, dato2, operacion, fila, columna):
        self.dato1 = dato1
        self.dato2 = dato2
        self.operacion = operacion
        self.fila = fila
        self.columna = columna


    def verificar_tipo(self, ambito_actual):
        tipo1 = self.dato1.verificar_tipo(ambito_actual)
        tipo2 = self.dato2.verificar_tipo(ambito_actual)

        if tipo1 == Tipo_dato.ENTERO:
            if tipo2 == Tipo_dato.ENTERO:
                return Tipo_dato.ENTERO
            elif tipo2 == Tipo_dato.DECIMAL:
                return Tipo_dato.ENTERO
            elif tipo2 == Tipo_dato.CARACTER:
                return Tipo_dato.ENTERO
            else:
                print("ERROR: No se puden comparar INT con CADENAS")
                return False
        elif tipo1 == Tipo_dato.DECIMAL:
            if tipo2 == Tipo_dato.ENTERO:
                return Tipo_dato.ENTERO
            elif tipo2 == Tipo_dato.DECIMAL:
                return Tipo_dato.ENTERO
            elif tipo2 == Tipo_dato.CARACTER:
                return Tipo_dato.ENTERO
            else:
                print("ERROR: No se puden comparar DECIMALES con CADENAS")
                return False
        elif tipo1 == Tipo_dato.CARACTER:
            if tipo2 == Tipo_dato.ENTERO:
                return Tipo_dato.ENTERO
            elif tipo2 == Tipo_dato.DECIMAL:
                return Tipo_dato.ENTERO
            elif tipo2 == Tipo_dato.CARACTER:
                return Tipo_dato.ENTERO
            else:
                print("ERROR: No se puden comparar DECIMALES con CADENAS")
                return False
        else:
            return False

    def generar_C3D(self, tipo_A = None):#(self, tipo_A)
        augus = ""
        dato1 = []
        dato2 = []
        if isinstance(self.dato1, variables):
            dato1 = self.dato1.generar_C3D(tipo_A)
            tipo1 = self.dato1.get_tipo(tipo_A)
        elif isinstance(self.dato1, Primitivo):
            tipo1 = self.dato1.get_tipo()
            if (tipo1 != False and tipo1 == Tipo_dato.ENTERO) or (tipo1 != False and tipo1 == Tipo_dato.DECIMAL):
                dato1 = self.dato1.generar_C3D(tipo_A)
            elif tipo1 != False and tipo1 == Tipo_dato.CARACTER:
                dato1 = self.dato1.generar_C3D(Tipo_dato.ENTERO)
            else:
                dato1 = self.dato1.generar_C3D(tipo_A)
        else:
            dato1 = self.dato1.generar_C3D(tipo_A)

        if isinstance(self.dato2, variables):
            dato2 = self.dato2.generar_C3D(tipo_A)
            tipo2 = self.dato2.get_tipo(tipo_A)
        elif isinstance(self.dato2, Primitivo):
            tipo2 = self.dato2.get_tipo()
            if (tipo2 != False and tipo2 == Tipo_dato.ENTERO) or (tipo2 != False and tipo2 == Tipo_dato.DECIMAL):
                dato2 = self.dato2.generar_C3D(tipo_A)
            elif tipo2 != False and tipo2 == Tipo_dato.CARACTER:
                dato2 = self.dato2.generar_C3D(Tipo_dato.ENTERO)
            else:
                dato2 = self.dato2.generar_C3D(tipo_A)
        else:
            dato2 = self.dato2.generar_C3D(tipo_A)

        augus += dato1[0]
        augus += dato2[0]

        val = new_temp()

        if self.operacion == Operacion_logica.AND:
            #verificar los tipos y hacer el cast de una
            augus += str(val) + " = " + str(dato1[1]) + " && " + str(dato2[1]) + ";" + "\n"
        elif self.operacion == Operacion_logica.OR:
            augus += str(val) + " = " + str(dato1[1]) + " || " + str(dato2[1]) + ";" + "\n"

        return [augus, val]

