from Traduccion.Abstracta import abst
from Traduccion.Variables import variables
from Traduccion.Tabla_Sim_C import Simbolo
from Traduccion.Valores import *
from Traduccion.Tipos import Tipo_dato
from Traduccion.Var_Array import var_arry
from Errores import *

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
                    if inst[0].cadena:
                        sim.tipo = Tipo_dato.CADENA
                        self.tipo = Tipo_dato.CADENA
                    add_sim_report(sim)
                    actual.agregar_simbolo(sim)
                else:
                    print("la variable ya existe y no se puede vovler a declarar")
                    Err = Error("Declaracion", "Semantico", "La variable ya existe y no se puede volver a declarar",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False
            elif isinstance(inst[0], var_arry):
                if not actual.exite_aqui(str(inst[0].id)):
                    sim = Simbolo(inst[0].id, self.tipo, "Arreglo", ambito_actual, None, str(len(inst[0].dimensiones)), new_temp(), self.fila, self.columna)
                    add_sim_report(sim)
                    actual.agregar_simbolo(sim)
                else:
                    print("la variable ya existe y no se puede vovler a declarar")
                    Err = Error("Declaracion", "Semantico", "La variable ya existe y no se puede volver a declarar",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
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
                            Err = Error("Declaracion", "Semantico",
                                        "No se puede asignar un valor string a uno de tipo entero", self.fila,
                                        self.columna)
                            Lista_errores.append(Err)
                            return False
                    elif simbolos.tipo == Tipo_dato.DECIMAL:
                        if resultado == Tipo_dato.CADENA:
                            print("Error no se puede asignar un valor")
                            Err = Error("Declaracion", "Semantico",
                                        "No se puede asignar un valor string a uno de tipo decimal", self.fila,
                                        self.columna)
                            Lista_errores.append(Err)
                            return False
                    elif simbolos.tipo == Tipo_dato.CARACTER:
                        if resultado == Tipo_dato.CADENA:
                            print("Error no se puede asignar un valor")
                            Err = Error("Declaracion", "Semantico",
                                        "No se puede asignar un valor string a uno de tipo caracter", self.fila,
                                        self.columna)
                            Lista_errores.append(Err)
                            return False
                    elif simbolos.tipo == Tipo_dato.CADENA:
                        if resultado != Tipo_dato.CADENA and resultado != Tipo_dato.CARACTER:
                            print("Error no se puede asignar un valor")
                            Err = Error("Declaracion", "Semantico",
                                        "Solo se puede asignar un valor string o caracter a uno de tipo string", self.fila,
                                        self.columna)
                            Lista_errores.append(Err)
                            return False

            elif isinstance(inst[0], var_arry):
                simbolos = ambito.get_simbol(inst[0].id)

                for cont in inst[0].dimensiones:
                    resultado = cont.verificar_tipo(ambito)

                    if resultado == False or resultado != Tipo_dato.ENTERO:
                        return False

                if inst[1] is not None:
                    for cont in inst[1]:
                        resultado = cont.verificar_tipo(ambito)
                        if resultado == False:
                            return False

                        if simbolos.tipo == Tipo_dato.ENTERO:
                            if resultado == Tipo_dato.CADENA:
                                print("Error no se puede asignar un valor")
                                Err = Error("Declaracion", "Semantico",
                                            "No se puede asignar un valor string a uno de tipo entero", self.fila,
                                            self.columna)
                                Lista_errores.append(Err)
                                return False
                        elif simbolos.tipo == Tipo_dato.DECIMAL:
                            if resultado == Tipo_dato.CADENA:
                                print("Error no se puede asignar un valor")
                                Err = Error("Declaracion", "Semantico",
                                            "No se puede asignar un valor string a uno de tipo decimal", self.fila,
                                            self.columna)
                                Lista_errores.append(Err)
                                return False
                        elif simbolos.tipo == Tipo_dato.CARACTER:
                            if resultado == Tipo_dato.CADENA:
                                print("Error no se puede asignar un valor")
                                Err = Error("Declaracion", "Semantico",
                                            "No se puede asignar un valor string a uno de tipo caracter", self.fila,
                                            self.columna)
                                Lista_errores.append(Err)
                                return False
                        elif simbolos.tipo == Tipo_dato.CADENA:
                            if resultado != Tipo_dato.CADENA and resultado != Tipo_dato.CARACTER:
                                print("Error no se puede asignar un valor")
                                Err = Error("Declaracion", "Semantico",
                                            "Solo se puede asignar un valor string o caracter a uno de tipo string",
                                            self.fila,
                                            self.columna)
                                Lista_errores.append(Err)
                                return False
        self.entorno = ambito
        return True


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

            elif isinstance(instr[0], var_arry):
                simbolos = self.entorno.get_simbol(instr[0].id)
                ultima_temp = ""
                conta = 0

                for cont in instr[0].dimensiones:
                    resultado = cont.generar_C3D()
                    augus += resultado[0]

                    if resultado[0] == "":
                        temp = new_temp()
                        if conta == 0:
                            augus += str(temp) + " = " + str(resultado[1]) + ";\n"
                            ultima_temp = temp

                        else:
                            augus += str(temp) + " = " + str(resultado[1]) + " * " + str(ultima_temp) + ";\n"
                            ultima_temp = temp

                    else:
                        if conta == 0:
                            ultima_temp = str(resultado[1])
                        else:
                            augus += str(resultado[1]) + " = " + str(resultado[1]) + " * " + ultima_temp + ";\n"
                            ultima_temp = str(resultado[1])
                    conta += 1

                if instr[1] is not None:
                    temp = new_temp()
                    etiV = new_etiqueta()
                    etiF = new_etiqueta()

                    augus += temp + " = " + str(len(instr[1])) + ";\n"
                    augus += str(simbolos.var_aug) + " = array();\n"
                    augus += "if ({} == {}) goto {};\n".format(ultima_temp, temp , etiV)
                    augus += "print(\"ERROR: la cantidad de elementos no es igual a la declarada\\n\");\n"
                    augus += "unset(" + str(simbolos.var_aug) + ");\n"
                    augus += "goto " + etiF + ";\n"
                    augus += "\n" + str(etiV) + ":\n"
                    cont = 0

                    for op in instr[1]:
                        resultado = op.generar_C3D(self.tipo)
                        augus += resultado[0]
                        augus += str(simbolos.var_aug) + "[" + str(cont) + "] = " + str(resultado[1]) + ";\n"
                        cont += 1

                    augus += "\n" + str(etiF) + ":\n"

                else:
                    eti1 = new_etiqueta()
                    eti2 = new_etiqueta()
                    temp = new_temp()

                    augus += str(ultima_temp) + " = " + str(ultima_temp) + ";\n"

                    if self.tipo == Tipo_dato.ENTERO:
                        augus += "{4} = array();\n{0} = 0;\n{1}:\nif({0} >= {2}) goto {3};\n{4}[{0}] = 0;\n{0} = {0} + 1;\ngoto {1};\n{3}:\n".format(
                            temp, eti1, ultima_temp, eti2, str(simbolos.var_aug))
                    elif self.tipo == Tipo_dato.DECIMAL:
                        augus += "{4} = array();\n{0} = 0;\n{1}:\nif({0} >= {2}) goto {3};\n{4}[{0}] = 0.0;\n{0} = {0} + 1;\ngoto {1};\n{3}:\n".format(
                            temp, eti1, ultima_temp, eti2, str(simbolos.var_aug))
                    elif self.tipo == Tipo_dato.CARACTER:
                        augus += "{4} = array();\n{0} = 0;\n{1}:\nif({0} >= {2}) goto {3};\n{4}[{0}] = '';\n{0} = {0} + 1;\ngoto {1};\n{3}:\n".format(
                            temp, eti1, ultima_temp, eti2, str(simbolos.var_aug))


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
            else:
                nombre_id = "id_dim_" + str(new_nombre())
                dot.edge(nombre_hijo, nombre_id)
                x = ""
                y = ""
                if len(inst[0].dimensiones) == 1:
                    x = str(inst[0].dimensiones[0].valor)
                    temp = str(inst[0].id) + "[" + x + "]"
                    dot.node(nombre_id, str(temp))
                elif len(inst[0].dimensiones) == 2:
                    x = str(inst[0].dimensiones[0].valor)
                    y = str(inst[0].dimensiones[1].valor)
                    temp = str(inst[0].id) + "[" + x + "][" + y + "]"
                    dot.node(nombre_id, str(temp))

                if inst[1] is not None:
                    nombre_temp = "val_" + str(new_nombre())
                    dot.edge(nombre_hijo, nombre_temp)
                    val = []
                    for i in inst[1]:
                        val.append(i.valor)
                    dot.node(nombre_temp, str(val))
