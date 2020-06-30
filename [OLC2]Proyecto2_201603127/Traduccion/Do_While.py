from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tipos import *
from Traduccion.Valores import *
from Traduccion.Break import Break
from Traduccion.Continue import Continue


class Do_While(abst):

    def __init__(self, condicion, contenido, fila, columna):
        self.condicion = condicion
        self.contenido = contenido
        self.fila = fila
        self.columna = columna
        self.entorno = None

    def agregar_Tabla(self, actual, ambito_actual):
        entorno_temp = ambito(actual)

        if self.condicion != None:
            resultado = self.condicion.agregar_Tabla(entorno_temp, ambito_actual + str('_do-while'))

            if resultado == False:
                return False

        if self.contenido != None:
            for inst in self.contenido:
                resultado = inst.agregar_Tabla(entorno_temp, ambito_actual + str('_do-while'))

            if resultado == False:
                return False

        self.entorno = entorno_temp
        return True

    def verificar_tipo(self, ambito):

        if self.condicion != None:
            resultado = self.condicion.verificar_tipo(self.entorno)

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
        label1 = new_etiqueta() #etiqueta do
        label2 = new_etiqueta() #condicion
        label3 = new_etiqueta() #etiqueta salida

        augus += "\n" + str(label1) + ":\n"

        if self.contenido != None:
            for inst in self.contenido:
                if isinstance(inst, Break):
                    augus += "goto " + label3 + "; #Break\n"
                elif isinstance(inst, Continue):
                    augus += "goto " + label2 + "; #Continue\n"
                else:
                    resultado = inst.generar_C3D()
                    augus += resultado[0]

        augus += "goto " + str(label2) + ";\n\n"
        augus += str(label2) + ":\n"

        condicion = self.condicion.generar_C3D()
        augus += condicion[0]

        augus += "if(!" + str(condicion[1]) + ") goto " + str(label3) + ";\n"
        augus += "goto " + str(label1) + ";\n\n"

        augus += str(label3) + ":\n"

        return [augus, ""]