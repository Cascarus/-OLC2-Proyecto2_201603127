from Traduccion.Abstracta import abst
from Traduccion.Variables import variables
from Traduccion.Tipos import Tipo_dato
from Traduccion.Tipos import tipo_asign
from Traduccion.Valores import *
from Traduccion.Var_Array import var_arry
from Errores import *

class Asignacion(abst):
    def __init__(self,lista, fila, columna):
        self.lista = lista
        self.fila = fila
        self.columna = columna
        self.entorno = None


    def verificar_tipo(self, ambito):
        for inst in self.lista:
            if isinstance(inst[0], variables):
                simbolos = ambito.get_simbol(inst[0].id)
                resultado = inst[1].verificar_tipo(ambito)
                if resultado == False or simbolos == False:
                    return False

                if simbolos.tipo == Tipo_dato.ENTERO:
                    if resultado == Tipo_dato.CADENA:
                        print("Error no se puede asignar un valor")
                        Err = Error("Asignacion", "Semantico", "No se puede asignar un valor string a uno de tipo entero", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False
                elif simbolos.tipo == Tipo_dato.DECIMAL:
                    if resultado == Tipo_dato.CADENA:
                        print("Error no se puede asignar un valor")
                        Err = Error("Asignacion", "Semantico",
                                    "No se puede asignar un valor string a uno de tipo decimal", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False
                elif simbolos.tipo == Tipo_dato.CARACTER:
                    if resultado == Tipo_dato.CADENA:
                        print("Error no se puede asignar un valor")
                        Err = Error("Asignacion", "Semantico",
                                    "No se puede asignar un valor string a uno de tipo caracter", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False
                elif simbolos.tipo == Tipo_dato.CADENA:
                    if resultado != Tipo_dato.CADENA and resultado != Tipo_dato.CARACTER:
                        print("Error no se puede asignar un valor")
                        Err = Error("Asignacion", "Semantico",
                                    "Solo se puede asignar un valor string o caracter a uno de tipo string", self.fila, self.columna)
                        Lista_errores.append(Err)
                        return False
            elif isinstance(inst[0], var_arry):
                simbolos = ambito.get_simbol(inst[0].id)

                for cont in inst[0].dimensiones:
                    resultado = cont.verificar_tipo(ambito)

                    if resultado == False or resultado != Tipo_dato.ENTERO:
                        return False

                if inst[1] is not None:
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
                                        "Solo se puede asignar un valor string o caracter a uno de tipo string",
                                        self.fila,
                                        self.columna)
                            Lista_errores.append(Err)
                            return False

        self.entorno = ambito

    def generar_C3D(self):
        augus = ""

        for instr in self.lista:
            if isinstance(instr[0], variables):
                simbolos = self.entorno.get_simbol(instr[0].id)

                if instr[1] != None:
                    temp = instr[1].generar_C3D(simbolos.tipo)
                    augus += temp[0]


                    if instr[2] == tipo_asign.IGUAL:
                        augus += str(simbolos.var_aug) + str(" = ") + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.MASIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " + " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.MENOSIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " - " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.PORIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " * " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.DIVIIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " / " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.RESIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " % " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.IZQIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " << " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.DERIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " >> " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.ANDIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " & " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.ORIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " | " + str(temp[1]) + ";\n"
                    elif instr[2] == tipo_asign.XORIGUAL:
                        augus += str(simbolos.var_aug) + " = " + str(simbolos.var_aug) + " ^ " + str(temp[1]) + ";\n"

            else:
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
                            augus += str(temp) + " = " + str(temp) + " + 1;\n"
                            ultima_temp = temp

                        else:
                            augus += str(temp) + " = " + str(resultado[1]) + " + 1;\n"
                            augus += str(temp) + " = " + str(temp) + " * " + str(ultima_temp) + ";\n"
                            ultima_temp = temp

                    else:
                        if conta == 0:
                            augus += str(resultado[1]) + " = " + str(resultado[1]) + " + 1;\n"
                            ultima_temp = str(resultado[1])
                        else:
                            augus += str(resultado[1]) + " = " + str(resultado[1]) + " + 1;\n"
                            augus += str(resultado[1]) + " = " + str(resultado[1]) + " * " + ultima_temp + ";\n"
                            ultima_temp = str(resultado[1])
                    conta += 1

                res = instr[1].generar_C3D(simbolos.tipo)
                augus += res[0]
                augus += ultima_temp + " = " + ultima_temp + " - 1;\n"
                augus += str(simbolos.var_aug) + "[" + str(ultima_temp) + "] = " + str(res[1]) + ";\n"
                #augus += str(simbolos.var_aug) + "[" + str(ultima_temp) + "] = "
                #augus += str(res[1]) + ";\n"

        return [augus, '']

    def generar_AST(self, dot, nombre):
        for instr in self.lista:
            nombre_hijo = "asignacion_" + str(new_nombre())
            dot.edge(nombre, nombre_hijo)

            if instr[2] == tipo_asign.IGUAL:
                dot.node(nombre_hijo, "Asignacion \n =")
            elif instr[2] == tipo_asign.MASIGUAL:
                dot.node(nombre_hijo, "Asignacion \n +=")
            elif instr[2] == tipo_asign.MENOSIGUAL:
                dot.node(nombre_hijo, "Asignacion \n -=")
            elif instr[2] == tipo_asign.PORIGUAL:
                dot.node(nombre_hijo, "Asignacion \n *=")
            elif instr[2] == tipo_asign.DIVIIGUAL:
                dot.node(nombre_hijo, "Asignacion \n /=")
            elif instr[2] == tipo_asign.RESIGUAL:
                dot.node(nombre_hijo, "Asignacion \n %=")
            elif instr[2] == tipo_asign.IZQIGUAL:
                dot.node(nombre_hijo, "Asignacion \n <<=")
            elif instr[2] == tipo_asign.DERIGUAL:
                dot.node(nombre_hijo, "Asignacion \n >>=")
            elif instr[2] == tipo_asign.ANDIGUAL:
                dot.node(nombre_hijo, "Asignacion \n &=")
            elif instr[2] == tipo_asign.ORIGUAL:
                dot.node(nombre_hijo, "Asignacion \n |=")
            elif instr[2] == tipo_asign.XORIGUAL:
                dot.node(nombre_hijo, "Asignacion \n ^=")
            

            if isinstance(instr[0], variables):
                instr[0].generar_AST(dot, nombre_hijo)
                instr[1].generar_AST(dot, nombre_hijo)
