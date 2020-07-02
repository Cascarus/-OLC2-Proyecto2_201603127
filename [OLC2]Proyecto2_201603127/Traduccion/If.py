from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tipos import Tipo_dato
from Traduccion.Valores import *
from Errores import *


class If(abst):
    def __init__(self, operaciones, contenido, cont_else, fila, columna):
        self.operaciones = operaciones
        self.contenido = contenido
        self.cont_else = cont_else
        self.fila = fila
        self.columna = columna
        self.entornos_if = []
        self.entornos_else = None

    def agregar_Tabla(self, actual, ambito_actual):
        estado = True

        for cont in self.contenido:
            entorno_temp = ambito(actual)

            for inst in cont:
                resultado = inst.agregar_Tabla(entorno_temp, ambito_actual + str('_if' if estado else "_elif"))
                estado = False

                if resultado == False:
                    Err = Error("If", "Semantico", "Ha fallado alguan asignacion o declaracion",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False
            self.entornos_if.append(entorno_temp)

        entorno_temp = ambito(actual)
        if self.cont_else != None:
            for cont in self.cont_else:
                resultado = cont.agregar_Tabla(entorno_temp, ambito_actual + "_else")

                if resultado == False:
                    Err = Error("Else", "Semantico", "Algo ha fallado en el else",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False

        self.entornos_else = entorno_temp

        return True

    def verificar_tipo(self, ambito=None):
        conta = 0

        while conta < len(self.operaciones):
            resultado = self.operaciones[conta].verificar_tipo(self.entornos_if[conta])

            if resultado == False:
                Err = Error("If", "Semantico", "La condicion no es de tipo entero",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False
            elif resultado != Tipo_dato.ENTERO:
                Err = Error("If", "Semantico", "La condicion no es de tipo entero",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

            for inst in self.contenido[conta]:
                resultado = inst.verificar_tipo(self.entornos_if[conta])

                if resultado == False:
                    Err = Error("If", "Semantico", "Algo ha fallado en el cuerpo del if",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False

            conta += 1

        if self.cont_else != None:
            for inst in self.cont_else:
                resultado = inst.verificar_tipo(self.entornos_else)

                if resultado == False:
                    Err = Error("Else", "Semantico", "Algo ha pasado en el cuerpo de else",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False

        return True

    def generar_C3D(self):
        augus = ""
        label = new_etiqueta()

        conta = 0
        while conta < len(self.operaciones):
            resultado = self.operaciones[conta].generar_C3D()
            augus += resultado[0]
            label2 = new_etiqueta()

            augus += "if(!" + str(resultado[1]) + ") goto " + str(label2) + ";\n"

            for inst in self.contenido[conta]:
                resultado = inst.generar_C3D()
                augus += resultado[0]

            augus += "goto " + str(label) + ";\n\n"
            augus += str(label2) + ":\n"

            conta += 1

        if self.cont_else != None:
            for inst in self.cont_else:
                resultado = inst.generar_C3D()
                augus += resultado[0]

        augus += "\n" + str(label) + ":\n"

        return [augus, ""]

    def generar_AST(self, dot, nombre):
        conta = 0

        nombre_h1 = "sent_if_" + new_nombre()
        dot.edge(nombre, nombre_h1)
        dot.node(nombre_h1, "Sentencia If")
        while conta < len(self.operaciones):
            nombre_hijo = ""
            if conta == 0:
                nombre_hijo = "if_" + new_nombre()
                dot.edge(nombre_h1, nombre_hijo)
                dot.node(nombre_hijo, "If")
            else:
                nombre_hijo = "elif_" + new_nombre()
                dot.edge(nombre_h1, nombre_hijo)
                dot.node(nombre_hijo, "Else If")
            self.operaciones[conta].generar_AST(dot, nombre_hijo)

            for inst in self.contenido[conta]:
                inst.generar_AST(dot, nombre_hijo)

            conta += 1

        if self.cont_else is not None:
            nombre_hijo = "else_" + new_nombre()
            dot.edge(nombre_h1, nombre_hijo)
            dot.node(nombre_hijo, "Else")

            for inst in self.cont_else:
                inst.generar_AST(dot, nombre_hijo)
