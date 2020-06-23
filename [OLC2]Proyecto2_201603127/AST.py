from funciones import *
from Valores_Variables import *

Lista_AST = []

class Nodo_AST():
    def __init__(self, id, hijos = []):
        self.id = id
        self.hijos = hijos

    def agregar_hijo(self,nodo):
        self.hijos.append(nodo)

class AST():
    diccionario_label = {}
    diccionario_banderas = {}
    lista_etiquetas = []
    conta = 0
    raiz = None

    def ejecutar_imprimir(self,instr):
        lista_hijos = []
        resultado = self.resolver_operaciones(instr.mensaje)
        lista_hijos.append(resultado)
        nodo = Nodo_AST("Imprimir", lista_hijos)
        return nodo

    def ejecutar_asignacion(self, instr):
        lista_hijos = []
        resultado = ""
        if isinstance(instr.valor, Read):
            resultado = Nodo_AST("Read()", [])
        else:
            resultado = self.resolver_operaciones(instr.valor)
        nodo = Nodo_AST(instr.variable.id, [])


        if isinstance(instr.variable, Var_Array):
            lista = ""
            for val in instr.variable.lista:
                lista += "[" + str(self.obt_val(val)) + "]"
            nodo = Nodo_AST(str(instr.variable.id) + str(lista),[])
        lista_hijos.append(nodo)
        lista_hijos.append(resultado)
        nodo = Nodo_AST("Asignacion", lista_hijos)
        return nodo

    def ejecutar_if(self, instr):
        lista_hijos = []
        expresion_logica = self.resolver_operaciones(instr.op_logica)
        nodo = Nodo_AST(instr.goto_etiqueta, [])
        lista_hijos.append(expresion_logica)
        lista_hijos.append(nodo)

        nodo = Nodo_AST("if Goto", lista_hijos)
        return nodo

    def ejecutar_goto(self, instr):
        nodo = Nodo_AST(instr.etiqueta, [])
        nodo2 = Nodo_AST("Goto", [nodo])
        return nodo2

    def ejecutar_Unset(self, instr):
        nodo = Nodo_AST(instr.variable.id, [])
        nodo2 = Nodo_AST("Unset", [nodo])
        return nodo2

    def resolver_operaciones(self, Val_variable):
        if isinstance(Val_variable, Operacion_Binaria):
            exp1 = self.obtener_valores(Val_variable.val1)
            exp2 = self.obtener_valores(Val_variable.val2)
            signo = ""
            lista = []
            # EMPIEZAN LAS OPERACIONES MATEMATICAS
            if Val_variable.operacion == Operacion_Aritmetica.SUMA:
                nodo = Nodo_AST("+", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Aritmetica.RESTA:
                nodo = Nodo_AST("-", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Aritmetica.POR:
                nodo = Nodo_AST("*", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Aritmetica.DIVICION:
                nodo = Nodo_AST("/", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Aritmetica.RESIDUIO:
                nodo = Nodo_AST("%", [])
                lista = [exp1, nodo, exp2]

            # EMPIEZAN LAS OPERACIONES LOGICAS
            elif Val_variable.operacion == Operacion_Logica.DIFERENTE:
                nodo = Nodo_AST("!=", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.IGUAL_IGUAL:
                nodo = Nodo_AST("==", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.MAYOR_IGUAL:
                nodo = Nodo_AST(">=", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.MENOR_IGUAL:
                nodo = Nodo_AST("<=", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.MAYOR:
                nodo = Nodo_AST(">", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.MENOR:
                nodo = Nodo_AST("<", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.AND:
                nodo = Nodo_AST("&&", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.OR:
                nodo = Nodo_AST("||", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Logica.XOR:
                nodo = Nodo_AST("xor", [])
                lista = [exp1, nodo, exp2]

            # EMPIEZAN LAS OPERACIONES BIT A BIT
            elif Val_variable.operacion == Operacion_Bit.AND:
                nodo = Nodo_AST("&", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Bit.OR:
                nodo = Nodo_AST("|", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Bit.XOR:
                nodo = Nodo_AST("^", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Bit.SHIFTI:
                nodo = Nodo_AST("<<", [])
                lista = [exp1, nodo, exp2]

            elif Val_variable.operacion == Operacion_Bit.SHIFTD:
                nodo = Nodo_AST(">>", [])
                lista = [exp1, nodo, exp2]

            nodo = Nodo_AST("Operacion binaria", lista)
            return nodo

        elif isinstance(Val_variable, Numerico_Negativo):
            resultado = self.obtener_valores(Val_variable.val)
            lista = [resultado]
            nodo = Nodo_AST("Negativo", lista)
            return nodo

        elif isinstance(Val_variable, Numerico_Absoluto):
            resultado = self.obtener_valores(Val_variable.val)
            lista = [resultado]
            nodo = Nodo_AST("Absoluto", lista)
            return nodo

        elif isinstance(Val_variable, Bool_Negado):
            resultado = self.obtener_valores(Val_variable.val)
            lista = [resultado]
            nodo = Nodo_AST("Not", lista)
            return nodo

        elif isinstance(Val_variable, Bit_Negado):
            resultado = self.obtener_valores(Val_variable.val)
            lista = [resultado]
            nodo = Nodo_AST("Not", lista)
            return nodo

        elif isinstance(Val_variable, Array):
            nodo = Nodo_AST("Array", [])
            return nodo

        elif isinstance(Val_variable, Conversion_Int):
            resultado = self.obtener_valores(Val_variable.val)
            nodo = Nodo_AST("int", [])
            lista = [nodo, resultado]
            nodo = Nodo_AST("Conversion", lista)
            return nodo

        elif isinstance(Val_variable, Conversion_Float):
            resultado = self.obtener_valores(Val_variable.val)
            nodo = Nodo_AST("float", [])
            lista = [nodo, resultado]
            nodo = Nodo_AST("Conversion", lista)
            return nodo

        elif isinstance(Val_variable, Conversion_Char):
            resultado = self.obtener_valores(Val_variable.val)
            nodo = Nodo_AST("char", [])
            lista = [nodo, resultado]
            nodo = Nodo_AST("Conversion", lista)
            return nodo

        else:
            return self.obtener_valores(Val_variable)

    def obtener_valores(self, Val_variable):
        if isinstance(Val_variable, Numerico_Decimal):
            nodo = Nodo_AST(str(Val_variable.val), [])
            return nodo
        elif isinstance(Val_variable, Numerico_Entero):
            nodo = Nodo_AST(str(Val_variable.val), [])
            return nodo
        elif isinstance(Val_variable, String_Val):
            nodo = Nodo_AST(str(Val_variable.val), [])
            return nodo
        elif isinstance(Val_variable, Var_Temporales):
            nodo = Nodo_AST(Val_variable.id, [])
            return nodo
        elif isinstance(Val_variable, Var_Parametros):
            nodo = Nodo_AST(Val_variable.id, [])
            return nodo
        elif isinstance(Val_variable, Var_Devueltos):
            nodo = Nodo_AST(Val_variable.id, [])
            return nodo
        elif isinstance(Val_variable, Var_Simulado):
            nodo = Nodo_AST(Val_variable.id, [])
            return nodo
        elif isinstance(Val_variable, Var_Pila):
            nodo = Nodo_AST(Val_variable.id, [])
            return nodo
        elif isinstance(Val_variable, Var_Puntero_Pila):
            nodo = Nodo_AST(Val_variable.id, [])
            return nodo
        elif isinstance(Val_variable, Var_Array):
            id = Val_variable.id
            lista = ""
            for val in Val_variable.lista:
                lista += "[" + str(self.obt_val(val)) + "]"
            nodo = Nodo_AST(str(id + lista), [])
            return nodo

    def obt_val(self, Val_variable):
        if isinstance(Val_variable, Numerico_Decimal):
            return Val_variable.val
        elif isinstance(Val_variable, Numerico_Entero):
            return Val_variable.val
        elif isinstance(Val_variable, String_Val):
            return Val_variable.val
        elif isinstance(Val_variable, Var_Temporales):
            return Val_variable.id
        elif isinstance(Val_variable, Var_Parametros):
            return Val_variable.id
        elif isinstance(Val_variable, Var_Devueltos):
            return Val_variable.id
        elif isinstance(Val_variable, Var_Simulado):
            return Val_variable.id
        elif isinstance(Val_variable, Var_Pila):
            return Val_variable.id
        elif isinstance(Val_variable, Var_Puntero_Pila):
            return Val_variable.id
        elif isinstance(Val_variable, Var_Array):
            id = Val_variable.id
            lista = str(id)
            for val in Val_variable.lista:
                lista += "[" + str(self.obt_val(val)) + "]"
            return lista

    def inicializar(self):
        self.diccionario_banderas.clear()
        self.diccionario_label.clear()
        self.lista_etiquetas.clear()
        self.diccionario_banderas["ultimo"] = False
        self.diccionario_banderas["ended"] = False
        self.diccionario_banderas["contador"] = 0

    def iniciar_ejecucion(self, instrucciones):
        self.inicializar()
        lista_acciones = []
        nombre_actual = str(instrucciones[0].id).lower()

        for instr in instrucciones:
            if isinstance(instr, Etiqueta):
                nombre_etiqueta = str(instr.id).lower()
                self.lista_etiquetas.append(nombre_etiqueta)
                if nombre_actual != nombre_etiqueta:
                    self.diccionario_label[nombre_actual] = lista_acciones.copy()
                    lista_acciones.clear()
                    nombre_actual = nombre_etiqueta

            elif isinstance(instr, Asignacion):
                lista_acciones.append(instr)

            elif isinstance(instr, Imprimir):
                lista_acciones.append(instr)

            elif isinstance(instr, If_Goto):
                lista_acciones.append(instr)

            elif isinstance(instr, Goto):
                lista_acciones.append(instr)

            elif isinstance(instr, Exit):
                lista_acciones.append(instr)

            elif isinstance(instr, Unset):
                lista_acciones.append(instr)

        self.diccionario_label[nombre_actual] = lista_acciones.copy()
        lista_acciones.clear()

        lista_raiz_hijos = []
        try:
            for etiqeta in self.lista_etiquetas:
                lista_hijos = self.ejecutar(self.diccionario_label[etiqeta])
                nombre = etiqeta
                nodo = Nodo_AST(nombre, lista_hijos)
                lista_raiz_hijos.append(nodo)
        except:
            print("Ha ocurrido un error y no se ha generado el AST")

        Lista_AST = lista_raiz_hijos
        self.raiz = Nodo_AST("Inicio", Lista_AST)

    def ejecutar(self, instrucciones):
        lista_hijos = []
        for instr in instrucciones:
            if isinstance(instr, Asignacion):
                nodo = self.ejecutar_asignacion(instr)
                lista_hijos.append(nodo)

            elif isinstance(instr, Imprimir):
                nodo = self.ejecutar_imprimir(instr)
                lista_hijos.append(nodo)

            elif isinstance(instr, If_Goto):
                nodo = self.ejecutar_if(instr)
                lista_hijos.append(nodo)

            elif isinstance(instr, Goto):
                nodo = self.ejecutar_goto(instr)
                lista_hijos.append(nodo)

            elif isinstance(instr, Exit):
                nodo = Nodo_AST("Exit", [])
                lista_hijos.append(nodo)

            elif isinstance(instr, Unset):
                nodo = self.ejecutar_Unset(instr)
                lista_hijos.append(nodo)

        return lista_hijos

    def __init__(self):
        '''Crear el AST'''