from Errores import *
from Valores_Variables import *
from funciones import *

from Analisis.Ascendente.ply import lex

reservadas = {
    'main': 'MAIN',
    'goto': 'GOTO',
    'unset': 'UNSET',
    'print': 'PRINT',
    'read': 'READ',
    'exit': "EXIT",
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'abs': 'ABS',
    'array': 'ARRAY',
    'if': 'IF',
    'xor': 'XOR'
}

tokens = [
             'PARENTA',
             'PARENTC',
             'CORCHEA',
             'CORCHEC',
             'PUNTOCOMA',
             'DOSPUNTOS',
             'MAS',
             'MENOS',
             'POR',
             'DIVICION',
             'IGUAL',
             'MODULO',
             'EXCLAMA',
             'AND1',
             'OR1',
             'NOT',
             'XOR2',
             'AND2',
             'OR2',
             'SHIFTI',
             'SHIFTD',
             'IGUALIGUAL',
             'DIFERENTE',
             'MAYORIGUAL',
             'MENORIGUAL',
             'MAYOR',
             'MENOR',
             'DECIMAL',
             'ENTERO',
             'CADENA',
             'ID',
             'TEMPORALES',
             'PARAMETROS',
             'VALORES_DEVUELTOS',
             'SIMULADO',
             'PILA',
             'PUNTERO_PILA'
         ] + list(reservadas.values())

t_PARENTA = r'\('
t_PARENTC = r'\)'
t_CORCHEA = r'\['
t_CORCHEC = r'\]'
t_PUNTOCOMA = r';'
t_DOSPUNTOS = r':'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVICION = r'/'
t_IGUAL = r'='
t_MODULO = r'%'
t_EXCLAMA = r'!'
t_AND1 = r'&&'
t_OR1 = r'\|\|'
t_NOT = r'~'
t_XOR2 = r'\^'
t_AND2 = r'&'
t_OR2 = r'\|'
t_SHIFTI = r'<<'
t_SHIFTD = r'>>'
t_IGUALIGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MAYOR = r'>'
t_MENOR = r'<'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Int value too large %d", t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'\".*?\" | \'.*?\''
    t.value = t.value[1:-1]
    t.value = t.value.replace("\\n", "\n")
    t.value = t.value.replace("\\t", "\t")
    t.value = t.value.replace("\\r", "\r")
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t


def t_TEMPORALES(t):
    r'\$t[0-9]+'
    t.type = reservadas.get(t.value.lower(), 'TEMPORALES')
    return t


def t_PARAMETROS(t):
    r'\$a[0-9]+'
    t.type = reservadas.get(t.value.lower(), 'PARAMETROS')
    return t


def t_VALORES_DEVUELTOS(t):
    r'\$v[0-9]+'
    t.type = reservadas.get(t.value.lower(), 'VALORES_DEVUELTOS')
    return t


def t_SIMULADO(t):
    r'\$ra'
    t.type = reservadas.get(t.value.lower(), 'SIMULADO')
    return t


def t_PILA(t):
    r'\$s[0-9]+'
    t.type = reservadas.get(t.value.lower(), 'PILA')
    return t


def t_PUNTERO_PILA(t):
    r'\$sp'
    t.type = reservadas.get(t.value.lower(), 'PUNTERO_PILA')
    return t


def t_COMENTARIO_S(t):
    r'\#(.*)\n'
    t.lexer.lineno += 1


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    #t.lexer.lineno += t.value.count("\n")
    t.lexer.lineno += len(t.value)

def t_error(t):
    Err = Error(t.value[0], "Lexico", "Caracter no reconocido", t.lineno, get_Column(t))
    Lista_errores.append(Err)
    print("Illegal character '%s'" % t.value[0])
    # print("trono lexicamente :\"v")
    t.lexer.skip(1)

# importacion de clases porpias para la funcionalidad
lexer = lex.lex()


def get_Column(token):
    lin_start = lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - lin_start) + 1


def p_init(t):
    '''inicio : instrucciones'''
    t[0] = t[1]


def p_instrucciones_lista(t):
    '''instrucciones : instrucciones instruccion'''
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t):
    '''instrucciones : instruccion'''
    t[0] = [t[1]]


def p_instruccion(t):
    '''instruccion : etiqueta_main
                   | etiqueta_ID
                   | asignacion
	               | inst_goto
    	           | inst_if
	               | inst_print
	               | inst_exit
                   | inst_unset'''
    # print("la etiqueta es.........",t[1])
    t[0] = t[1]


def p_etiqueta_main(t):
    '''etiqueta_main : MAIN DOSPUNTOS'''
    t[0] = Etiqueta(t[1], t.slice[1].lineno, get_Column(t.slice[1]))


def p_etiqueta_ID(t):
    '''etiqueta_ID : ID DOSPUNTOS'''
    t[0] = Etiqueta(t[1], t.slice[1].lineno, get_Column(t.slice[1]))


