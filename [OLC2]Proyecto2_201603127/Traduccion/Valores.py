temporales = 0
parametros = 0
devueltos = 0
pila = 0
simulador = 0
puntero = 0
etiqueta = 0
conta_nombre = 0
sim_report = []
ret = ""
entorno = None
salida = None
lista_retorno = {}
conta_ambito = 0


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
    devueltos += 1
    return nombre

def add_sim_report(simbolo):
    global sim_report
    sim_report.append(simbolo)

def new_nombre():
    global conta_nombre
    nombre = str(conta_nombre)
    conta_nombre += 1
    return nombre

def set_ret(id):
    global ret
    ret = id

def set_entorno(entor):
    global entorno
    entorno = entor

def get_entorno():
    global entorno
    return entorno

def set_salida(id):
    global salida
    salida = id

def get_salida():
    global salida
    return salida

def incrementar_global():
    global conta_ambito
    conta_ambito += 1

def get_global():
    global conta_ambito
    return conta_ambito

def add_etiquetaL(id):
    global lista_retorno
    global conta_ambito
    lista_retorno[conta_ambito] = id

def get_etiquetal():
    global lista_retorno
    return lista_retorno;

def limpiar():
    global temporales
    global parametros
    global devueltos
    global pila
    global simulador
    global puntero
    global etiqueta
    global sim_report
    global ret
    global entorno
    global salida
    global lista_retorno
    global conta_ambito

    temporales = 0
    parametros = 0
    devueltos = 0
    pila = 0
    simulador = 0
    puntero = 0
    etiqueta = 0
    ret = ""
    entorno = None
    salida = None
    lista_retorno = {}
    conta_ambito = 0
    sim_report.clear()


