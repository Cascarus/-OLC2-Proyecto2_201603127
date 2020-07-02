from Traduccion.Abstracta import abst


class funciones(abst):
    def __init__(self,tipo, id, parametros, instrucciones, fila, columna):
        self.tipo = tipo
        self.id = id
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna