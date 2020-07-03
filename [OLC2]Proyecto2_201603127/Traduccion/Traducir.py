from Traduccion.Ambito import ambito
from Traduccion.Valores import *
from Traduccion.Tipos import Tipo_dato
from Traduccion.Main import clase_main
from Traduccion.Declaracion import Declaracion

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
        codigo_main = "main:\n"
        nueva_etiqueta =  new_etiqueta()
        set_salida(nueva_etiqueta)
        #atributo = Atributos()
        for instr in self.instrucciones:
            aux = instr.generar_C3D()
            if isinstance(instr,clase_main):
                #temp = codigo_main
                codigo_main += aux[0]
            elif isinstance(instr, Declaracion):
                codigo_main += aux[0]
            else:
                cod_augus += aux[0]
        retornos = get_etiquetal()
        salida_salida = new_etiqueta()
        codigo_main += "goto " + salida_salida + ";\n\n"

        if len(retornos) != 0:
            conta = 0
            temporal = new_temp()
            lista_llave = list(retornos.keys())
            lista_values = list(retornos.values())
            cod_augus += str(nueva_etiqueta) + ":\n"
            cod_augus += "if($ra == -1) goto " + salida_salida + ";\n"
            cod_augus += str(temporal) + " = $s1[$ra];\n"

            for llave in lista_llave:
                cod_augus += "if(" + str(temporal) + " == " + str(llave) + ") goto " + lista_values[conta] + ";\n"
                conta += 1

            cod_augus += "\n" + str(salida_salida) + ":\nexit;"

        else:
            cod_augus += str(salida_salida) + ":\nexit;"


        return codigo_main + cod_augus