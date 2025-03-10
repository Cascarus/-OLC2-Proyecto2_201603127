from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tipos import *
from Traduccion.Declaracion import Declaracion
from Traduccion.Valores import *
from Traduccion.Break import Break
from Traduccion.Continue import Continue
from Errores import *


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
                Err = Error("For", "Semantico", "Ha fallado la asignacion o declaracion de la variable de iteracion",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        if self.condicion != None:
            resultado = self.condicion.agregar_Tabla(entorno_temp, ambito_actual + str('_for'))

            if resultado == False:
                Err = Error("For", "Semantico", "La condicion no devuelve un tipo entero",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        if self.incre_decre != None:
            resultado = self.incre_decre.agregar_Tabla(entorno_temp, ambito_actual + str('_for'))

            if resultado == False:
                Err = Error("For", "Semantico", "El incremento ha fallado",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        if self.contenido != None:
            for inst in self.contenido:
                resultado = inst.agregar_Tabla(entorno_temp, ambito_actual + str('_for'))

            if resultado == False:
                Err = Error("For", "Semantico", "algo ha fallado en le contenido",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        self.entorno = entorno_temp
        return True

    def verificar_tipo(self, ambito):
        if self.variable != None:
            resultado = self.variable.verificar_tipo(self.entorno)

            if resultado == False or resultado == Tipo_dato.CARACTER or resultado == Tipo_dato.CADENA:
                Err = Error("For", "Semantico", "Solo se puede utilizar una variable de tipo int para iterar",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False


        if self.condicion != None:
            resultado = self.condicion.verificar_tipo(self.entorno)

            if resultado == False or resultado == Tipo_dato.CARACTER or resultado == Tipo_dato.CADENA:
                Err = Error("For", "Semantico", "La condicion no devuelve un tipo entero",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        if self.incre_decre != None:
            resultado = self.incre_decre.verificar_tipo(self.entorno)

            if resultado == False or resultado == Tipo_dato.CARACTER or resultado == Tipo_dato.CADENA:
                Err = Error("For", "Semantico", "Solo se puede utilizar una variable de tipo int para el incremento o decremento",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        if self.contenido != None:
            for instr in self.contenido:
                resultado = instr.verificar_tipo(self.entorno)

                if resultado == False:
                    Err = Error("For", "Semantico", "Algo a fallado en el cuerpo",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False

        return True

    def generar_C3D(self):
        augus  = ''

        if isinstance(self.variable, Declaracion):
            resultado = self.variable.generar_C3D()
            augus += resultado[0]

            label1 = new_etiqueta()# etiqueta for
            label2 = new_etiqueta()# etiqueta de salida
            label3 = new_etiqueta()#etiqueta de aumento
            augus += "\n" + str(label1) + ":\n"

            condicion = self.condicion.generar_C3D()
            augus += condicion[0]

            augus += "if(!" + str(condicion[1]) + ") goto " + str(label2) + ";\n"

            if self.contenido is not None:
                for inst in self.contenido:
                    print("Si paso puto")

            if self.contenido is not None:
                for inst in self.contenido:
                    if isinstance(inst, Break):
                        augus += "goto " + label2 + "; #Break\n"
                    elif isinstance(inst, Continue):
                        augus += "goto " + label3 + "; #Continue\n"
                    else:
                        resultado = inst.generar_C3D()
                        augus += resultado[0]

            augus += "\n" + label3 + ":\n"
            incre_decre = self.incre_decre.generar_C3D()
            augus += incre_decre[0]

            augus += "goto " + str(label1) + ";\n\n"
            augus += str(label2) + ":\n"

            return [augus, ""]

        else:
            resultado = self.variable.generar_C3D()
            augus += resultado[0]

            label1 = new_etiqueta()  # etiqueta for
            label2 = new_etiqueta()  # etiqueta de salida
            label3 = new_etiqueta()  # etiqueta de aumento

            set_etiqueta_continue(label3)
            set_etiqueta_break(label2)
            augus += "\n" + str(label1) + ": #etiqueta for\n"

            condicion = self.condicion.generar_C3D()
            augus += condicion[0]

            augus += "if(!" + str(condicion[1]) + ") goto " + str(label2) + ";\n"


            if self.contenido != None:
                for inst in self.contenido:
                    if isinstance(inst, Break):
                        augus += "goto " + label2 + "; #Break\n"
                    elif isinstance(inst, Continue):
                        augus += "goto " + label3 + "; #Continue\n"
                    else:
                        resultado = inst.generar_C3D()
                        augus += resultado[0]

            augus += "\n" + label3 + ": #etiqueta incre_decre\n"
            incre_decre = self.incre_decre.generar_C3D()
            augus += incre_decre[0]
            augus += "goto " + str(label1) + ";\n\n"
            augus += str(label2) + ": #etiqueta salida for\n"

            get_etiqueta_break()
            get_etiqueta_continue()

            return [augus, ""]

    def generar_AST(self, dot, nombre):
        nombre_hijo = "for_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, "For")

        self.variable.generar_AST(dot, nombre_hijo)
        self.condicion.generar_AST(dot, nombre_hijo)
        self.incre_decre.generar_AST(dot, nombre_hijo)

        nombre_2 = "cont_for_" + new_nombre()
        dot.edge(nombre_hijo, nombre_2)
        dot.node(nombre_2, "Contenido\n For")

        for inst in self.contenido:
            inst.generar_AST(dot, nombre_2)


