from Traduccion.Abstracta import abst
from Traduccion.Valores import new_nombre
from Traduccion.Tipos import Tipo_dato
from Errores import *

class Print(abst):

    def __init__(self, contenido, fila, columna):
        self.contenido = contenido[1:]
        self.fila = fila
        self.columna = columna
        self.cadena = contenido[0]

    def verificar_tipo(self, ambito):
        self.tipo = []
        if len(self.contenido) != 0:
            for instr in self.contenido:
                resultado = instr.verificar_tipo(ambito)

                if resultado == False:
                    Err = Error("Printf", "Semantico", "Algo ha fallado en el contenido ",
                                self.fila, self.columna)
                    Lista_errores.append(Err)
                    return False
                self.tipo.append(resultado)


    def generar_C3D(self):
        augus = ""
        conta = 0
        bandera = False

        if len(self.contenido) == 0:
            contenido = self.cadena.generar_C3D("print")
            augus += contenido[0]
            augus += "print(" + str(contenido[1]) + ");\n"

        else:
            temp = self.cadena.valor
            cadena = ""
            for char in temp:
                if bandera:
                    conta += 1
                    bandera = False
                    continue
                if char == "%":
                    augus += "print(\"" + cadena + "\");\n"
                    cadena = ""
                    if len(self.contenido) > 0:
                        if conta + 1 < len(temp):
                            bandera = True
                            if temp[conta+1] == "d" or temp[conta+1] == "i":
                                tipo = self.tipo.pop(0)
                                if tipo == Tipo_dato.ENTERO:
                                    resultado = self.contenido.pop(0).generar_C3D()
                                    augus += resultado[0]
                                    augus += "print(" + str(resultado[1]) + ");\n"
                                else:
                                    if tipo != Tipo_dato.CADENA:
                                        resultado = self.contenido.pop(0).generar_C3D(Tipo_dato.ENTERO)
                                        augus += resultado[0]
                                        augus += "print(" + str(resultado[1]) + ");\n"
                                    else:
                                        print("ERROR: Se esperaba un dato de tipo Decimal en el print")
                                        break

                            elif temp[conta+1] == "f":
                                tipo = self.tipo.pop(0)
                                if tipo == Tipo_dato.DECIMAL:
                                    resultado = self.contenido.pop(0).generar_C3D()
                                    augus += resultado[0]
                                    augus += "print(" + str(resultado[1]) + ");\n"
                                else:
                                    if tipo != Tipo_dato.CADENA:
                                        resultado = self.contenido.pop(0).generar_C3D(Tipo_dato.DECIMAL)
                                        augus += resultado[0]
                                        augus += "print(" + str(resultado[1]) + ");\n"
                                    else:
                                        print("ERROR: Se esperaba un dato de tipo Decimal en el print")
                                        break


                            elif temp[conta+1] == "s":
                                tipo = self.tipo.pop(0)
                                if tipo == Tipo_dato.CADENA or tipo == Tipo_dato.CARACTER:
                                    resultado = self.contenido.pop(0).generar_C3D("print")
                                    augus += resultado[0]
                                    augus += "print(" + str(resultado[1]) + ");\n"
                                else:
                                    print("ERROR: Se esperaba un dato de tipo Decimal en el print")
                                    break

                            elif temp[conta+1] == "c":
                                tipo = self.tipo.pop(0)
                                if tipo == Tipo_dato.CARACTER:
                                    resultado = self.contenido.pop(0).generar_C3D(Tipo_dato.CARACTER)
                                    augus += resultado[0]
                                    augus += "print(" + str(resultado[1]) + ");\n"
                                else:
                                    if tipo != Tipo_dato.CADENA:
                                        resultado = self.contenido.pop(0).generar_C3D(Tipo_dato.CARACTER)
                                        augus += resultado[0]
                                        augus += "print(" + str(resultado[1]) + ");\n"
                                    else:
                                        print("ERROR: Se esperaba un dato de tipo Decimal en el print")
                                        break
                            else:
                                print("ERROR: Esto no deberia ocurrir")
                        else:
                            print("ERROR: PRINT INCOMPLETO")
                            break
                    else:
                        print("ERROR: LA CANTIDAD DE PARAMETROS ES MENOR A LA CANTIDAD DE MARCAS")
                        break
                else:
                    cadena += char
                if conta == len(temp)-1 and len(self.contenido) > 0:
                    print("ERROR: LA CANTIADAD DE PARAMETROS ES MAYOR A LA CANTIDAD DE MARCAS")
                    break
                conta += 1
            augus += "print(\"" + cadena + "\");\n"

        return[augus, ""]

    def generar_AST(self, dot, nombre):
        nombre_hijo = "print_" + new_nombre()
        dot.edge(nombre, nombre_hijo)
        dot.node(nombre_hijo, "Printf")

        self.cadena.generar_AST(dot, nombre_hijo)

        for instr in self.contenido:
            instr.generar_AST(dot, nombre_hijo)