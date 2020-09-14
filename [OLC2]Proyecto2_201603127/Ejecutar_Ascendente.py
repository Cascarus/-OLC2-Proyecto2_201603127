from funciones import *
from Valores_Variables import *
from Errores import *
import Tabla_Simbolos as table_s
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit
import sys
import re

diccionario_label = {}
diccionario_banderas = {}
conta = 0
ambito = []

def ejecutar_imprimir(instr, tabla, consola=QPlainTextEdit):
    texto = consola.toPlainText()
    resultado = resolver_operaciones(instr.mensaje, tabla)
    if isinstance(resultado, dict):
        #resultado = "ERROR: NO SE PUEDE IMPRIMIR UNA ARRAY SIN ESPECIFICAR LA DIRECCION"
        Err = Error(instr.mensaje.id, "Semantico", "No se puede imprimir una array sin especificar la direccion", instr.fila, instr.columna)
        Lista_errores.append(Err)
        return

    if resultado == None:
        Err = Error(instr.mensaje.id, "Semantico", "El dato a imprimir no esta declarado", instr.fila, instr.columna)
        Lista_errores.append(Err)
        return

    #texto += str(resultado) + "\n"
    texto += str(resultado)
    consola.setPlainText(texto)


def ejecutar_asignacion(instr, tabla, ambito, main =QMainWindow, consola=QPlainTextEdit):
    print(str(diccionario_banderas["contador"]), ". Entro a ejecutar asignacion", instr.variable.id)
    resultado = None

    if isinstance(instr.valor, Read):
        resultado1 = False
        val_sin_tipo = ""
        while resultado1 == False:
            valor, resultado1 = QInputDialog.getText(main, "Read()", "Ingrese el valor para " + str(instr.variable.id) + ":", QLineEdit.Normal, "")
            texto = consola.toPlainText()
            texto += valor
            consola.setPlainText(texto)
            if resultado1 == True:
                val_sin_tipo = valor

        resultado1 = False
        if resultado1 == False:
            try:
                resultado = int(val_sin_tipo)
                print("fue transfomado en int: ", resultado)
                resultado1 = True
            except (ValueError, TypeError):
                print("no es int")

        if resultado1 == False:
            try:
                resultado = float(val_sin_tipo);
                print("fue transformado en float: ", resultado)
                resultado1 = True
            except:
                print("no es float")
        if resultado1 == False:
            try:
                resultado = str(val_sin_tipo);
                print("fue transformado en sting: ", resultado)
                resultado1 = True
            except:
                print("no es String")
    else:
        resultado = resolver_operaciones(instr.valor, tabla)

    if resultado == True:
        resultado = 1
    elif resultado == False:
        resultado = 0
    elif resultado == None:
        return

    tipo = obt_tipo(resultado)
    simbolo = table_s.Simbolo(instr.variable.id, tipo, resultado, 1, ambito, None)

    if isinstance(instr.variable, Var_Array):
        if tabla.existe_simbolo(simbolo):
            if isinstance(tabla.get_simbolo(instr.variable.id).valor, dict):
                lista1 = tabla.get_simbolo(instr.variable.id).valor
                lista2 = []
                for val in instr.variable.lista:
                    lista2.append(obtener_valores(val, tabla))
                lista1 = asignar_valor_array(lista1, lista2, resultado, instr.variable.id, instr.variable.fila, instr.variable.columna)
                if lista1 == None:
                    Err = Error(simbolo.id, "Semantico", "No se puede insertar el valor, el indice esta ocupado", instr.variable.fila, instr.variable.columna)
                    Lista_errores.append(Err)
                    return
                tipo = Tipo_Dato.ARRAY
                simbolo = table_s.Simbolo(instr.variable.id, tipo, lista1, None,ambito,None)

            elif isinstance(tabla.get_simbolo(instr.variable.id).valor, str):
                lista1 = tabla.get_simbolo(instr.variable.id).valor
                lista2 = []
                for val in instr.variable.lista:
                    lista2.append(obtener_valores(val, tabla))
                lista1 = asignar_valor_array(lista1, lista2, resultado, instr.variable.id, instr.variable.fila, instr.variable.columna)
                if lista1 == None:
                    Err = Error(simbolo.id, "Semantico", "No se puede insertar el valor, el indice esta ocupado",
                                instr.variable.fila, instr.variable.columna)
                    Lista_errores.append(Err)
                    return
                tipo = Tipo_Dato.CADENA# cadena
                simbolo = table_s.Simbolo(instr.variable.id, tipo, lista1, None, ambito, None)
            else:
                Err = Error(simbolo.id, "Semantico", "La variable no es de tipo array", instr.variable.fila, instr.variable.columna)
                Lista_errores.append(Err)
                return
        else:
            Err = Error(simbolo.id, "Semantico", "La variable no ha sido creada", instr.fila, instr.columna)
            Lista_errores.append(Err)
            return


    if tabla.existe_simbolo(simbolo):
        sim = tabla.get_simbolo(simbolo.id)
        entor_ant = sim.declarada
        simbolo.declarada = entor_ant
        tabla.update_simbolo(simbolo)
    else:
        tabla.add_simbolo(simbolo)


