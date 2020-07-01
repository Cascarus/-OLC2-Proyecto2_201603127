temporales = 0
parametros = 0
devueltos = 0
pila = 0
simulador = 0
puntero = 0
etiqueta = 0
conta_nombre = 0
sim_report = []

def new_temp():
    global temporales
    nombre = "$t" + str(temporales)
    temporales += 1
    return nombre

def get_temp():
    global temporales
    return "$t" + str(temporales)

def new_etiqueta():
    global etiqueta
    nombre = "etq" + str(etiqueta)
    etiqueta += 1
    return nombre

def get_etiqueta():
    global  etiqueta
    nombre = 'etq' + str(etiqueta)
    return nombre

def new_param():
    global  parametros
    nombre = "$a" + str(parametros)
    parametros += 1
    return nombre

def new_dev():
    global devueltos
    nombre = "$v" + str(devueltos)
    devueltos += 11
    return nombre

def add_sim_report(simbolo):
    global sim_report
    sim_report.append(simbolo)

def new_nombre():
    global conta_nombre
    nombre = str(conta_nombre)
    conta_nombre += 1
    return nombre

def limpiar():
    global temporales
    global parametros
    global devueltos
    global pila
    global simulador
    global puntero
    global etiqueta
    global sim_report

    temporales = 0
    parametros = 0
    devueltos = 0
    pila = 0
    simulador = 0
    puntero = 0
    etiqueta = 0
    sim_report.clear()


