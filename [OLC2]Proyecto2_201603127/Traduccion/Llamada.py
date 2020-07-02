from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Valores import *
from Traduccion.Tipos import *
from Errores import *

class clase_llamada(abst):
    def __init__(self, id, parametros, fila, columna):
        self.id = id
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.entorno = None
        self.variables_param = None
        self.ambito = None

    def verificar_tipo(self, ambito):
        if not ambito.existe_funcion(self.id):
            return False

        sim = ambito.get_funcion(self.id)
        param = sim.parametros
        tipo = sim.tipo

        if param is not None and self.parametros is not None:
            if len(param) == len(self.parametros):
                i = 0
                while i < len(self.parametros):
                    resultado = self.parametros[i].verificar_tipo(ambito)

                    if resultado != param[i][1]:
                        Err = Error("Llamada", "Semantico",
                                    "El parametro dado no es del mismo tipo que el del metodo", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False
                    i += 1
            else:
                Err = Error("Llamada", "Semantico", "No se estan dando los parametros correctamente",
                            self.fila, self.columna)
                Lista_errores.append(Err)
                return False

        self.ambito = ambito
        return tipo


    def generar_C3D(self):
        sim = self.ambito.get_funcion(self.id)
        param = sim.parametros

        conta = 0
        augus = ""

        if self.parametros is not None:
            for paramet in self.parametros:
                resultado = paramet.generar_C3D()
                augus += resultado[0]
                augus += str(param[conta][2]) + " = " + str(resultado[1]) + ";\n"
                conta += 1

        augus += "$ra = $ra + 1;\n"
        augus += "$s1[$ra] = " + str(get_global()) + ";\n"
        eti = new_etiqueta()
        add_etiquetaL(eti)
        incrementar_global()
        augus += "goto {};\n\n".format(self.id)
        augus += str(eti) + ":\n"
        augus += "$ra = $ra - 1;\n"

        return [augus, ""]


    def generar_AST(self, dot, nombre):
        nombre_hijo = "llamada_" + str(self.id) + "_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, self.id)

        if self.parametros is not None:
            nombre_temp = "parametros_" + new_nombre()
            dot.edge(nombre_hijo, nombre_temp)
            dot.node(nombre_temp, "Parametros")
            for param in self.parametros:
                param.generar_AST(dot,nombre_temp)