def ejecutar_if(instr, tabla, conta, consola=QPlainTextEdit, main = QMainWindow):
    expresion_logica = resolver_operaciones(instr.op_logica, tabla)
    print(str(diccionario_banderas["contador"]), ". Entro a if", str(instr.goto_etiqueta), " resultado....", str(expresion_logica))
    etiqueta = instr.goto_etiqueta

    # ir a buscar la etiqueta q corresponde y ejecutar
    if expresion_logica == True or expresion_logica == 1:
        #hacer validacion de que la etiqueta exista
        if etiqueta in diccionario_label:
            return diccionario_label[etiqueta]
        else:
            Err = Error(etiqueta,"Sintactico", "LA ETIQUETA NO ESTA DEFINIDA", instr.fila, instr.columna)
            Lista_errores.append(Err)
            return 1000
    return conta


def ejecutar_goto(instr, tabla, consola=QPlainTextEdit, main = QMainWindow):
    print(str(diccionario_banderas["contador"]), ". Entro a goto", instr.etiqueta)
    etiqueta = instr.etiqueta
    if etiqueta in diccionario_label:
        return diccionario_label[etiqueta]
    else:
        Err = Error(etiqueta, "Sintactico", "LA ETIQUETA NO ESTA DEFINIDA", instr.fila, instr.columna)
        Lista_errores.append(Err)
        return 1000


def ejecutar_Unset(instr, tabla):
     id = instr.variable.id
     eliminar = tabla.delete_simbolo(id)
     if not eliminar:
         Err = Error(id, "Sintactico", "LA VARIABLE NO EXISTE", instr.fila, instr.columna)
         Lista_errores.append(Err)


