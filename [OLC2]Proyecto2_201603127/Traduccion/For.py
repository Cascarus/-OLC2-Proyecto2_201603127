from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tipos import *
from Traduccion.Declaracion import Declaracion
from Traduccion.Valores import *
from Traduccion.Break import Break
from Traduccion.Continue import Continue


class For(abst):

    def __init__(self, variable, condicion, incre_decre, contenido, fila, columna):
        self.variable = variable
        self.condicion = condicion
        self.incre_decre = incre_decre
        self.contenido = contenido
        self.fila = fila
        self.columna = columna
        self.entorno = None

    def agregar_Tabla(self, actual, ambito_actual):
        entorno_temp = ambito(actual)
        if self.variable != None:
            resultado = self.variable.agregar_Tabla(entorno_temp, ambito_actual + str('_for'))

            if resultado == False:
                return False

        if self.condicion != None:
            resultado = self.condicion.agregar_Tabla(entorno_temp, ambito_actual + str('_for'))

            if resultado == False:
                return False

        if self.incre_decre != None:
            resultado = self.incre_decre.agregar_Tabla(entorno_temp, ambito_actual + str('_for'))

            if resultado == False:
                return False

        if self.contenido != None:
            for inst in self.contenido:
                resultado = inst.agregar_Tabla(entorno_temp, ambito_actual + str('_for'))

            if resultado == False:
                return False

        self.entorno = entorno_temp
        return True

    def verificar_tipo(self, ambito):
        if self.variable != None:
            resultado = self.variable.verificar_tipo(self.entorno)

            if resultado == False or resultado == Tipo_dato.CARACTER or resultado == Tipo_dato.CADENA:
                return False


        if self.condicion != None:
            resultado = self.condicion.verificar_tipo(self.entorno)

            if resultado == False or resultado == Tipo_dato.CARACTER or resultado == Tipo_dato.CADENA:
                return False

        if self.incre_decre != None:
            resultado = self.incre_decre.verificar_tipo(self.entorno)

            if resultado == False or resultado == Tipo_dato.CARACTER or resultado == Tipo_dato.CADENA:
                return False

        if self.contenido != None:
            for instr in self.contenido:
                resultado = instr.verificar_tipo(self.entorno)

                if resultado == False:
                    return False

        return True

    def generar_C3D(self):
        augus  = ''

        if isinstance(self.variable, Declaracion):
            resultado = self.variable.generar_C3D()
            augus += resultado[0]

            label1 = new_etiqueta()# etiqueta for
            label2 = new_etiqueta()# etiqueta de salida
            augus += "\n" + str(label1) + ":\n"

            condicion = self.condicion.generar_C3D()
            augus += condicion[0]

            augus += "if(!" + str(condicion[1]) + ") goto " + str(label2) + ";\n"
            incre_decre = self.incre_decre.generar_C3D()
            augus += incre_decre[0]

            if self.contenido != None:
                for inst in self.contenido:
                    if isinstance(inst, Break):
                        augus += "goto " + label2 + "; #Break\n"
                    elif isinstance(inst, Continue):
                        augus += "goto " + label1 + "; #Continue\n"
                    else:
                        resultado = inst.generar_C3D()
                        augus += resultado[0]

            augus += "goto " + str(label1) + ";\n\n"
            augus += str(label2) + ":\n"

            return [augus, ""]

        else:
            resultado = self.variable.generar_C3D()
            augus += resultado[0]

            label1 = new_etiqueta()  # etiqueta for
            label2 = new_etiqueta()  # etiqueta de salida
            augus += "\n" + str(label1) + ":\n"

            condicion = self.condicion.generar_C3D()
            augus += condicion[0]

            augus += "if(!" + str(condicion[1]) + ") goto " + str(label2) + ";\n"
            incre_decre = self.incre_decre.generar_C3D()
            augus += incre_decre[0]

            if self.contenido != None:
                for inst in self.contenido:
                    if isinstance(inst, Break):
                        augus += "goto " + label2 + "; #Break\n"
                    elif isinstance(inst, Continue):
                        augus += "goto " + label1 + "; #Continue\n"
                    else:
                        resultado = inst.generar_C3D()
                        augus += resultado[0]



            augus += "goto " + str(label1) + ";\n\n"
            augus += str(label2) + ":\n"

            return [augus, ""]

