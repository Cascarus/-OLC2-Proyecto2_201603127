from graphviz import Digraph
from Traduccion.Valores import sim_report

class Reporte_Simbolos:
    def crear_reporte(self):
        dot = Digraph(comment="Minor C - Reporte de simbolos",
                      format="png",
                      node_attr={'shape': 'plaintext'},
                      graph_attr={'rankdir': 'LR'})
        contenido = "<<table border = '1'><tr><td>Fila</td><td>ID</td><td>Tipo</td><td>Ambito</td><td>Dimensiones</td><td>Parametros</td></tr>"

        for simbolo in sim_report:
            temp = simbolo
            contenido += "<tr><td>" + str(temp.fila)+ "</td><td>" + str(temp.id) + "</td><td>" + str(temp.rol) + "</td><td>" + str(temp.ambito) + "</td><td>" + str(temp.tam) + "</td><td>" + str(temp.parametros) + "</td></tr>"

        contenido += "</table>>"
        dot.node("A", contenido)
        dot.node("T", "Reporte de Simbolos")

        try:
            dot.render("Reportes/Reporte_Simbolos", view = False)
        except:
            print("El reporte no se pudo gener")

    def __init__(self):
        '''clase del reporte simbolos'''