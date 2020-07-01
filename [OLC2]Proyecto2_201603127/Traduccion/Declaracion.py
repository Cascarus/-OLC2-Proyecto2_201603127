from Traduccion.Abstracta import abst
from Traduccion.Variables import variables
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Valores import *
from Traduccion.Tipos import Tipo_dato

class Declaracion(abst):
    def __init__(self, tipo, lista, fila, columna):
        self.tipo = tipo
        self.lista = lista
        self.fila = fila
        self.columna = columna
        self.entorno = None

    def agregar_Tabla(self, actual, ambito_actual):
        for inst in self.lista:
            if isinstance(inst[0], variables):
                if not actual.exite_aqui(str(inst[0].id)):
                    sim = Simbolo(inst[0].id, self.tipo, "variable", ambito_actual, None, 0, new_temp(), self.fila, self.columna)
                    add_sim_report(sim)
                    actual.agregar_simbolo(sim)
                else:
                    print("la variable ya existe y no se puede vovler a declarar")
                    return False
        return True

    def verificar_tipo(self, ambito):
        for inst in self.lista:
            if isinstance(inst[0], variables):
                simbolos = ambito.get_simbol(inst[0].id)

                if inst[1] != None:#verifica que la variable tenga valor o no
                    resultado = inst[1].verificar_tipo(ambito)

                    if resultado == False:
                        return False

                    if simbolos.tipo == Tipo_dato.ENTERO:
                        if resultado == Tipo_dato.CADENA:
                            print("Error no se puede asignar un valor")
                            return False
                    elif simbolos.tipo == Tipo_dato.DECIMAL:
                        if resultado == Tipo_dato.CADENA:
                            print("Error no se puede asignar un valor")
                            return False
                    elif simbolos.tipo == Tipo_dato.CARACTER:
                        if resultado == Tipo_dato.CADENA:
                            print("Error no se puede asignar un valor")
                            return False
                    elif simbolos.tipo == Tipo_dato.CADENA:
                        if resultado != Tipo_dato.CADENA and resultado != Tipo_dato.CARACTER:
                            print("Error no se puede asignar un valor")
                            return False

        self.entorno = ambito


    def generar_C3D(self):
        augus = ""

        for instr in self.lista:
            if isinstance(instr[0], variables):
                simbolos = self.entorno.get_simbol(instr[0].id)

                if instr[1] != None:
                    temp = instr[1].generar_C3D(self.tipo)
                    augus += temp[0]
                    op = "" + str(simbolos.var_aug) + str(" = ") + str(temp[1]) + str(';\n')
                    augus += op

                else:
                    default_v = self.valor_defecto(self.tipo)
                    op = str(simbolos.var_aug) + str(" = ") + str(default_v) + ';\n'
                    augus += op

        return [augus, '']


    def valor_defecto(self, tipo):
        if tipo == Tipo_dato.ENTERO:
            return "0"
        elif tipo == Tipo_dato.DECIMAL:
            return "0.0"
        elif tipo == Tipo_dato.CADENA or tipo == Tipo_dato.CARACTER:
            return "\"\""
        else:
            return "array()"

    def verificar_combinacion_tipo(self,tipo_decla, tipo_dato):
        if tipo_decla == Tipo_dato.ENTERO:
            if tipo_dato == Tipo_dato.ENTERO:
                return True


    def generar_AST(self, dot, nombre):

        for inst in self.lista:
            nombre_hijo = "declaracion_" + str(new_nombre())
            dot.edge(nombre, nombre_hijo)
            if inst[1] != None:
                dot.node(nombre_hijo,"Declaracion \n =")
            else:
                dot.node(nombre_hijo, "Declaracion")

            if isinstance(inst[0], variables):
                inst[0].generar_AST(dot, nombre_hijo)
                if inst[1] != None:
                    inst[1].generar_AST(dot, nombre_hijo)