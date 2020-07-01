from enum import Enum
from Valores_Variables import Tipo_Dato

class TIPO_DATO(Enum):
    ENTERO = 1
    DECIMAL = 2
    CADENA = 3
    CARACTER = 4

class Simbolo():
    def __init__(self, id, tipo, valor, dimension, declarada, referencias):
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.dimension = dimension
        self. declarada = declarada
        self.referencias = referencias

class Tabla_Simbolos():
    def __init__(self, simbolos = {}):
        self.simbolos = simbolos

    def add_simbolo(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    def get_simbolo(self, id):
        if not id in self.simbolos:
            print("no existe el simbolo")
            return Simbolo(None,None,None,None,None,None)
        sim = self.simbolos[id]
        if sim.tipo == Tipo_Dato.ARRAY:
            ''''''
        return self.simbolos[id]
        #imprimir error

    def update_simbolo(self, simbolo):
        if simbolo.id in self.simbolos:
            self.simbolos[simbolo.id] = simbolo
        
            #imprimir error 

    def existe_simbolo(self, simbolo):
        if simbolo.id in self.simbolos:
            return True
        return False

    def existe_id(self, id):
        if id in self.simbolos:
            return True
        return False

    def clear(self):
        self.simbolos.clear()

    def get_all(self):
        return self.simbolos

    def delete_simbolo(self, id):
        if id in self.simbolos:
            texto = self.simbolos.pop(id)
            return True
        return False


    def print_tabla(self):
        for simbolo in self.simbolos:
            temp = self.get_simbolo(simbolo)
            print("simbolo: ", str(temp.id), " tipo: ", str(temp.tipo), " Valor: ", str(temp.valor))