def p_asignacion(t):
    '''asignacion : variables IGUAL operaciones PUNTOCOMA'''
    t[0] = Asignacion(t[1], t[3], t[1].fila, t[1].columna)

def p_asignacion_array(t):
    '''asignacion : variables_array IGUAL operaciones PUNTOCOMA'''
    t[0] = Asignacion(t[1], t[3], t[1].fila, t[1].columna)

def p_goto(t):
    '''inst_goto : GOTO ID PUNTOCOMA'''
    t[0] = Goto(t[2], t.slice[1].lineno, get_Column(t.slice[1]))


def p_if(t):
    '''inst_if : IF PARENTA operaciones PARENTC GOTO ID PUNTOCOMA'''
    t[0] = If_Goto(t[3], t[6], t.slice[1].lineno, get_Column(t.slice[1]))


def p_print(t):
    '''inst_print : PRINT PARENTA variables PARENTC PUNTOCOMA
                  | PRINT PARENTA val PARENTC PUNTOCOMA'''
    t[0] = Imprimir(t[3], t.slice[1].lineno, get_Column(t.slice[1]))


def p_unset(t):
    '''inst_unset : UNSET PARENTA variables PARENTC PUNTOCOMA'''
    t[0] = Unset(t[3], t.slice[1].lineno, get_Column(t.slice[1]))

def p_exit(t):
    '''inst_exit : EXIT PUNTOCOMA'''
    t[0] = Exit(t.slice[1].lineno, get_Column(t.slice[1]))


def p_operaciones(t):
    '''operaciones : val MAS val
                     | val MENOS val
                     | val POR val
                     | val DIVICION val
                     | val MODULO val
                     | val AND1 val
                     | val OR1 val
                     | val XOR val
                     | val AND2 val
                     | val OR2 val
                     | val XOR2 val
                     | val SHIFTI val
                     | val SHIFTD val
                     | val IGUALIGUAL val
                     | val DIFERENTE val
                     | val MAYORIGUAL val
                     | val MENORIGUAL val
                     | val MAYOR val
                     | val MENOR val'''
    if t[2] == '+':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Aritmetica.SUMA, t[1].fila, t[1].columna)
    elif t[2] == '-':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Aritmetica.RESTA, t[1].fila, t[1].columna)
    elif t[2] == '*':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Aritmetica.POR, t[1].fila, t[1].columna)
    elif t[2] == '/':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Aritmetica.DIVICION, t[1].fila, t[1].columna)
    elif t[2] == '%':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Aritmetica.RESIDUIO, t[1].fila, t[1].columna)
    elif t[2] == '&&':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.AND, t[1].fila, t[1].columna)
    elif t[2] == '||':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.OR, t[1].fila, t[1].columna)
    elif str(t[2]).lower() == 'xor':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.XOR, t[1].fila, t[1].columna)
    elif t[2] == '&':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Bit.AND, t[1].fila, t[1].columna)
    elif t[2] == '|':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Bit.OR, t[1].fila, t[1].columna)
    elif t[2] == '^':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Bit.XOR, t[1].fila, t[1].columna)
    elif t[2] == '<<':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Bit.SHIFTI, t[1].fila, t[1].columna)
    elif t[2] == '>>':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Bit.SHIFTD, t[1].fila, t[1].columna)
    elif t[2] == '==':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.IGUAL_IGUAL, t[1].fila, t[1].columna)
    elif t[2] == '!=':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.DIFERENTE, t[1].fila, t[1].columna)
    elif t[2] == '>=':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.MAYOR_IGUAL, t[1].fila, t[1].columna)
    elif t[2] == '<=':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.MENOR_IGUAL, t[1].fila, t[1].columna)
    elif t[2] == '>':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.MAYOR, t[1].fila, t[1].columna)
    elif t[2] == '<':
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.MENOR, t[1].fila, t[1].columna)


def p_operaciones_unaria(t):
    '''operaciones : MENOS val
                   | EXCLAMA val
                   | NOT val
                   | ABS PARENTA val PARENTC
                   | READ PARENTA PARENTC
                   | ARRAY PARENTA PARENTC'''

    if t[1] == '-':
        t[0] = Numerico_Negativo(t[2], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1] == '!':
        t[0] = Bool_Negado(t[2], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1] == '~':
        t[0] = Bit_Negado(t[2], t.slice[1].lineno, get_Column(t.slice[1]))
    elif str(t[1]).lower() == 'abs':
        t[0] = Numerico_Absoluto(t[3], t.slice[1].lineno, get_Column(t.slice[1]))
    elif str(t[1]).lower() == 'read':
        print("llego al read")
        t[0] = Read(t.slice[1].lineno, get_Column(t.slice[1]))
    elif str(t[1]).lower() == 'array':
        t[0] = Array(t.slice[1].lineno, get_Column(t.slice[1]))


