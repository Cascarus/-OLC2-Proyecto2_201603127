class Metodos:
    '''clase  abstracta'''

class Asignacion(Metodos):
    def __init__(self, variable, valor, fila, columna):
        self.variable = variable
        self.valor = valor
        self.fila = fila
        self.columna = columna

class Imprimir(Metodos):
    def __init__(self, mensaje, fila, columna):
        self.mensaje = mensaje
        self.fila = fila
        self.columna = columna

class If_Goto(Metodos):
    def __init__(self, op_logica, goto_etiqueta, fila, columna):
        self.op_logica = op_logica
        self.goto_etiqueta = goto_etiqueta
        self.fila = fila
        self.columna = columna

class Goto(Metodos):
    def __init__(self, etiqueta, fila, columna):
        self. etiqueta = etiqueta
        self.fila = fila
        self.columna = columna

class Read(Metodos):
    def __init__(self, fila, columna):
        '''Esta clase es del read'''
        self.fila = fila
        self.columna = columna

class Unset(Metodos):
    def __init__(self, variable, fila, columna):
        self.variable = variable
        self.fila = fila
        self.columna = columna

class Exit(Metodos):
    def __init__(self, fila, columna):
        ''''Esta clase es del exit'''
        self.fila = fila
        self.columna = columna

class Array(Metodos):
    def __init__(self, fila, columna):
        '''Esta clase es del read'''
        self.fila = fila
        self.columna = columna