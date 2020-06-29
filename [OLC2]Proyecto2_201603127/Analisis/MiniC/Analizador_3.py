from Errores import *
from Traduccion.Primitivos import Primitivo
from Traduccion.Declaracion import Declaracion
from Traduccion.Funciones import funciones
from Traduccion.Variables import variables
from Traduccion.Tipos import *
from Traduccion.Operacion_binaria import Operacion_binaria
from Traduccion.Operacion_relacional import Op_relacional
from Traduccion.Operacion_logica import Op_logica
from Traduccion.Asignacion import Asignacion
from Traduccion.If import If
from Traduccion.Print import Print
from Traduccion.Scanf import Scanf
from Traduccion.Operacion_unaria import Operacion_unaria
from Traduccion.Incre_Decre import incre_decre
from Traduccion.For import For
from Traduccion.While import While
from Traduccion.Do_While import Do_While
from Traduccion.Break import Break
from Traduccion.Switch import Switch

from Analisis.MiniC.ply import lex

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
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
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
    ('left', 'INCREMENTO', 'DECREMENTO','NOT', 'EXCLAMA'),
    ('left', 'PARENTA', 'PARENTC'),
    ('left', 'ID')
)



def p_init(t):
#    '''inicio : instrucciones'''
    '''inicio : lista_sentencias'''
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
                 | INT MAIN PARENTA PARENTC bloque_sentencias'''
    t[0] = funciones(t[1], t[2], None, t[5],t.slice[3].lineno, get_Column(t.slice[3]))

def p_funciones_param(t):
    '''funciones : tipo ID PARENTA lista_param PARENTC bloque_sentencias'''

def p_structs(t):
    '''structs : STRUCT ID LLAVEA declaracion LLAVEC PUNTOCOMA'''


def p_lista_param_lista(t):
    '''lista_param : lista_param COMA param'''


def p_lista_param_param(t):
    '''lista_param : param'''


def p_param(t):
    '''param : tipo ID'''

def p_bloque_sentencias(t):
    '''bloque_sentencias : LLAVEA lista_sentencias LLAVEC'''
    t[0] = t[2]

def p_bloque_sentencias_vacio(t):
    '''bloque_sentencias : LLAVEA LLAVEC'''
    t[0] = None

def p_lista_sentencias_list(t):
    '''lista_sentencias : lista_sentencias sentencia'''
    t[1].append(t[2])
    t[0] = t[1]

def p_lista_sentencias_sent(t):
    '''lista_sentencias : sentencia'''
    t[0] = [t[1]]

def p_lista_sentencia_vacio(t):
    '''lista_sentencias : '''
    t[0] = [None]

def p_sentencia(t):
    '''sentencia : declaracion PUNTOCOMA
                 | asignacion PUNTOCOMA
                 | fun_if
                 | fun_switch
                 | fun_for
                 | fun_while
                 | fun_do_while
                 | print
                 | fun_return PUNTOCOMA
                 | fun_break PUNTOCOMA
                 | incre_decre PUNTOCOMA
                 | fun_continue PUNTOCOMA'''
    t[0] = t[1]


def p_declaracion(t):
    '''declaracion : tipo lista_declaracion'''
    t[0] = Declaracion(t[1][0],t[2], t[1][1], t[1][2])

def p_lista_declaracion(t):
    '''lista_declaracion : lista_declaracion COMA bloque_declara'''
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_declara_bloque(t):
    '''lista_declaracion : bloque_declara'''
    t[0] = [t[1]]

def p_bloque_declara(t):
    '''bloque_declara : declaraConVal
                      | declaraSinVal'''
    t[0] = t[1]

def p_declaraConVal(t):
    '''declaraConVal : tipo_ID IGUAL operaciones'''
    t[0] = [t[1], t[3]]

def p_declaraConVal_char(t):
    '''declaraConVal : ID CORCHEA CORCHEC IGUAL CADENA'''
    t[0] = [t[1], t[5]]

def p_declaraConVal_Scan(t):
    '''declaraConVal : tipo_ID IGUAL SCANF PARENTA PARENTC'''
    t[0] = [t[1],Scanf(t.slice[2].lineno, get_Column(t.slice[2]))]

def p_declaraConVal_llave(t):
    '''declaraConVal : tipo_ID IGUAL LLAVEA lista_filas LLAVEC'''
    t[0] = [t[1], t[4]]
def p_declaraConVal_Fila(t):
    '''declaraConVal : tipo_ID IGUAL LLAVEA lista_val LLAVEC'''
    t[0] = [t[1], t[4]]

def p_declaraSinVal(t):
    '''declaraSinVal : tipo_ID'''
    t[0] = [t[1], None]

def p_tipo(t):
    '''tipo : INT
            | CHAR
            | DOUBLE
            | FLOAT'''

    if str(t[1]).lower() == 'int':
        t[0] = [Tipo_dato.ENTERO, t.slice[1].lineno, get_Column(t.slice[1])]
    elif str(t[1]).lower() == 'char':
        t[0] = [Tipo_dato.CARACTER, t.slice[1].lineno, get_Column(t.slice[1])]
    elif str(t[1]).lower() == 'double':
        t[0] = [Tipo_dato.DECIMAL, t.slice[1].lineno, get_Column(t.slice[1])]
    elif str(t[1]).lower() == 'float':
        t[0] = [Tipo_dato.DECIMAL, t.slice[1].lineno, get_Column(t.slice[1])]


def p_TIPO_ID_id(t):
    '''tipo_ID : ID'''
    t[0] = variables(t[1], t.slice[1].lineno, get_Column(t.slice[1]))

def p_TIPO_ID_dimen(t):
    '''tipo_ID : ID dimension'''

def p_dimension(t):
    '''dimension : dimension CORCHEA val CORCHEC
                 | CORCHEA val CORCHEC
                 | CORCHEA CORCHEC'''

def p_asignacion(t):
    '''asignacion : lista_asignacion'''
    t[0] = Asignacion(t[1], t[1][0][0].fila, t[1][0][0].columna)


def p_lista_asignacion(t):
    '''lista_asignacion : lista_asignacion COMA bloque_asignacion'''
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_asignacion_b(t):
    '''lista_asignacion : bloque_asignacion'''
    t[0] = [t[1]]

def p_bloque_asignacion_1(t):
    '''bloque_asignacion : tipo_ID tipo_asignacion operaciones'''
    t[0] = [t[1], t[3], t[2]]

def p_bloque_asignacion_2(t):
    '''bloque_asignacion : tipo_ID IGUAL SCANF PARENTA PARENTC'''
    t[0] = [t[1], Scanf(t.slice[2].lineno,get_Column(t.slice[2])), t[2]]

def p_bloque_asignacion_3(t):
    '''bloque_asignacion : tipo_ID tipo_asignacion LLAVEA lista_filas LLAVEC
                      | tipo_ID tipo_asignacion LLAVEA lista_val LLAVEC'''

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

    if t[1] == '=':
        t[0] = tipo_asign.IGUAL
    elif t[1] == '+=':
        t[0] = tipo_asign.MASIGUAL
    elif t[1] == '-=':
        t[0] = tipo_asign.MENOSIGUAL
    elif t[1] == '*=':
        t[0] = tipo_asign.PORIGUAL
    elif t[1] == '/=':
        t[0] = tipo_asign.DIVIIGUAL
    elif t[1] == '%=':
        t[0] = tipo_asign.RESIGUAL
    elif t[1] == '<<=':
        t[0] = tipo_asign.IZQIGUAL
    elif t[1] == '>>=':
        t[0] = tipo_asign.DERIGUAL
    elif t[1] == '&=':
        t[0] = tipo_asign.ANDIGUAL
    elif t[1] == '|=':
        t[0] = tipo_asign.ORIGUAL
    elif t[1] == '^=':
        t[0] = tipo_asign.XORIGUAL


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
    '''fun_if : IF PARENTA operaciones PARENTC bloque_sentencias'''
    t[0] = If([t[3]], [t[5]], None, t.slice[1].lineno, get_Column(t.slice[1]))

def p_elif(t):
    '''fun_if : IF PARENTA operaciones PARENTC bloque_sentencias ELSE fun_if'''
    t[3] = [t[3]] + t[7].operaciones
    t[5] = [t[5]] + t[7].contenido
    t[0] = If(t[3], t[5], t[7].cont_else, t.slice[1].lineno, get_Column(t.slice[1]))

def p_else(t):
    '''fun_if : IF PARENTA operaciones PARENTC bloque_sentencias ELSE bloque_sentencias'''
    t[0] = If([t[3]],[t[5]],t[7],t.slice[1].lineno, get_Column(t.slice[1]))

def p_switch_1(t):
    '''fun_switch : SWITCH PARENTA operaciones PARENTC LLAVEA list_switch default LLAVEC'''
    t[0] = Switch(t[3], t[6], t[7], t.slice[1].lineno, get_Column(t.slice[1]))

def p_switch_2(t):
    '''fun_switch : SWITCH PARENTA operaciones PARENTC LLAVEA list_switch LLAVEC'''
    t[0] = Switch(t[3], t[6], None, t.slice[1].lineno, get_Column(t.slice[1]))

def p_switch_3(t):
    '''fun_switch : SWITCH PARENTA operaciones PARENTC LLAVEA default LLAVEC'''
    t[0] = Switch(t[3], None, t[7], t.slice[1].lineno, get_Column(t.slice[1]))
def p_switch_4(t):
    '''fun_switch : SWITCH PARENTA operaciones PARENTC LLAVEA LLAVEC'''
    t[0] = Switch(t[3], None, None, t.slice[1].lineno, get_Column(t.slice[1]))

def p_list_switch_1(t):
    '''list_switch : list_switch cont_switch'''
    t[1].append(t[2])
    t[0] = t[1]

def p_list_switch_2(t):
    '''list_switch :  cont_switch'''
    t[0] = [t[1]]

def p_cont_switch_1(t):
    '''cont_switch : CASE val DOSPUNTOS lista_sentencias'''
    t[0] = [t[2], t[4]]

def p_cont_switch_2(t):
    '''cont_switch : CASE val DOSPUNTOS'''
    t[0] = [t[2], None]

def p_default_1(t):
    '''default : DEFAULT DOSPUNTOS lista_sentencias'''
    t[0] = t[3]

def p_default_2(t):
    '''default : DEFAULT DOSPUNTOS'''
    t[0] = None

def p_for_lleno(t):
    '''fun_for : FOR PARENTA declaracion PUNTOCOMA operaciones PUNTOCOMA incre_decre PARENTC bloque_sentencias
               | FOR PARENTA asignacion PUNTOCOMA operaciones PUNTOCOMA incre_decre PARENTC bloque_sentencias'''

    t[0] = For(t[3], t[5], t[7], t[9], t.slice[1].lineno, get_Column(t.slice[1]))

def p_while(t):
    '''fun_while : WHILE PARENTA operaciones PARENTC bloque_sentencias'''
    t[0] = While(t[3], t[5], t.slice[1].lineno, get_Column(t.slice[1]))

def p_do_while(t):
    '''fun_do_while : DO bloque_sentencias WHILE PARENTA operaciones PARENTC PUNTOCOMA'''
    t[0] = Do_While(t[5], t[2], t.slice[1].lineno, get_Column(t.slice[1]))

def p_return(t):
    '''fun_return : RETURN operaciones
                  | RETURN incre_decre
                  | RETURN '''

def p_break(t):
    '''fun_break : BREAK'''
    t[0] = Break(t.slice[1].lineno, get_Column(t.slice[1]))

def p_inc_dec(t):
    '''incre_decre : INCREMENTO val
                   | DECREMENTO val
                   | val INCREMENTO
                   | val DECREMENTO'''
    if t[1] == '++':
        t[0] = incre_decre(t[2], tipo_incre.INCRE, 0, t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1] == '--':
        t[0] = incre_decre(t[2], tipo_incre.DECRE, 0, t.slice[1].lineno, get_Column(t.slice[1]))
    else:
        if t[2] == '++':
            t[0] = incre_decre(t[1], tipo_incre.INCRE, 1, t.slice[2].lineno, get_Column(t.slice[2]))
        elif t[2] == '--':
            t[0] = incre_decre(t[1], tipo_incre.DECRE, 1, t.slice[2].lineno, get_Column(t.slice[2]))

def p_print(t):
    '''print : PRINTF PARENTA val PARENTC PUNTOCOMA'''
    t[0] = Print(t[3],t.slice[1].lineno, get_Column(t.slice[1]))

def p_continue(t):
    '''fun_continue : CONTINUE'''

def p_operaciones_bin(t):
    '''operaciones : operaciones MAS operaciones
                     | operaciones MENOS operaciones
                     | operaciones POR operaciones
                     | operaciones DIVICION operaciones
                     | operaciones RESIDUO operaciones'''
    if t[2] == '+':
        t[0] = Operacion_binaria(t[1], t[3], Tipo_operacion.SUMA, t[1].fila, t[1].columna)
    elif t[2] == '-':
        t[0] = Operacion_binaria(t[1], t[3], Tipo_operacion.RESTA, t[1].fila, t[1].columna)
    elif t[2] == '*':
        t[0] = Operacion_binaria(t[1], t[3], Tipo_operacion.POR, t[1].fila, t[1].columna)
    elif t[2] == '/':
        t[0] = Operacion_binaria(t[1], t[3], Tipo_operacion.DIVICION, t[1].fila, t[1].columna)
    else:
        t[0] = Operacion_binaria(t[1], t[3], Tipo_operacion.RESIDUIO, t[1].fila, t[1].columna)

def p_operaciones_logicas(t):
    '''operaciones : operaciones AND1 operaciones
                     | operaciones OR1 operaciones'''

    if t[2] == '&&':
        t[0] = Op_logica(t[1], t[3], Operacion_logica.AND, t[1].fila, t[1].columna)
    elif t[2] == '||':
        t[0] = Op_logica(t[1], t[3], Operacion_logica.OR, t[1].fila, t[1].columna)

def p_operacion_relacional(t):
    '''operaciones : operaciones IGUALIGUAL operaciones
                     | operaciones DIFERENTE operaciones
                     | operaciones MAYORIGUAL operaciones
                     | operaciones MENORIGUAL operaciones
                     | operaciones MAYOR operaciones
                     | operaciones MENOR operaciones'''

    if t[2] == '==':
        t[0] = Op_relacional(t[1], t[3], Operacion_logica.IGUAL_IGUAL, t[1].fila, t[1].columna)
    elif t[2] == '!=':
        t[0] = Op_relacional(t[1], t[3], Operacion_logica.DIFERENTE, t[1].fila, t[1].columna)
    elif t[2] == '>=':
        t[0] = Op_relacional(t[1], t[3], Operacion_logica.MAYOR_IGUAL, t[1].fila, t[1].columna)
    elif t[2] == '<=':
        t[0] = Op_relacional(t[1], t[3], Operacion_logica.MENOR_IGUAL, t[1].fila, t[1].columna)
    elif t[2] == '>':
        t[0] = Op_relacional(t[1], t[3], Operacion_logica.MAYOR, t[1].fila, t[1].columna)
    else:
        t[0] = Op_relacional(t[1], t[3], Operacion_logica.MENOR, t[1].fila, t[1].columna)


def p_operaciones_bit(t):
    '''operaciones : operaciones XOR operaciones
                     | operaciones AND2 operaciones
                     | operaciones OR2 operaciones
                     | operaciones SHIFTI operaciones
                     | operaciones SHIFTD operaciones'''
    if t[2] == '&':
        t[0] = Operacion_binaria(t[1], t[3], Operacion_bit.AND, t[1].fila, t[1].columna)
    elif t[2] == '|':
        t[0] = Operacion_binaria(t[1], t[3], Operacion_bit.OR, t[1].fila, t[1].columna)
    elif t[2] == '^':
        t[0] = Operacion_binaria(t[1], t[3], Operacion_bit.XOR, t[1].fila, t[1].columna)
    elif t[2] == '<<':
        t[0] = Operacion_binaria(t[1], t[3], Operacion_bit.SHIFTI, t[1].fila, t[1].columna)
    else:
        t[0] = Operacion_binaria(t[1], t[3], Operacion_bit.SHIFTD, t[1].fila, t[1].columna)

def p_operaciones_unaria(t):
    '''operaciones : MENOS operaciones
                   | EXCLAMA operaciones
                   | NOT operaciones
                   | AND2 operaciones'''
    if t[1] == '-':
        t[0] = Operacion_unaria(t[2],tipo_unaria.MENOS, t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1] == '!':
        t[0] = Operacion_unaria(t[2],tipo_unaria.EXCLAMA, t.slice[1].lineno, get_Column(t.slice[1]))
    elif t[1] == '~':
        t[0] = Operacion_unaria(t[2],tipo_unaria.NOT, t.slice[1].lineno, get_Column(t.slice[1]))
    else:
        t[0] = Operacion_unaria(t[2], tipo_unaria.AND, t.slice[1].lineno, get_Column(t.slice[1]))


def p_op_ternario(t):
    '''operaciones : operaciones TERNARIO operaciones DOSPUNTOS operaciones'''

def p_op_incre(t):
    '''operaciones : incre_decre'''
    t[0] = t[1]

def p_op_val(t):
    '''operaciones : val'''
    t[0] = t[1]

def p_op_corche(t):
    '''operaciones : PARENTA operaciones PARENTC'''
    t[0] = t[2]

def p_val_numerico_entero(t):
    '''val : ENTERO'''
    print(t)
    t[0] = Primitivo(t[1], Tipo_dato.ENTERO, t.slice[1].lineno, get_Column(t.slice[1]))

def p_val_numerico_decimal(t):
    '''val : DECIMAL'''
    t[0] = Primitivo(t[1], Tipo_dato.DECIMAL, t.slice[1].lineno, get_Column(t.slice[1]))

def p_val_cadena(t):
    '''val : CADENA'''
    t[0] = Primitivo(t[1], Tipo_dato.CADENA, t.slice[1].lineno, get_Column(t.slice[1]))

def p_val_char(t):
    '''val : CHAR'''
    t[0] = Primitivo(t[1],Tipo_dato.CARACTER, t.slice[1].lineno, get_Column(t.slice[1]))

def p_val_variables(t):
    '''val : ID'''
    t[0] = variables(t[1], t.slice[1].lineno, get_Column(t.slice[1]))


def p_val_variables_array(t):
    '''val : variables_array'''
    t[0] = t[1]


def p_v_array(t):
    '''variables_array : ID indices'''

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

from Analisis.MiniC.ply import yacc as yacc
parser = yacc.yacc()

def parse(texto):
    lexer.lineno = 1
    return parser.parse(texto)