def p_op_val(t):
    '''operaciones : val'''
    t[0] = t[1]


def p_val_conversiones(t):
    '''val : conversiones'''
    t[0] = t[1]


def p_val_numerico_entero(t):
    '''val : ENTERO'''
    t[0] = Numerico_Entero(t[1], Tipo_Dato.ENTERO, t.slice[1].lineno, get_Column(t.slice[1]))


def p_val_numerico_decimal(t):
    '''val : DECIMAL'''
    t[0] = Numerico_Decimal(t[1], Tipo_Dato.DECIMAL, t.slice[1].lineno, get_Column(t.slice[1]))
    # print(t[0])


def p_val_cadena(t):
    '''val : CADENA'''
    t[0] = String_Val(t[1], Tipo_Dato.CADENA, t.slice[1].lineno, get_Column(t.slice[1]))


def p_val_variables(t):
    '''val : variables'''
    t[0] = t[1]


def p_val_variables_array(t):
    '''val : variables_array'''
    t[0] = t[1]


def p_val_varibles(t):
    '''variables : TEMPORALES
                 | PARAMETROS
                 | VALORES_DEVUELTOS
                 | SIMULADO
                 | PILA
                 | PUNTERO_PILA'''

    if t[1][1] == 't':
        t[0] = Var_Temporales(Tipo_Variable.TEMPORALES, t[1], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 'a':
        t[0] = Var_Parametros(Tipo_Variable.PARAMETROS, t[1], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 'v':
        t[0] = Var_Devueltos(Tipo_Variable.DEVUELTOS, t[1], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 'r':
        t[0] = Var_Simulado(Tipo_Variable.SIMULADOR, t[1], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 's':
        if t[1] == '$sp':
            t[0] = Var_Puntero_Pila(Tipo_Variable.PUNTERO_PILA, t[1], t.slice[1].lineno, get_Column(t.slice[1]))
        else:
            t[0] = Var_Pila(Tipo_Variable.PILA, t[1], t.slice[1].lineno, get_Column(t.slice[1]))
    #print(t[0])


def p_v_array(t):
    '''variables_array : TEMPORALES indices
                       | PARAMETROS indices
                       | VALORES_DEVUELTOS indices
                       | SIMULADO indices
                       | PILA indices
                       | PUNTERO_PILA indices'''
    if t[1][1] == 't':
        t[0] = Var_Array(Tipo_Variable.TEMPORALES, t[1], t[2], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 'a':
        t[0] = Var_Array(Tipo_Variable.PARAMETROS, t[1], t[2], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 'v':
        t[0] = Var_Array(Tipo_Variable.DEVUELTOS, t[1], t[2], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 'r':
        t[0] = Var_Array(Tipo_Variable.SIMULADOR, t[1], t[2], t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1][1] == 's':
        if t[1] == '$sp':
            t[0] = Var_Array(Tipo_Variable.PUNTERO_PILA, t[1], t[2], t.slice[1].lineno, get_Column(t.slice[1]))
        else:
            t[0] = Var_Array(Tipo_Variable.PILA, t[1], t[2], t.slice[1].lineno, get_Column(t.slice[1]))

def p_indices_incices(t):
    '''indices : indices indice'''
    t[1].append(t[2])
    t[0] = t[1]

def p_indices_indice(t):
    '''indices : indice'''
    t[0] = [t[1]]
def p_indice(t):
    '''indice : CORCHEA val CORCHEC'''
    t[0] = t[2]

def p_conversiones(t):
    '''conversiones : PARENTA INT PARENTC val
                    | PARENTA FLOAT PARENTC val
                    | PARENTA CHAR PARENTC val'''
    if str(t[2]).lower() == 'int':
        t[0] = Conversion_Int(t[4], t.slice[1].lineno, get_Column(t.slice[1]))
    elif str(t[2]).lower() == 'float':
        t[0] = Conversion_Float(t[4], t.slice[1].lineno, get_Column(t.slice[1]))
    elif str(t[2]).lower() == 'char':
        t[0] = Conversion_Char(t[4], t.slice[1].lineno, get_Column(t.slice[1]))


def p_error(t):

    if not t:
        Err = Error("EOF", "Sintactico", "Token no esperado", 0, 0)
        Lista_errores.append(Err)
        print("final del documento")
        return
    Err = Error(t.value, "Sintactico", "Token no esperado", t.lineno, get_Column(t))
    Lista_errores.append(Err)
    print("ERROR SINTACTICO ", t.value)

    while True:
        tok = parser.token()
        if not tok or tok.type == "PUNTOCOMA":
            break
    parser.errok()
    return tok

from Analisis.Ascendente.ply import yacc as yacc
parser = yacc.yacc()

def parse(texto):
    lexer.lineno = 1
    return parser.parse(texto)
