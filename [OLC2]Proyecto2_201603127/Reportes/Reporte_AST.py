from graphviz import Digraph
from AST import *


class Reporte_AST():
    contador = 0

    def crear_reporte(self, raiz = Nodo_AST):
        dot = Digraph(comment="Reporte AST descendente",
                      format="png",
                      node_attr={'shape': 'box'})


        dot.node('0', raiz.id)
        self.recorrer(raiz,dot,"0")

        try:
            dot.render("Reportes/Reporte_AST", view = False)
        except:
            print("El reporte no se pudo gener")

    def recorrer(self, raiz, dot, nombre):
        for hijo in raiz.hijos:
            self.contador += 1
            nombre_hijo = str(str(hijo.id) + str(self.contador))
            dot.edge(nombre, nombre_hijo)
            dot.node(nombre_hijo, hijo.id)
            self.recorrer(hijo, dot, nombre_hijo)

    def __init__(self):
        '''clase del reporte simbolos'''