def resolver_operaciones(Val_variable, tabla):
    if isinstance(Val_variable, Operacion_Binaria):

        exp1 = resolver_operaciones(Val_variable.val1, tabla)
        exp2 = resolver_operaciones(Val_variable.val2, tabla)
        tipo1 = obtener_tipo(Val_variable.val1, tabla)
        tipo2 = obtener_tipo(Val_variable.val2, tabla)

        if exp1 == None:
            Err = Error(Val_variable.val1.id, "SEMANTICO", "EL DATO NO ESTA DECLARADO", Val_variable.fila, Val_variable.columna)
            Lista_errores.append(Err)
            return None

        if exp2 == None:
            Err = Error(Val_variable.val2.id, "SEMANTICO", "EL DATO NO ESTA DECLARADO", Val_variable.fila,
                        Val_variable.columna)
            Lista_errores.append(Err)
            return None

        if isinstance(Val_variable.val1, Var_Array):
            tipo1 = obt_tipo(exp1)
        if isinstance(Val_variable.val2, Var_Array):
            tipo2 = obt_tipo(exp2)

        #EMPIEZAN LAS OPERACIONES MATEMATICAS
        if Val_variable.operacion == Operacion_Aritmetica.SUMA:
            # return exp1 + exp2
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 + exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return exp1 + exp2
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return exp1 + exp2
            elif tipo1 == Tipo_Dato.CADENA and tipo2 == Tipo_Dato.CADENA:
                return str(exp1) + str(exp2)
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", " NO SE PUEDE SUMAR VALRORES DE TIPO " + str(tipo1) + " CON VALORES DE TIPO " + str(tipo2),Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Aritmetica.RESTA:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 - exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return exp1 - exp2
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return exp1 - exp2
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", "SOLO SE PUEDE RESTAR VALORES DE TIPO ENTERO O DE TIPO DECIMAL",Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Aritmetica.POR:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 * exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return exp1 * exp2
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return exp1 * exp2
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", "SOLO SE PUEDE MULTIPLICAR VALORES DE TIPO ENTERO O DE TIPO DECIMAL", Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Aritmetica.DIVICION:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                try:
                    return exp1 / exp2
                except ZeroDivisionError:
                    Err = Error(Val_variable.val1.id, "SEMANTICO", "SOLO SE PUEDE MULTIPLICAR VALORES DE TIPO ENTERO O DE TIPO DECIMAL", Val_variable.fila,Val_variable.columna)
                    Lista_errores.append(Err)
                    return None
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                try:
                    return exp1 / exp2
                except ZeroDivisionError:
                    Err = Error(Val_variable.val1.id, "SEMANTICO",
                                "SOLO SE PUEDE MULTIPLICAR VALORES DE TIPO ENTERO O DE TIPO DECIMAL", Val_variable.fila,
                                Val_variable.columna)
                    Lista_errores.append(Err)
                    return None
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                try:
                    return exp1 / exp2
                except ZeroDivisionError:
                    Err = Error(Val_variable.val1.id, "SEMANTICO", "SOLO SE PUEDE MULTIPLICAR VALORES DE TIPO ENTERO O DE TIPO DECIMAL", Val_variable.fila, Val_variable.columna)
                    Lista_errores.append(Err)
                    return None
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", "SOLO SE PUEDE DIVIDIR VALORES DE TIPO ENTERO O DE TIPO DECIMAL", Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Aritmetica.RESIDUIO:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 % exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return exp1 % exp2
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return exp1 % exp2
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", "SOLO SE PUEDE CALCULAR RESIDUO VALORES DE TIPO ENTERO O DE TIPO DECIMAL", Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        #EMPIEZAN LAS OPERACIONES LOGICAS
        elif Val_variable.operacion == Operacion_Logica.DIFERENTE:
            # return exp1 + exp2
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 != exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return float(exp1) != float(exp2)
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return float(exp1) != float(exp2)
            elif tipo1 == Tipo_Dato.CADENA or tipo2 == Tipo_Dato.CADENA:
                return str(exp1) != str(exp2)
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", "NO SE PUEDE HACER UNA OPERACION LOGICA ENTRE VALORES DE TIPO " + tipo1 + " CON VALORES DE TIPO " + tipo2, Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Logica.IGUAL_IGUAL:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 == exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return float(exp1) == float(exp2)
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return exp1 == exp2
            elif tipo1 == Tipo_Dato.CADENA and tipo2 == Tipo_Dato.CADENA:
                return str(exp1) == str(exp2)
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", "NO SE PUEDE HACER UNA OPERACION LOGICA ENTRE VALORES DE TIPO " + tipo1 + " CON VALORES DE TIPO " + tipo2, Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Logica.MAYOR_IGUAL:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 >= exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return float(exp1) >= float(exp2)
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return float(exp1) >= float(exp2)
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO", "SOLO SE PUEDE HACER UNA OPERACION MAYOR IGUAL ENTRE VALORES DE TIPO ENTERO Y DECIMAL", Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Logica.MENOR_IGUAL:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 <= exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return float(exp1) <= float(exp2)
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return float(exp1) <= float(exp2)
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO","SOLO SE PUEDE HACER UNA OPERACION MENOR IGUAL ENTRE VALORES DE TIPO ENTERO Y DECIMAL", Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Logica.MAYOR:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 > exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return float(exp1) > float(exp2)
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return float(exp1) > float(exp2)
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDE HACER UNA OPERACION MAYOR QUE ENTRE VALORES DE TIPO ENTERO Y DECIMAL",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Logica.MENOR:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 < exp2
            elif (tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.ENTERO) or (
                    tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.DECIMAL):
                return float(exp1) < float(exp2)
            elif tipo1 == Tipo_Dato.DECIMAL and tipo2 == Tipo_Dato.DECIMAL:
                return float(exp1) < float(exp2)
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDE HACER UNA OPERACION MENOR QUE ENTRE VALORES DE TIPO ENTERO Y DECIMAL",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Logica.AND:
            temp1 = False
            temp2 = False

            if int(exp1) == 1 or int(exp1) == 0:
                temp1 = True
            if int(exp2) == 1 or int(exp2) == 0:
                temp2 = True

            if temp1 and temp2:
                if int(exp1) == 1 and int(exp2) == 1:
                    return 1
                return 0
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDE REALIZAR AND CON VALORES DE 0 O 1",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Logica.OR:
            temp1 = False
            temp2 = False

            if int(exp1) == 1 or int(exp1) == 0:
                temp1 = True
            if int(exp2) == 1 or int(exp2) == 0:
                temp2 = True

            if temp1 and temp2:
                if int(exp1) == 0 and int(exp2) == 0:
                    return 0
                return 1
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDE REALIZAR OR CON VALORES DE 0 O 1",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                print("ERROR SEMANTICO: SOLO SE PUEDE OR VALORES DE 0 O 1")
                return

        elif Val_variable.operacion == Operacion_Logica.XOR:
            temp1 = False
            temp2 = False

            if int(exp1) == 1 or int(exp1) == 0:
                temp1 = True
            if int(exp2) == 1 or int(exp2) == 0:
                temp2 = True

            if temp1 and temp2:
                if (int(exp1) == 0 and int(exp2) == 1) or (int(exp1) == 1 and int(exp2) == 0):
                    return 1
                return 0
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDE REALIZAR XOR CON VALORES DE 0 O 1",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                print("ERROR SEMANTICO: SOLO SE PUEDE XOR VALORES 0 O 1")
                return None

        #EMPIEZAN LAS OPERACIONES BIT A BIT
        elif Val_variable.operacion == Operacion_Bit.AND:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                temp = exp1 & exp2
                return temp
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDEN HACER OPERACIONES BIT A BIT CON ENTEROS",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Bit.OR:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 | exp2
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDEN HACER OPERACIONES BIT A BIT CON ENTEROS",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Bit.XOR:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 ^ exp2
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDEN HACER OPERACIONES BIT A BIT CON ENTEROS",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Bit.SHIFTI:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 << exp2
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDEN HACER OPERACIONES BIT A BIT CON ENTEROS",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

        elif Val_variable.operacion == Operacion_Bit.SHIFTD:
            if tipo1 == Tipo_Dato.ENTERO and tipo2 == Tipo_Dato.ENTERO:
                return exp1 >> exp2
            else:
                Err = Error(Val_variable.val1.id, "SEMANTICO",
                            "SOLO SE PUEDEN HACER OPERACIONES BIT A BIT CON ENTEROS",
                            Val_variable.fila, Val_variable.columna)
                Lista_errores.append(Err)
                return None

    elif isinstance(Val_variable, Numerico_Negativo):
        resultado = obtener_valores(Val_variable.val, tabla)
        if resultado == None:
            Err = Error(Val_variable.val.id, "SEMANTICO", "EL DATO NO ESTA DECLARADO", Val_variable.fila, Val_variable.columna)
            Lista_errores.append(Err)
            return None
        tipo = obtener_tipo(Val_variable.val, tabla)
        if tipo == Tipo_Dato.ENTERO or tipo == Tipo_Dato.DECIMAL:
            return resultado * -1
        Err = Error(Val_variable.val.id, "SEMANTICO", "SOLO SE PUEDE CALCULAR EL NEGATIVO DE ENTEROS Y DECIMALES", Val_variable.fila, Val_variable.columna)
        Lista_errores.append(Err)
        return None

    elif isinstance(Val_variable, Numerico_Absoluto):
        valor = obtener_valores(Val_variable.val, tabla)
        tipo = obtener_tipo(Val_variable.val, tabla)
        if tipo == Tipo_Dato.ENTERO or tipo == Tipo_Dato.DECIMAL:
            return abs(valor)
        Err = Error(Val_variable.val.id, "SEMANTICO", "SOLO SE PUEDE CALCULAR EL ABSOLUTO DE ENTEROS Y DECIMALES",
                    Val_variable.fila, Val_variable.columna)
        Lista_errores.append(Err)
        return None

    elif isinstance(Val_variable, Bool_Negado):
        resultado = obtener_valores(Val_variable.val, tabla)
        tipo = obtener_tipo(Val_variable.val, tabla)

        if tipo == Tipo_Dato.ENTERO:
            if int(resultado) == 1:
                return 0
            elif int(resultado) == 0:
                return 1
            else:
                Err = Error(Val_variable.val.id, "SEMANTICO",
                            "SOLO SE PUEDE REALIZAR INSTRUCCIONES LOGICAS CON VALORES DE 0 O 1", Val_variable.fila,
                            Val_variable.columna)
                Lista_errores.append(Err)
        else:
            Err = Error(Val_variable.val.id, "SEMANTICO",
                        "SOLO SE PUEDE REALIZAR INSTRUCCIONES LOGICAS CON VALORES DE 0 O 1", Val_variable.fila,
                        Val_variable.columna)
            Lista_errores.append(Err)
        return None

    elif isinstance(Val_variable, Bit_Negado):
        resultado = obtener_valores(Val_variable.val, tabla)
        tipo = obtener_tipo(Val_variable.val, tabla)

        if tipo == Tipo_Dato.ENTERO:
            return ~resultado
        else:
            Err = Error(Val_variable.val1.id, "SEMANTICO",
                        "SOLO SE PUEDE REALIZAR UNA OPERACION BIT A BIT CON ENTEROS", Val_variable.fila,
                        Val_variable.columna)
            Lista_errores.append(Err)
            return None


    elif isinstance(Val_variable, Array):
        return {}

    elif isinstance(Val_variable, Conversion_Int):
        valor = obtener_valores(Val_variable.val, tabla)
        tipo = obtener_tipo(Val_variable.val, tabla)

        if valor == None:
            Err = Error(Val_variable.val.id,"SEMANTICO","LA VARIABLE A CONVERTIR NO EXISTE",Val_variable.fila,Val_variable.columna)
            Lista_errores.append(Err)
            return None

        if tipo == Tipo_Dato.ENTERO:
            return int(valor)
        if tipo == Tipo_Dato.DECIMAL:
            return int(valor)
        elif tipo == Tipo_Dato.CADENA:
            ascii = ord(valor[0])
            return ascii

    elif isinstance(Val_variable, Conversion_Float):
        valor = obtener_valores(Val_variable.val, tabla)
        tipo = obtener_tipo(Val_variable.val, tabla)

        if valor == None:
            Err = Error(Val_variable.val.id,"SEMANTICO","LA VARIABLE A CONVERTIR NO EXISTE",Val_variable.fila,Val_variable.columna)
            Lista_errores.append(Err)
            return None

        if tipo == Tipo_Dato.ENTERO:
            return float(valor)
        if tipo == Tipo_Dato.DECIMAL:
            return float(valor)
        elif tipo == Tipo_Dato.CADENA:
            ascii = ord(valor[0])
            return float(ascii)

    elif isinstance(Val_variable, Conversion_Char):
        valor = obtener_valores(Val_variable.val, tabla)
        tipo = obtener_tipo(Val_variable.val, tabla)

        if valor == None:
            Err = Error(Val_variable.val.id,"SEMANTICO","LA VARIABLE A CONVERTIR NO EXISTE",Val_variable.fila,Val_variable.columna)
            Lista_errores.append(Err)
            return None

        if tipo == Tipo_Dato.ENTERO:
            if valor <= 255:
                return chr(valor)
            return chr(valor % 256)

        if tipo == Tipo_Dato.DECIMAL:
            valor = int(valor)
            if valor <= 255:
                return chr(valor)
            return chr(valor % 256)

        elif tipo == Tipo_Dato.CADENA:
            return valor[0]

    else:
        return obtener_valores(Val_variable, tabla)


