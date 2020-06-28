from Traduccion.Abstracta import abst

class Print(abst):

    def __init__(self, contenido, fila, columna):
        self.contenido = contenido
        self.fila = fila
        self.columna = columna


    def verificar_tipo(self, ambito):
        tipo_cont = self.contenido.verificar_tipo(ambito)

        if tipo_cont == False:
            return False
        else:
            return True


    def generar_C3D(self):
        augus = ""

        contenido = self.contenido.generar_C3D("print")
        augus += contenido[0]
        augus += "print(" + str(contenido[1]) + ");\n"

        return[augus, ""]