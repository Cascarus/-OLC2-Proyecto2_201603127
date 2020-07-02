from Traduccion.Abstracta import abst
from Traduccion.Ambito import ambito
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Valores import *
from Traduccion.Tipos import *


class clase_metodos(abst):
    def __init__(self, id, parametros, instrucciones, fila, columna):
        self.id = id
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.entorno = None
        self.variables_param = None

    def agregar_Tabla(self, actual, ambito_actual):
        entorno_temp = ambito(actual)
        list_temp = []
        if self.parametros != None:
            for param in self.parametros:
                temp = new_param()
                param.append(temp)
                list_temp.append(param[0])

        dev = str(new_dev())

        sim1 = Simbolo(self.id, "Void", "Metodo", ambito_actual, self.parametros, 0, dev, self.fila, self.columna)
        actual.agregar_funcion(self.id, sim1)
        sim2 = Simbolo(self.id, "Void", "Metodo", ambito_actual, list_temp, 0, dev, self.fila, self.columna)
        add_sim_report(sim2)

        if self.parametros != None:
            for param in self.parametros:
                if not entorno_temp.exite_aqui(str(param[0])):
                    sim = Simbolo(param[0], param[1], "variable", ambito_actual + "_" + str(self.id), None, 0, param[2], self.fila,
                                  self.columna)
                    add_sim_report(sim)
                    entorno_temp.agregar_simbolo(sim)
                else:
                    print("la variable ya existe y no se puede vovler a declarar")
                    return False

        for inst in self.instrucciones:
            resultado = inst.agregar_Tabla(entorno_temp, ambito_actual + "_" + str(self.id))
            if resultado is False:
                return False
        self.entorno = entorno_temp
        return True

    def verificar_tipo(self, ambito):
        for inst in self.instrucciones:
            resultado = inst.verificar_tipo(self.entorno)
            if resultado is False:
                return False
        return True


    def generar_C3D(self):
        augus = str(self.id) + ":\n"

        sim = self.entorno.get_funcion(self.id)
        set_ret(sim.var_aug)
        set_entorno(self.entorno)

        for instr in self.instrucciones:
            resultado = instr.generar_C3D()
            augus += resultado[0]

        augus += "goto " + str(get_salida()) + ";\n\n"
        return [augus, ""]


    def generar_AST(self, dot, nombre):
        nombre_hijo = str(self.id) + "_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, self.id)

        if self.parametros is not None:
            nombre_temp = "parametros_" + new_nombre()
            dot.edge(nombre_hijo, nombre_temp)
            dot.node(nombre_temp, "Parametros")
            for param in self.parametros:
                nom_param = "param_" + new_nombre()
                dot.edge(nombre_temp, nom_param)
                dot.node(nom_param,str(param[0]))

        for inst in self.instrucciones:
            inst.generar_AST(dot, nombre_hijo)