def obtener_valores(Val_variable, tabla):
    if isinstance(Val_variable, Numerico_Decimal):
        return Val_variable.val
    elif isinstance(Val_variable, Numerico_Entero):
        return Val_variable.val
    elif isinstance(Val_variable, String_Val):
        return Val_variable.val
    elif isinstance(Val_variable, Var_Temporales):
        return tabla.get_simbolo(Val_variable.id).valor
    elif isinstance(Val_variable, Var_Parametros):
        return tabla.get_simbolo(Val_variable.id).valor
    elif isinstance(Val_variable, Var_Devueltos):
        return tabla.get_simbolo(Val_variable.id).valor
    elif isinstance(Val_variable, Var_Simulado):
        return tabla.get_simbolo(Val_variable.id).valor
    elif isinstance(Val_variable, Var_Pila):
        return tabla.get_simbolo(Val_variable.id).valor
    elif isinstance(Val_variable, Var_Puntero_Pila):
        return tabla.get_simbolo(Val_variable.id).valor
    elif isinstance(Val_variable, Var_Array):
        nombre = str(Val_variable.id)
        if tabla.existe_id(Val_variable.id):
            if isinstance(tabla.get_simbolo(Val_variable.id).valor, dict) or isinstance(tabla.get_simbolo(Val_variable.id).valor, str):
                lista = tabla.get_simbolo(Val_variable.id).valor
                lista2 = []
                for val in Val_variable.lista:
                    lista2.append(obtener_valores(val, tabla))
                    nombre += "[" + str(obtener_valores(val, tabla)) + "]"
                valor = get_valor_array(lista2, lista, Val_variable.id, Val_variable.fila, Val_variable.columna)
                if valor == None:
                    Err = Error(nombre, "Semantico", "La posicion del arreglo no esta definida", Val_variable.fila,Val_variable.columna)
                    Lista_errores.append(Err)
                return valor
            else:
                Err = Error(nombre, "Semantico", "La variable no es de tipo array", Val_variable.fila,Val_variable.columna)
                Lista_errores.append(Err)
                return
        else:
            Err = Error(nombre, "Semantico", "La variable no ha sido creada", Val_variable.fila, Val_variable.columna)
            Lista_errores.append(Err)
            return
    else:
        return None


