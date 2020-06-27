from Traduccion.Ambito import ambito
from Traduccion.Valores import limpiar
from Traduccion.Tipos import Tipo_dato

class traducir():
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.raiz = ambito(None)

    def inizializar_tablas(self):
        ''''aqui va la traduccion'''
        limpiar()
        for instr in self.instrucciones:
            resultado = instr.agregar_Tabla(self.raiz, "global")

            if resultado == False:
                return False


    def verificar_tipos(self):
        for instr in self.instrucciones:
            resultado = instr.verificar_tipo(self.raiz)

            if resultado == False:
                return False

        return self

    def comenzar_traduccion(self):
        cod_augus = ""
        #atributo = Atributos()
        for instr in self.instrucciones:
            aux = instr.generar_C3D()
            cod_augus += aux[0]

        return cod_augus