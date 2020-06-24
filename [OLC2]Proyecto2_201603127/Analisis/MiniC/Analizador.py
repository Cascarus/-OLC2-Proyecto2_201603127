from Errores import *
from Valores_Variables import *
from funciones import *

from Analisis.Ascendente.ply import lex

reservadas = {
    'main': 'MAIN',
    'break': 'BREAK',
    'case': 'CASE',
#    'const': 'CONST',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'do': 'DO',
    'else': 'ELSE',
#    'enum': 'ENUM',
    'for': 'FOR',
#    'goto': 'GOTO',
    'if': 'IF',
    'int': 'INT',
    'return': 'RETURN',
#    'sizeof': 'SIZEOF',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'void': 'VOID',
    'while': 'WHILE',
    'printf': 'PRINTF',
    'scanf': 'SCANF',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'float': 'FLOAT'
}

tokens = [
             'PARENTA',
             'PARENTC',
             'CORCHEA',
             'CORCHEC',
             'LLAVEA',
             'LLAVEC',
             'PUNTOCOMA',
             'DOSPUNTOS',
             'COMA',
#             'PUNTO',
             'TERNARIO',
             'MAS',
             'MENOS',
             'POR',
             'DIVICION',
             'IGUAL',
             'RESIDUO',
             'EXCLAMA',
             'AND1',
             'OR1',
             'NOT',
             'XOR',
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
             'INCREMENTO',
             'DECREMENTO',
             'MASIGUAL',
             'MENOSIGUAL',
             'PORIGUAL',
             'DIVIIGUAL',
             'RESIGUAL',
             'IZQIGUAL',
             'DERIGUAL',
             'ANDIGUAL',
             'ORIGUAL',
             'XORIGUAL',
             'DECIMAL',
             'ENTERO',
             'CADENA',
             'ID'
         ] + list(reservadas.values())

t_PARENTA = r'\('
t_PARENTC = r'\)'
t_CORCHEA = r'\['
t_CORCHEC = r'\]'
t_LLAVEA = r'\{'
t_LLAVEC = r'\}'
t_PUNTOCOMA = r';'
t_DOSPUNTOS = r':'
t_COMA = r','
#t_PUNTO = r'\.'
t_TERNARIO = r'\?'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVICION = r'/'
t_IGUAL = r'='
t_RESIDUO = r'%'
t_EXCLAMA = r'!'
t_AND1 = r'&&'
t_OR1 = r'\|\|'
t_NOT = r'~'
t_XOR = r'\^'
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
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'
t_MASIGUAL = r'\+='
t_MENOSIGUAL = r'-='
t_PORIGUAL = r'\*='
t_RESIGUAL = r'%='
t_IZQIGUAL = r'<<='
t_DERIGUAL = r'>>='
t_ANDIGUAL = r'&='
t_ORIGUAL = r'\|='
t_XORIGUAL = r'\^='

def t_DIVIIGUAL(t):
    r'/='
    print(t.value)
    return t


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


def t_CHAR(t):
    r'\'.\''
    t.value = t.value[1:-1]
    t.value = t.value.replace("\\n", "\n")
    t.value = t.value.replace("\\t", "\t")
    t.value = t.value.replace("\\r", "\r")
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    t.value = t.value.replace("\\n", "\n")
    t.value = t.value.replace("\\t", "\t")
    t.value = t.value.replace("\\r", "\r")
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t


def t_COMENTARIO_S(t):
    r'//(.*)\n'
    t.lexer.lineno += 1

def t_COMENTARIO_M(t):
    r'/\*(.*)\*/'
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

precedence = (
    ('left', 'COMA'),
    ('left', 'IGUAL','MASIGUAL','MENOSIGUAL', 'PORIGUAL', 'DIVIIGUAL', 'RESIGUAL','IZQIGUAL', 'DERIGUAL', 'ANDIGUAL','ORIGUAL', 'XORIGUAL'),
    ('left', 'TERNARIO'),
    ('left', 'OR1'),
    ('left', 'AND1'),
    ('left', 'OR2'),
    ('left', 'XOR'),
    ('left', 'AND2'),
    ('left', 'IGUALIGUAL', 'DIFERENTE'),
    ('left', 'MAYORIGUAL', 'MENORIGUAL', 'MAYOR', 'MENOR'),
    ('left', 'SHIFTI', 'SHIFTD'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVICION', 'RESIDUO'),
    ('left', 'INCREMENTO', 'DECREMENTO'),
    ('left', 'PARENTA', 'PARENTC'),
    ('left', 'ID')
)



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
    '''instruccion : metodos
                   | funciones
                   | structs'''
    t[0] = t[1]


def p_metodos(t):
    '''metodos : VOID ID PARENTA PARENTC bloque_sentencias
               | VOID ID PARENTA lista_param PARENTC bloque_sentencias'''

def p_funciones(t):
    '''funciones : tipo ID PARENTA PARENTC bloque_sentencias
                 | tipo ID PARENTA lista_param PARENTC bloque_sentencias
                 | INT MAIN PARENTA PARENTC bloque_sentencias'''


def p_structs(t):
    '''structs : STRUCT ID LLAVEA declaracion LLAVEC PUNTOCOMA'''


def p_lista_param_lista(t):
    '''lista_param : lista_param COMA param'''


def p_lista_param_param(t):
    '''lista_param : param'''


def p_param(t):
    '''param : tipo ID'''
#             | STRUCT ID lista_apunt'''

def p_bloque_sentencias(t):
    '''bloque_sentencias : LLAVEA lista_sentencias LLAVEC'''

def p_bloque_sentencias_vacio(t):
    '''bloque_sentencias : LLAVEA LLAVEC'''

def p_lista_sentencias_list(t):
    '''lista_sentencias : lista_sentencias sentencia'''

def p_lista_sentencias_sent(t):
    '''lista_sentencias : sentencia
                        | '''

def p_sentencia(t):
    '''sentencia : declaracion PUNTOCOMA
                 | asignacion PUNTOCOMA
                 | fun_if
                 | fun_switch
                 | fun_for
                 | fun_while
                 | fun_do_while
                 | print
                 | scan
                 | fun_return PUNTOCOMA
                 | fun_break PUNTOCOMA
                 | incre_decre PUNTOCOMA
                 | fun_continue PUNTOCOMA'''


def p_declaracion(t):
    '''declaracion : tipo lista_declaracion'''

def p_lista_declaracion(t):
    '''lista_declaracion : lista_declaracion COMA bloque_declara'''


def p_lista_declara_bloque(t):
    '''lista_declaracion : bloque_declara'''

def p_bloque_declara(t):
    '''bloque_declara : declaraConVal
                      | declaraSinVal'''

def p_declaraConVal(t):
    '''declaraConVal : tipo_ID IGUAL operaciones'''

def p_declaraConVal_llave(t):
    '''declaraConVal : tipo_ID IGUAL LLAVEA lista_filas LLAVEC'''

def p_declaraConVal_Fila(t):
    '''declaraConVal : tipo_ID IGUAL LLAVEA lista_val LLAVEC'''

def p_declaraSinVal(t):
    '''declaraSinVal : tipo_ID'''

def p_tipo(t):
    '''tipo : INT
            | CHAR
            | DOUBLE
            | FLOAT'''


def p_TIPO_ID(t):
    '''tipo_ID : ID
               | ID dimension'''

def p_dimension(t):
    '''dimension : dimension CORCHEA val CORCHEC
                 | CORCHEA val CORCHEC
                 | CORCHEA CORCHEC'''

def p_asignacion(t):
    '''asignacion : ID tipo_asignacion operaciones
                  | ID dimension tipo_asignacion operaciones
                  | ID dimension tipo_asignacion LLAVEA lista_filas LLAVEC
                  | ID dimension tipo_asignacion LLAVEA lista_val LLAVEC'''

def p_tipo_asign(t):
    '''tipo_asignacion : IGUAL
                       | MASIGUAL
                       | MENOSIGUAL
                       | PORIGUAL 
                       | DIVIIGUAL
                       | RESIGUAL
                       | IZQIGUAL
                       | DERIGUAL
                       | ANDIGUAL
                       | ORIGUAL
                       | XORIGUAL'''
def p_lista_filas(t):
    '''lista_filas : lista_filas COMA fila'''

def p_lista_filas_fila(t):
    '''lista_filas : fila'''

def p_fila(t):
    '''fila : LLAVEA lista_columna LLAVEC'''

def p_lista_columna(t):
    '''lista_columna : lista_columna COMA columna'''

def p_lista_columna_colum(t):
    '''lista_columna : columna'''

def p_columna(t):
    '''columna : operaciones '''

def p_lista_val_lista(t):
    '''lista_val : lista_val COMA val'''

def p_lista_val_val(t):
    '''lista_val : val'''

def p_if(t):
    '''fun_if : IF PARENTA operaciones PARENTC bloque_sentencias
              | IF PARENTA operaciones PARENTC bloque_sentencias ELSE fun_if
              | IF PARENTA operaciones PARENTC bloque_sentencias ELSE bloque_sentencias'''

def p_switch(t):
    '''fun_switch : SWITCH PARENTA operaciones PARENTC LLAVEA list_switch LLAVEC'''

def p_list_switch(t):
    '''list_switch : list_switch cont_switch
                    | cont_switch'''

def p_cont_switch(t):
    '''cont_switch : CASE val DOSPUNTOS lista_sentencias
                   | CASE val DOSPUNTOS bloque_sentencias
                   | CASE val DOSPUNTOS
                   | DEFAULT DOSPUNTOS lista_sentencias
                   | DEFAULT DOSPUNTOS bloque_sentencias
                   | DEFAULT DOSPUNTOS'''

def p_for(t):
    '''fun_for : FOR PARENTA declaracion PUNTOCOMA operaciones PUNTOCOMA incre_decre PARENTC bloque_sentencias
               | FOR PARENTA asignacion PUNTOCOMA operaciones PUNTOCOMA incre_decre PARENTC bloque_sentencias
               | FOR PARENTA declaracion PUNTOCOMA operaciones PUNTOCOMA incre_decre PARENTC LLAVEA LLAVEC 
               | FOR PARENTA asignacion PUNTOCOMA operaciones PUNTOCOMA incre_decre PARENTC LLAVEA LLAVEC'''

def p_while(t):
    '''fun_while : WHILE PARENTA operaciones PARENTC bloque_sentencias'''

def p_do_while(t):
    '''fun_do_while : DO bloque_sentencias WHILE PARENTA operaciones PARENTC PUNTOCOMA
                    | DO LLAVEA LLAVEC WHILE PARENTA operaciones PARENTC PUNTOCOMA'''


def p_return(t):
    '''fun_return : RETURN operaciones
                  | RETURN incre_decre
                  | RETURN '''

def p_break(t):
    '''fun_break : BREAK'''

def p_inc_dec(t):
    '''incre_decre : INCREMENTO val
                   | DECREMENTO val
                   | val INCREMENTO
                   | val DECREMENTO'''

def p_print(t):
    '''print : PRINTF PARENTA lista_print PARENTC PUNTOCOMA'''

def p_scan(t):
    '''scan : SCANF PARENTA lista_print PARENTC PUNTOCOMA'''

def p_continue(t):
    '''fun_continue : CONTINUE'''

def p_lista_print(t):
    '''lista_print : lista_print COMA operaciones
                   | operaciones'''

def p_operaciones(t):
    '''operaciones : operaciones MAS operaciones
                     | operaciones MENOS operaciones
                     | operaciones POR operaciones
                     | operaciones DIVICION operaciones
                     | operaciones RESIDUO operaciones
                     | operaciones AND1 operaciones
                     | operaciones OR1 operaciones
                     | operaciones XOR operaciones
                     | operaciones AND2 operaciones
                     | operaciones OR2 operaciones
                     | operaciones SHIFTI operaciones
                     | operaciones SHIFTD operaciones
                     | operaciones IGUALIGUAL operaciones
                     | operaciones DIFERENTE operaciones
                     | operaciones MAYORIGUAL operaciones
                     | operaciones MENORIGUAL operaciones
                     | operaciones MAYOR operaciones
                     | operaciones MENOR operaciones
                     | PARENTA operaciones PARENTC'''
    '''if t[2] == '+':
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
        t[0] = Operacion_Binaria(t[1], t[3], Operacion_Logica.MENOR, t[1].fila, t[1].columna)'''


def p_operaciones_unaria(t):
    '''operaciones : MENOS val
                   | EXCLAMA val
                   | NOT val
                   | SCANF PARENTA PARENTC
                   | AND2 val'''

    '''if t[1] == '-':
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
        t[0] = Array(t.slice[1].lineno, get_Column(t.slice[1]))'''


def p_op_ternario(t):
    '''operaciones : operaciones TERNARIO operaciones DOSPUNTOS operaciones'''

def p_op_val(t):
    '''operaciones : val'''
    t[0] = t[1]


#def p_val_conversiones(t):
#    '''val : conversiones'''
#    t[0] = t[1]


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

def p_val_char(t):
    '''val : CHAR'''


def p_val_variables(t):
    '''val : ID'''
    t[0] = t[1]


def p_val_variables_array(t):
    '''val : variables_array'''
    t[0] = t[1]


def p_v_array(t):
    '''variables_array : ID indices'''
#    if t[1][1] == 't':
#        t[0] = Var_Array(Tipo_Variable.TEMPORALES, t[1], t[2], t.slice[1].lineno, get_Column(t.slice[1]))

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

#def p_conversiones(t):
#    '''conversiones : PARENTA INT PARENTC val
#                    | PARENTA FLOAT PARENTC val
#                    | PARENTA CHAR PARENTC val'''
#    if str(t[2]).lower() == 'int':
#        t[0] = Conversion_Int(t[4], t.slice[1].lineno, get_Column(t.slice[1]))
#    elif str(t[2]).lower() == 'float':
#        t[0] = Conversion_Float(t[4], t.slice[1].lineno, get_Column(t.slice[1]))
#    elif str(t[2]).lower() == 'char':
#        t[0] = Conversion_Char(t[4], t.slice[1].lineno, get_Column(t.slice[1]))


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