def obtener_tipo(Val_variable, tabla):
    if isinstance(Val_variable, Numerico_Entero):
        return Val_variable.tipo
    elif isinstance(Val_variable, Numerico_Decimal):
        return Val_variable.tipo
    elif isinstance(Val_variable, String_Val):
        return Val_variable.tipo
    elif isinstance(Val_variable, Var_Temporales):
        return tabla.get_simbolo(Val_variable.id).tipo
    elif isinstance(Val_variable, Var_Parametros):
        return tabla.get_simbolo(Val_variable.id).tipo
    elif isinstance(Val_variable, Var_Devueltos):
        return tabla.get_simbolo(Val_variable.id).tipo
    elif isinstance(Val_variable, Var_Simulado):
        return tabla.get_simbolo(Val_variable.id).tipo
    elif isinstance(Val_variable, Var_Pila):
        return tabla.get_simbolo(Val_variable.id).tipo
    elif isinstance(Val_variable, Var_Puntero_Pila):
        return tabla.get_simbolo(Val_variable.id).tipo
    elif isinstance(Val_variable, Numerico_Negativo):
        return obtener_tipo(Val_variable.val, tabla)


def obt_tipo(resultado):
    if isinstance(resultado, int):
        return Tipo_Dato.ENTERO
    elif isinstance(resultado, float):
        return Tipo_Dato.DECIMAL
    elif isinstance(resultado, str):
        return Tipo_Dato.CADENA
    elif isinstance(resultado, dict):
        return Tipo_Dato.ARRAY
    else:
        return None

