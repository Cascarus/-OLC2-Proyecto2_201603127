from graphviz import Digraph
from AST import *
from Traduccion.Valores import *


class AST_MiniC():
    contador = 0

    def crear_reporte(self, lista):
        dot = Digraph(comment="Reporte AST descendente",
                      format="png",
                      node_attr={'shape': 'box'})

        nombre_padre = str(new_nombre())
        dot.node(nombre_padre, "Inicio")

        for inst in lista:
            inst.generar_AST(dot, nombre_padre)

        try:
            dot.render("Reportes/Reporte_AST_C", view=False)
        except:
            print("El reporte no se pudo gener")

    def __init__(self):
        '''clase del reporte simbolos'''
