from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tipos import Tipo_dato
from Traduccion.Valores import new_etiqueta

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
                    return False
            self.entornos_if.append(entorno_temp)

        entorno_temp = ambito(actual)
        if self.cont_else != None:
            for cont in self.cont_else:
                resultado = cont.agregar_Tabla(entorno_temp, ambito_actual + "_else")

                if resultado == False:
                    return False

        self.entornos_else = entorno_temp

        return True



    def verificar_tipo(self, ambito = None):
        conta = 0

        while conta < len(self.operaciones):
            resultado = self.operaciones[conta].verificar_tipo(self.entornos_if[conta])

            if resultado == False:
                return False
            elif resultado != Tipo_dato.ENTERO:
                return False

            for inst in self.contenido[conta]:
                resultado = inst.verificar_tipo(self.entornos_if[conta])

                if resultado == False:
                    return False

            conta += 1

        if self.cont_else != None:
            for inst in self.cont_else:
                resultado = inst.verificar_tipo(self.entornos_else)

                if resultado == False:
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