def asignar_valor_array(lista, posiciones, valor, id, fila, columna):
    if isinstance(lista, str):
        return valor_array(posiciones, valor, lista, id, fila, columna)
    if(posiciones[0] in lista):
        if len(posiciones) > 1:
            temp = valor_array(posiciones[1:], valor, lista[posiciones[0]], id, fila, columna)
            if temp == None:
                return None
            lista[posiciones[0]] = temp
        else:
            lista[posiciones[0]] = valor
        return lista
    else:
        if len(posiciones) > 1:
            temp = valor_array(posiciones[1:], valor, {}, id, fila, columna)
            if temp == None:
                return None
            lista[posiciones[0]] = temp
        else:
            lista[posiciones[0]] = valor

        return lista



def valor_array(posiciones, valor, lista, id, fila, columna):
    if (len(posiciones) > 1):
        if not (posiciones[0] in lista):
            lista[posiciones[0]] = {}
        temp = valor_array(posiciones[1:], valor, lista[posiciones[0]], id, fila, columna)
        if temp != None:
            lista[posiciones[0]] = temp
            return lista
        else:
            return None
    else:
        if isinstance(lista, dict):
            lista[posiciones[0]] = valor
            return lista
        elif isinstance(lista, str):
            lista_str = list(lista)
            if posiciones[0] >= len(lista_str):
                for i in range(posiciones[0] - len(lista_str)):
                    lista_str.append(chr(32))
                lista_str.append(valor)
            else:
                lista_str[posiciones[0]] = str(valor)
            nuevo_str = "".join(lista_str)
            lista = nuevo_str
            return lista
        else:
            #Err = Error(id,"Semantico","El indice esta ocupado", fila, columna)
            #Lista_errores.append(Err)
            return None


