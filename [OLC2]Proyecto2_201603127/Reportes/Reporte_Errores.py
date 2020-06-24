from graphviz import Digraph
import Errores


class Reporte_Errores:
    def crear_reporte(self, errores):
        dot = Digraph(comment="Reporte de Errores",
                      format="png",
                      node_attr={'shape': 'plaintext'},
                      graph_attr={'rankdir': 'LR'})
        contenido = "<<table border = '1'>\n<tr><td>Token</td><td>Tipo</td><td>Descripcion</td><td>Fila</td><td>Columna</td></tr>\n"

        for error in errores:
            cont = str(error.token)
            if cont.find('&') != -1:
                cont = str(error.token).replace('&', "&#38;")
            elif cont.find('<') != -1:
                cont = str(error.token).replace('<', "&#60;")
            elif cont.find('>') != -1:
                cont = str(error.token).replace('>', "&#62;")
            else:
                cont = str(error.token)
            contenido += "<tr><td>" + cont + "</td><td>" + str(error.tipo) + "</td><td>" + str(error.desc) + "</td><td>" + str(error.fila) + "</td><td>" + str(error.columna) + "</td></tr>\n"

        contenido += "</table>>"
        dot.node("A", contenido)
        dot.node("T", "Reporte de Errores")

        try:
            dot.render("Reportes/Reporte_Error", view = False)
        except:
            print("El reporte no se pudo gener")

    def __init__(self):
        '''clase del reporte simbolos'''
