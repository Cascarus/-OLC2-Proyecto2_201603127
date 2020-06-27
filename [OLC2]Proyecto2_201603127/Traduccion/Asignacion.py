from Traduccion.Abstracta import abst
from Traduccion.Variables import variables
from Traduccion.Tipos import Tipo_dato
from Traduccion.Tipos import tipo_asign

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
                    temp = instr[1].generar_C3D(simbolos.tipo)
                    augus += temp[0]
                    op = "" + str(simbolos.var_aug) + str(" = ") + str(temp[1]) + ";" + str('\n')
                    augus += op

                else:
                    default_v = self.valor_defecto(self.tipo)
                    op = str(simbolos.var_aug) + str("=") + str(default_v) + ";" +'\n'
                    augus += op

        return [augus, '']