def get_valor_array(posiciones, lista, id, fila, columna):
    if len(posiciones) > 1:
        if posiciones[0] in lista:
            temp = get_valor_array(posiciones[1:], lista[posiciones[0]], id, fila, columna)
            return temp
        else:
            #agregar error
            return None
    else:
        try:
            #hacer validacion de chars y si el dato existe
            if isinstance(lista, dict) or isinstance(lista, str):
                return lista[posiciones[0]]
            else:
                #La lista esta vacia
                Err = Error(id, "Semantico", "El indice esta ocupado", fila, columna)
                Lista_errores.append(Err)
                return None
        except:
            return IndexError

def inicializar():
    diccionario_banderas.clear()
    diccionario_label.clear()
    diccionario_banderas["contador"] = 0
    diccionario_banderas["ambito"] = ""

def iniciar_ejecucion(instrucciones, tabla, consola=QPlainTextEdit, MainWindow = QMainWindow):
    inicializar()
    sys.setrecursionlimit(10000)
    limit = sys.getrecursionlimit()
    print(limit)

    a = 0
    for instr in instrucciones:
        if isinstance(instr, Etiqueta):
            nombre_etiqueta = str(instr.id)
            diccionario_label[nombre_etiqueta] = a
        a += 1

    ejecutar(instrucciones, tabla, consola, MainWindow)


