from Traduccion.Abstracta import abst
from Traduccion.Tipos import *
from Traduccion.Valores import *

class incre_decre(abst):
    def __init__(self, valor, operacion, posicion, fila, columna):
        self.valor = valor
        self.operacion = operacion
        self.posicion = posicion
        self.fila = fila
        self.columna = columna


    def verificar_tipo(self, ambito):
        tipo = self.valor.verificar_tipo(ambito)

        if tipo != False:
            # combinaciones
            if tipo == Tipo_dato.ENTERO:
                return Tipo_dato.ENTERO
            elif tipo == Tipo_dato.DECIMAL:
                return Tipo_dato.DECIMAL
            elif tipo == Tipo_dato.CARACTER:
                return Tipo_dato.CARACTER
            else:
                return False
        else:
            return False  # agregar error


    def generar_C3D(self, tipo_A = None):
        augus = ""
        dato1 = self.valor.generar_C3D(tipo_A)
        tipo = self.valor.get_tipo(tipo_A)
        augus += dato1[0]

        if self.posicion == 0:
            if tipo != Tipo_dato.CARACTER:
                if self.operacion == tipo_incre.INCRE:
                    augus += str(dato1[1]) + " = " + str(dato1[1]) + " + 1;\n"
                    return  [augus, dato1[1]]
                elif self.operacion == tipo_incre.DECRE:
                    augus += str(dato1[1]) + " = " + str(dato1[1]) + " - 1;\n"
                    return [augus, dato1[1]]
            else:
                if self.operacion == tipo_incre.INCRE:
                    val1 = new_temp()
                    val2 = new_temp()
                    augus += str(val1) + " = (int)" + str(dato1[1]) + ";\n"
                    augus += str(val1) + " = " + str(val1) + " + 1;\n"
                    augus += str(val2) + " = (char)" + str(val1) + ";\n"
                    augus += str(dato1[1]) + " = " + str(val2) + ";\n"
                    return [augus, dato1[1]]
                elif self.operacion == tipo_incre.DECRE:
                    val1 = new_temp()
                    val2 = new_temp()
                    augus += str(val1) + " = (int)" + str(dato1[1]) + ";\n"
                    augus += str(val1) + " = " + str(val1) + " - 1;\n"
                    augus += str(val2) + " = (char)" + str(val1) + ";\n"
                    augus += str(dato1[1]) + " = " + str(val2) + ";\n"
                    return [augus, dato1[1]]
        else:
            val = new_temp()
            if tipo != Tipo_dato.CARACTER:
                if self.operacion == tipo_incre.INCRE:
                    augus += str(val) + " = " + str(dato1[1]) + ";\n"
                    augus += str(dato1[1]) + " = " + str(dato1[1]) + " + 1;\n"
                elif self.operacion == tipo_incre.DECRE:
                    augus += str(val) + " = " + str(dato1[1]) + ";\n"
                    augus += str(dato1[1]) + " = " + str(dato1[1]) + " - 1;\n"
            else:
                if self.operacion == tipo_incre.INCRE:
                    val1 = new_temp()
                    val2 = new_temp()
                    augus += str(val) + " = " + str(dato1[1]) + ";\n"
                    augus += str(val1) + " = (int)" + str(dato1[1]) + ";\n"
                    augus += str(val1) + " = " + str(val1) + " + 1;\n"
                    augus += str(val2) + " = (char)" + str(val1) + ";\n"
                    augus += str(dato1[1]) + " = " + str(val2) + ";\n"
                elif self.operacion == tipo_incre.DECRE:
                    val1 = new_temp()
                    val2 = new_temp()
                    augus += str(val) + " = " + str(dato1[1]) + ";\n"
                    augus += str(val1) + " = (int)" + str(dato1[1]) + ";\n"
                    augus += str(val1) + " = " + str(val1) + " + 1;\n"
                    augus += str(val2) + " = (char)" + str(val1) + ";\n"
                    augus += str(dato1[1]) + " = " + str(val2) + ";\n"

            return [augus, val]

    def generar_AST(self, dot, nombre):
        nombre_hijo = ""
        name = ""
        if self.operacion == tipo_incre.INCRE:
            nombre_hijo += "masmas_" + str(new_nombre())
            name += "++"
        else:
            nombre_hijo += "menosmenos_" + new_nombre()
            name += "--"

        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, name)
        self.valor.generar_AST(dot, nombre_hijo)