from Traduccion.Abstracta import abst
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Tipos import Tipo_dato
from Traduccion.Valores import *
from Errores import *

class var_arry(abst):
    def __init__(self, id, dimensiones, fila, columna):
        self.id = id
        self.dimensiones = dimensiones
        self.fila = fila
        self. columna = columna
        self.entorno = None

    def verificar_tipo(self, actual):
        simbolo = actual.get_simbol(self.id)

        if self.dimensiones != None:
            for dim in self.dimensiones:
                retorno =  dim.verificar_tipo(actual)

                if retorno == False or retorno == Tipo_dato.CADENA:
                    print("ERROR: NO EXISTE LA VARIABLE " + str(self.id))
                    Err = Error("Variable", "Semantico", "No existe la variable", self.fila,
                                self.columna)
                    Lista_errores.append(Err)
                    return False

        self.entorno = actual
        return simbolo.tipo


    def generar_C3D(self, ambt = None):
        augus = ""
        conta = 0
        ultimo_temp = 0
        simbolo = self.entorno.get_simbol(self.id)

        if self.dimensiones != None:
            for dim in self.dimensiones:
                resultado = dim.generar_C3D()
                augus += resultado[0]

                if resultado[0] == "":
                    temp = new_temp()
                    if conta == 0:
                        augus += str(temp) + " = " + str(resultado[1]) + ";\n"
                        augus += str(temp) + " = " + str(temp) + " + 1;\n"
                        ultimo_temp = temp

                    else:
                        augus += str(temp) + " = " + str(resultado[1]) + " + 1;\n"
                        augus += str(temp) + " = " + str(temp) + " * " + str(ultimo_temp) + ";\n"
                        ultimo_temp = temp
                else:
                    if conta == 0:
                        augus += str(resultado[1]) + " = " + str(resultado[1]) + " + 1;\n"
                        ultimo_temp = resultado[1]
                    else:
                        augus += str(resultado[1]) + " = " + str(resultado[1]) + " + 1;\n"
                        augus += str(resultado[1]) + " = " + str(resultado[1]) + " * " + ultimo_temp + ";\n"
                        ultimo_temp = str(resultado[1])
                conta += 1
            temp = new_temp()
            augus += str(ultimo_temp) + " = " + str(ultimo_temp) + " - 1;\n"
            augus += str(temp) + " = " + str(simbolo.var_aug) + "[" + str(ultimo_temp) + "];\n"

            return [augus, temp]

        else:
            return ["", simbolo.var_aug]


    def generar_AST(self, dot, nombre):
        nombre_hijo = str(self.id) + "_" + str(new_nombre())
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, self.id)