def iniciar_debbug(texto, indice, instrucciones, tabla, consola=QPlainTextEdit, MainWindow = QMainWindow):
    if indice < 0:
        inicializar()
        indice += 1
        a = 0
        for instr in instrucciones:
            if isinstance(instr, Etiqueta):
                nombre_etiqueta = str(instr.id)
                diccionario_label[nombre_etiqueta] = a
            a += 1
    mostrar_debug(texto, indice,consola)
    temp = debbug(instrucciones,tabla,consola,MainWindow,indice)
    return temp



def ejecutar(instrucciones, tabla, consola, main):
    conta = 0
    ambito = ""
    while conta < len(instrucciones):
        if isinstance(instrucciones[conta], Etiqueta):
            ambito = str(instrucciones[conta].id)

        if isinstance(instrucciones[conta], Asignacion):
            diccionario_banderas["contador"] = diccionario_banderas["contador"] + 1
            ejecutar_asignacion(instrucciones[conta], tabla, ambito, main, consola)

        elif isinstance(instrucciones[conta], Imprimir):
            ejecutar_imprimir(instrucciones[conta], tabla, consola)

        elif isinstance(instrucciones[conta], If_Goto):
            conta = ejecutar_if(instrucciones[conta], tabla, conta, consola, main)

        elif isinstance(instrucciones[conta], Goto):
            conta = ejecutar_goto(instrucciones[conta], tabla, consola, main)

        elif isinstance(instrucciones[conta], Exit):
            break

        elif isinstance(instrucciones[conta], Unset):
            ejecutar_Unset(instrucciones[conta], tabla)

        conta += 1

def debbug(instruccion, tabla, consola, main, indice):
    ind = indice
    ambito = diccionario_banderas["ambito"]
    if indice <= len(instruccion):
        if isinstance(instruccion[indice], Etiqueta):
            diccionario_banderas["ambito"] = str(instruccion[indice].id)

        elif isinstance(instruccion[indice], Asignacion):
            diccionario_banderas["contador"] = diccionario_banderas["contador"] + 1
            ejecutar_asignacion(instruccion[indice], tabla, ambito, main, consola)

        elif isinstance(instruccion[indice], Imprimir):
            ejecutar_imprimir(instruccion[indice], tabla, consola)

        elif isinstance(instruccion[indice], If_Goto):
            ind = ejecutar_if(instruccion[indice], tabla, indice, consola, main)

        elif isinstance(instruccion[indice], Goto):
            ind = ejecutar_goto(instruccion[indice], tabla, consola, main)

        elif isinstance(instruccion[indice], Exit):
            ind = -1

        elif isinstance(instruccion[indice], Unset):
            ejecutar_Unset(instruccion[indice], tabla)

        ind += 1
        if ind == len(instruccion):
            ind = -1

    return ind

def mostrar_debug(texto_analizar, indice, consola = QPlainTextEdit):
    texto = texto_analizar
    texto = re.sub(r'\#(.*)\n', "", texto)
    texto = texto.replace(" ", "")
    texto = texto.replace("\t", "")
    texto_limpio = texto.split("\n")
    nuevo = []
    for lin in texto_limpio:
        if lin != "":
            nuevo.append(lin)
    texto_limpio = nuevo
    texto_debug = "Debugeando--->" + str(texto_limpio[indice]) + "\n"
    consola.setPlainText(texto_debug)

