from enum import Enum


class Tipo_Dato(Enum):
    ENTERO = 1
    DECIMAL = 2
    CADENA = 3
    ARRAY = 4


class Operacion_Aritmetica(Enum):
    SUMA = 1
    RESTA = 2
    POR = 3
    DIVICION = 4
    RESIDUIO = 5


class Operacion_Logica(Enum):
    AND = 1
    OR = 2
    XOR = 3
    IGUAL_IGUAL = 4
    DIFERENTE = 5
    MAYOR_IGUAL = 6
    MENOR_IGUAL = 7
    MAYOR = 8
    MENOR = 9

class Operacion_Bit(Enum):
    AND = 1
    OR = 2
    XOR = 3
    SHIFTI = 4
    SHIFTD = 5


class Tipo_Variable(Enum):
    TEMPORALES = 1
    PARAMETROS = 2
    DEVUELTOS = 3
    PILA = 4
    SIMULADOR = 5
    PUNTERO_PILA = 6

class Operacion_Convercion(Enum):
    TO_INT = 1
    TO_STR = 2
    TO_CHAR = 3


class Val_Numerico:
    '''print("clase val_num")'''

class Operacion_Binaria():
    def __init__(self, val1, val2, operacion, fila, columna):
        self.val1 = val1
        self.val2 = val2
        self.operacion = operacion
        self.fila = fila
        self.columna = columna

class Numerico_Negativo(Val_Numerico):
    def __init__(self, val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

class Numerico_Absoluto(Val_Numerico):
    def __init__(self, val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

#PRIMITIVOS
class Numerico_Entero(Val_Numerico):
    def __init__(self, val, tipo, fila, columna):
        self.val = val
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Numerico_Decimal(Val_Numerico):
    def __init__(self, val, tipo, fila, columna):
        self.val = val
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Val_String:
    '''print("clase string y cadenas")'''

class String_Val(Val_String):
    def __init__(self, val, tipo, fila, columna):
        self.val = val
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

#CONVERSIONES
class Val_Conversion:
    '''print("clase val_conversion")'''

class Conversion_Int(Val_Conversion):
    def __init__(self, val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

class Conversion_Float(Val_Conversion):
    def __init__(self, val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

class Conversion_Char(Val_Conversion):
    def __init__(self, val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

#LOGICAS Y BIT A BIT
class Val_Bool():
    def __init__(self, val1, val2, operacion, fila, columna):
        self.val1 = val1
        self.val2 = val2
        self.operacion = operacion
        self.fila = fila
        self.columna = columna

class Bool_Negado():
    def __init__(self, val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

class Bit_Negado():
    def __init__(self, val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

#EMPIEZAN LAS VARIABLES
class Variables():
    ''''''

class Var_Temporales(Variables):
    def __init__(self, tipo, id, fila, columna):
        self.id = id
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Var_Parametros(Variables):
    def __init__(self, tipo, id, fila, columna):
        self.id = id
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Var_Devueltos(Variables):
    def __init__(self, tipo, id, fila, columna):
        self.id = id
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Var_Simulado(Variables):
    def __init__(self, tipo, id, fila, columna):
        self.id = id
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Var_Pila(Variables):
    def __init__(self, tipo, id, fila, columna):
        self.id = id
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Var_Puntero_Pila(Variables):
    def __init__(self, tipo, id, fila, columna):
        self.id = id
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

class Etiqueta():
    def __init__(self, id, fila, columna):
        self.id = id
        self.fila = fila
        self.columna = columna

class Var_Array(Variables):
    def __init__(self, tipo, id, lista, fila, columna):
        self.id = id
        self.lista = lista
        self.tipo = tipo
        self.fila = fila
        self.columna = columna