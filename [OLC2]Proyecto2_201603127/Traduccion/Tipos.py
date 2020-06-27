from enum import Enum

class Tipo_dato(Enum):
    ENTERO = 1
    DECIMAL = 2
    CADENA = 3
    CARACTER = 4

class Tipo_operacion(Enum):
    SUMA = 1
    RESTA = 2
    POR = 3
    DIVICION = 4
    RESIDUIO = 5

class Operacion_logica(Enum):
    AND = 1
    OR = 2
    XOR = 3
    IGUAL_IGUAL = 4
    DIFERENTE = 5
    MAYOR_IGUAL = 6
    MENOR_IGUAL = 7
    MAYOR = 8
    MENOR = 9

class Operacion_bit(Enum):
    AND = 1
    OR = 2
    XOR = 3
    SHIFTI = 4
    SHIFTD = 5

class tipo_decla(Enum):
    INT = 'ENTERO'
    DOUBLE = 'DOUBLE'
    FLOAT = 'FLOAT'
    CHAR = 'CARACTER'

class tipo_asign(Enum):
    IGUAL = 1
    MASIGUAL = 2
    MENOSIGUAL = 3
    PORIGUAL = 4
    DIVIIGUAL = 5
    RESIGUAL = 6
    IZQIGUAL = 7
    DERIGUAL = 8
    ANDIGUAL = 9
    ORIGUAL = 10
    XORIGUAL = 11