from graphviz import Digraph
import Tabla_Simbolos


class Reporte_Simbolos:
    def crear_reporte(self, Tabla=Tabla_Simbolos):
        dot = Digraph(comment="Reporte de tabla",
                      format="png",
                      node_attr={'shape': 'plaintext'},
                      graph_attr={'rankdir': 'LR'})
        contenido = "<<table border = '1'><tr><td>ID</td><td>Valor</td><td>Tipo</td><td>Dimension</td><td>Declarada</td><td>Referencias</td></tr>"

        for simbolo in Tabla.simbolos:
            temp = Tabla.get_simbolo(simbolo)
            contenido += "<tr><td>" + str(temp.id)+ "</td><td>" + str(temp.valor) + "</td><td>" + str(temp.tipo.name) + "</td><td>" + str(temp.dimension) + "</td><td>" + str(temp.declarada) + "</td><td>" + str(temp.referencias) + "</td></tr>"

        contenido += "</table>>"
        dot.node("A", contenido)
        dot.node("T", "Tabla de Simbolos")

        try:
            dot.render("Reportes/Reporte_Tabla_Simbolos", view = False)
        except:
            print("El reporte no se pudo gener")

    def __init__(self):
        '''clase del reporte simbolos'''
