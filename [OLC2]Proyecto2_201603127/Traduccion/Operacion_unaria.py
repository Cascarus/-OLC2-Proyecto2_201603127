from Traduccion.Tipos import *
from Traduccion.Abstracta import abst
from Traduccion.Valores import *
from Errores import *

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
            Err = Error("Operacion Unaria", "Semantico", "No se puede hacer unarias de Cadenas o Caracteres",
                        self.fila, self.columna)
            Lista_errores.append(Err)
            return False#agregar error

    def generar_C3D(self, tipo_A = None):#(self, tipo_A)
        augus = ""
        dato1 = self.dato.generar_C3D(tipo_A)
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

    def generar_AST(self, dot, nombre):
        nombre_hijo = ""
        name = ""
        if self.operacion == tipo_unaria.MENOS:
            nombre_hijo += "Umenos_" + str(new_nombre())
            name += "-"
        elif self.operacion == tipo_unaria.EXCLAMA:
            nombre_hijo += "Uexclama_" + str(new_nombre())
            name += "!"
        elif self.operacion == tipo_unaria.NOT:
            nombre_hijo += "Unot_" + new_nombre()
            name += "~"
        else:
            nombre_hijo += "Uand_" + new_nombre()
            name += "&"

        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, name)
        self.dato.generar_AST(dot, nombre_hijo)