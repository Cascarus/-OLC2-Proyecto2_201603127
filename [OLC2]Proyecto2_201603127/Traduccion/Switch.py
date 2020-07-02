from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tipos import Tipo_dato
from Traduccion.Valores import *
from Traduccion.Break import Break
from Errores import *

class Switch(abst):
    def __init__(self, variable, cases, default, fila, columna):
        self.variable = variable
        self.cases = cases
        self.default = default
        self.fila = fila
        self.columna = columna
        self.entornos_cases = None
        self.entorno_default = None


    def agregar_Tabla(self, actual, ambito_actual):
        entorno_temp = ambito(actual)

        if self.cases != None:
            for cont in self.cases:
                for inst in cont[1]:
                    resultado = inst.agregar_Tabla(entorno_temp, ambito_actual + str('_switch'))

                    if resultado == False:
                        Err = Error("Switch", "Semantico",
                                    "No se pudo crear el Case", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False

        self.entornos_cases = entorno_temp

        entorno_temp = ambito(actual)
        if self.default != None:
            for cont in self.default:
                resultado = cont.agregar_Tabla(entorno_temp, ambito_actual + "_switch")

                if resultado == False:
                    Err = Error("Switch", "Semantico", "No se puede crear el default",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False

        self.entorno_default = entorno_temp

        return True



    def verificar_tipo(self, ambito = None):

        if self.variable != None:
            resultado = self.variable.verificar_tipo(ambito)

            if resultado == False:
                Err = Error("Switch", "Semantico", "El tipo de la variable no es valido para el Switch",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        if self.cases != None:
            for caso in self.cases:
                if caso[0] != None:
                    resultado = caso[0].verificar_tipo(ambito)
                    if resultado == False:
                        Err = Error("Switch", "Semantico",
                                    "Algo salio mal en el seitch", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False

                for inst in caso[1]:
                    resultado = inst.verificar_tipo(self.entornos_cases)

                    if resultado == False:
                        Err = Error("Switch", "Semantico",
                                    "EL caso no se puede crear", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False

        if self.default != None:
            for inst in self.default:
                resultado = inst.verificar_tipo(self.entorno_default)

                if resultado == False:
                    Err = Error("Switch", "Semantico", "El default no se pudo crear",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False

        return True


    def generar_C3D(self):
        augus = ""

        resultado = self.variable.generar_C3D()
        augus += resultado[0]
        salida = new_etiqueta()

        if self.cases != None:

            for i in self.cases:
                '''print("si entro")'''

            for coso in self.cases:
                codigo_case = coso[0].generar_C3D()
                label1 = new_etiqueta()
                label2 = new_etiqueta()
                augus += "if(" + str(resultado[1]) + " == " + str(codigo_case[1]) + ") goto " + str(label1) + ";\n"
                augus += "goto " + str(label2) + ";\n\n"
                augus += str(label1) + ":\n"

                for inst in coso[1]:
                    if isinstance(inst, Break):
                        augus += "goto " + salida + ";\n\n"
                    else:
                        contenido = inst.generar_C3D()
                        augus += contenido[0]

                augus += str(label2) + ":\n"

        if self.default != None:
            for inst in self.default:
                contenido = inst.generar_C3D()
                augus += contenido[0]

        augus += "\n" + salida + ":\n"

        return [augus, ""]


    def generar_AST(self, dot, nombre):
        nombre_hijo = "switch_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, "Switch")

        for inst in self.cases:
            nombre_case = "case_" + new_nombre()
            dot.edge(nombre_hijo, nombre_case)
            dot.node(nombre_case, "Case: " + str(inst[0].valor))

            for cont in inst[1]:
                cont.generar_AST(dot, nombre_case)

        if self.default is not None:
            nombre_default = "default_" + new_nombre()
            dot.edge(nombre_hijo, nombre_default)
            dot.node(nombre_default, "Default")
            for inst in self.default:
                inst.generar_AST(dot, nombre_default)

