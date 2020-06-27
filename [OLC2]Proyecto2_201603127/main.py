# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

#pyuic5 -x main.ui -o main.py


import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from Editor import Editor_Codigo
from Reportes import Reporte_Tabla_Simbolos
from Reportes import Reporte_Errores
from Reportes import Reporte_AST
from Errores import *
from AST import *
from Traduccion.Traducir import traducir


import Analisis.Ascendente.Analizador as p
import Analisis.Descendente.Analizador_2 as asc
import Analisis.MiniC.Analizador as minic
import Ejecutar_Ascendente as Ejec1
import Tabla_Simbolos as tabla


class Ui_MainWindow(object):
    array_rutas = []
    array_editores = []
    array_nombre_tab = []
    nombre_archivo = ""
    ruta_archivo = ""
    Fuente = QtGui.QFont("Microsoft Sans Serif",10)
    Fuente2 = QtGui.QFont("Ebrima", 12)
    ruta_iconos = str(os.getcwd()) + "\Iconos"
    tabla_global = None
    indice = -1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("AUGUS COMPILER")
        MyIcon = QtGui.QIcon(self.ruta_iconos + "\\favicon.png")
        MainWindow.setWindowIcon(MyIcon)
        MainWindow.resize(1355, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.tbTab = QtWidgets.QTabWidget(self.centralwidget)
        self.tbTab.setGeometry(QtCore.QRect(20, 10, 770, 490))
        self.tbTab.setObjectName("tbTab")
        
        #Declaracion de la consola
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 510, 770, 190))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFont(self.Fuente)
        self.txtConsola = QtWidgets.QPlainTextEdit(self.groupBox)
        self.txtConsola.setGeometry(QtCore.QRect(10, 20, 750, 160))
        self.txtConsola.setObjectName("txtConsola")
        self.txtConsola.setFont(self.Fuente2)
        self.txtConsola.setStyleSheet("""QPlainTextEdit {background-color: #333; color: #00FF00;}""")
        self.txtConsola.setReadOnly(True)


        #Creacion del visor de imagenes
        self.visor = QtWidgets.QGraphicsView(self.centralwidget)
        self.visor.setGeometry(QtCore.QRect(795, 10, 555, 690))
        self.visor.setObjectName("qgVisor")

        MainWindow.setCentralWidget(self.centralwidget)

        #Declaracion de opciones del menu
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 21))
        self.menubar.setObjectName("menubar")
        self.menubar.setFont(self.Fuente)

        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuArchivo.setFont(self.Fuente)

        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setObjectName("menuEditar")
        self.menuEditar.setFont(self.Fuente)

        self.menuReportes = QtWidgets.QMenu(self.menubar)
        self.menuReportes.setObjectName("menuReportes")
        self.menuReportes.setFont(self.Fuente)

        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        self.menuAyuda.setFont(self.Fuente)

        self.menuEjecutar = QtWidgets.QMenu(self.menubar)
        self.menuEjecutar.setObjectName("menuEjecutar")
        self.menuEjecutar.setFont(self.Fuente)

        self.menuOpciones = QtWidgets.QMenu(self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        self.menuOpciones.setFont(self.Fuente)
        
        MainWindow.setMenuBar(self.menubar)
        
        #Declaracion de opciones del menu Archivo
        self.actionNuevo = QtWidgets.QAction(MainWindow)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionNuevo.setShortcut("Ctrl+N")
        self.actionNuevo.setIcon(QtGui.QIcon(self.ruta_iconos + "\\nuevo.png"))
        self.actionNuevo.triggered.connect(self.nuevo)

        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionAbrir.setShortcut("Ctrl+A")
        self.actionAbrir.setIcon(QtGui.QIcon(self.ruta_iconos + "\\abrir.png"))
        self.actionAbrir.triggered.connect(self.abrir)

        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar.setShortcut("Ctrl+G")
        self.actionGuardar.setIcon(QtGui.QIcon(self.ruta_iconos + "\\guardar.png"))
        self.actionGuardar.triggered.connect(self.guardar)
        
        self.actionGuardar_como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_como.setObjectName("actionGuardar_como")
        self.actionGuardar_como.setShortcut("Ctrl+Shift+S")
        self.actionGuardar_como.setIcon(QtGui.QIcon(self.ruta_iconos + "\\guardar_como.png"))
        self.actionGuardar_como.triggered.connect(self.guardar_como)
        
        self.actionCerrar = QtWidgets.QAction(MainWindow)
        self.actionCerrar.setShortcut("Ctrl+Q")
        self.actionCerrar.setObjectName("actionCerrar")
        self.actionCerrar.triggered.connect(self.cerrar)
        
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionSalir.setShortcut("Alt+F4")
        self.actionSalir.triggered.connect(self.salir)

        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_como)
        self.menuArchivo.addAction(self.actionCerrar)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionSalir)
        
        #Declaracion de opciones del menu Editar
        self.actionDeshacer = QtWidgets.QAction(MainWindow)
        self.actionDeshacer.setText("Deshacer")
        self.actionDeshacer.setShortcut("Ctrl+Z")
        self.actionDeshacer.setIcon(QtGui.QIcon(self.ruta_iconos + "\\undo.png"))
        self.actionDeshacer.triggered.connect(self.deshacer)

        self.actionRehacer = QtWidgets.QAction(MainWindow)
        self.actionRehacer.setText("Rehacer")
        self.actionRehacer.setShortcut("Ctrl+Y")
        self.actionRehacer.setIcon(QtGui.QIcon(self.ruta_iconos + "\\redo.png"))
        self.actionRehacer.triggered.connect(self.hacer)

        self.actionCopiar = QtWidgets.QAction(MainWindow)
        self.actionCopiar.setText("Copiar")
        self.actionCopiar.setShortcut(QtGui.QKeySequence.Copy)
        self.actionCopiar.setIcon(QtGui.QIcon(self.ruta_iconos + "\\copiar.png"))
        self.actionCopiar.triggered.connect(self.copiar)
        
        self.actionCortar = QtWidgets.QAction(MainWindow)
        self.actionCortar.setText("Cortar")
        self.actionCortar.setShortcut(QtGui.QKeySequence.Cut)
        self.actionCortar.setIcon(QtGui.QIcon(self.ruta_iconos + "\\cortar.png"))
        self.actionCortar.triggered.connect(self.cortar)
        
        self.actionPegar = QtWidgets.QAction(MainWindow)
        self.actionPegar.setText("Pegar")
        self.actionPegar.setShortcut(QtGui.QKeySequence.Paste)
        self.actionPegar.setIcon(QtGui.QIcon(self.ruta_iconos + "\\pegar2.png"))
        self.actionPegar.triggered.connect(self.pegar)
        
        self.actionBuscar = QtWidgets.QAction(MainWindow)
        self.actionBuscar.setText("Buscar")
        self.actionBuscar.setShortcut("Ctrl+F")
        self.actionBuscar.setIcon(QtGui.QIcon(self.ruta_iconos + "\\buscar.png"))
        self.actionBuscar.triggered.connect(self.buscar)

        self.actionReemplazar = QtWidgets.QAction(MainWindow)
        self.actionReemplazar.setText("Reemplazar")
        self.actionReemplazar.setShortcut("Ctrl+H")
        self.actionReemplazar.setIcon(QtGui.QIcon(self.ruta_iconos + "\\reemplazar.png"))
        self.actionReemplazar.triggered.connect(self.reemplazar)

        self.menuEditar.addAction(self.actionDeshacer)
        self.menuEditar.addAction(self.actionRehacer)
        self.menuEditar.addSeparator()
        self.menuEditar.addAction(self.actionCopiar)
        self.menuEditar.addAction(self.actionCortar)
        self.menuEditar.addAction(self.actionPegar)
        self.menuEditar.addSeparator()
        self.menuEditar.addAction(self.actionBuscar)
        self.menuEditar.addAction(self.actionReemplazar)

        
        #Declaracion de opciones del menu Opciones
        self.actionColorFondo = QtWidgets.QAction(MainWindow)
        self.actionColorFondo.setText("Fondo")
        self.actionColorFondo.triggered.connect(self.cambiar_color_fondo)
        self.menuOpciones.addAction(self.actionColorFondo)

        '''self.actionOcularNum = QtWidgets.QAction(MainWindow)
        self.actionOcularNum.setText("Ocultar")
        self.actionOcularNum.triggered.connect(self.ocultar_num)
        self.menuOpciones.addAction(self.actionOcularNum)'''

        #Declaracion de opciones del menu Ejecutar
        self.actionEjecutarAscendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutarAscendente.setText("Ascendente")
        self.actionEjecutarAscendente.setShortcut("F5")
        self.actionEjecutarAscendente.setIcon(QtGui.QIcon(self.ruta_iconos + "\\Ascendente.png"))
        self.actionEjecutarAscendente.triggered.connect(self.ejecutar_asc)

        self.actionEjecutarDescendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutarDescendente.setText("Descendente")
        self.actionEjecutarDescendente.setShortcut("F6")
        self.actionEjecutarDescendente.setIcon(QtGui.QIcon(self.ruta_iconos + "\\Descendente.png"))
        self.actionEjecutarDescendente.triggered.connect(self.ejecutar_des)

        self.actionDebug = QtWidgets.QAction(MainWindow)
        self.actionDebug.setText("Debugger")
        self.actionDebug.setShortcut("F7")
        self.actionDebug.setIcon(QtGui.QIcon(self.ruta_iconos + "\\depurar.png"))
        self.actionDebug.triggered.connect(self.debuger)

        self.menuEjecutar.addAction(self.actionEjecutarAscendente)
        self.menuEjecutar.addAction(self.actionEjecutarDescendente)
        self.menuEjecutar.addAction(self.actionDebug)

        #Declaracion de opciones del menu Reportes
        self.actionTablaSimbolos = QtWidgets.QAction(MainWindow)
        self.actionTablaSimbolos.setText("Ver Tabla de simbolos")
        self.actionTablaSimbolos.triggered.connect(self.abrir_tabla_s)

        self.actionErrores = QtWidgets.QAction(MainWindow)
        self.actionErrores.setText("Ver Reporte de Errores")
        self.actionErrores.triggered.connect(self.abrir_reporte_err)

        self.actionAST = QtWidgets.QAction(MainWindow)
        self.actionAST.setText("Ver AST")
        self.actionAST.triggered.connect(self.abrir_AST)

        self.menuReportes.addAction(self.actionTablaSimbolos)
        self.menuReportes.addAction(self.actionErrores)
        self.menuReportes.addAction(self.actionAST)

        #Declaracion de opciones del menu ayuda
        self.actionManualUsu = QtWidgets.QAction(MainWindow)
        self.actionManualUsu.setText("Ver Manual Usuario")
        self.actionManualUsu.triggered.connect(self.ver_manual_usuario)

        self.actionManualTec = QtWidgets.QAction(MainWindow)
        self.actionManualTec.setText("Ver Manual Tecnico")
        self.actionManualTec.triggered.connect(self.ver_manual_tec)

        self.actionAcerca_de = QtWidgets.QAction(MainWindow)
        self.actionAcerca_de.setObjectName("actionAcerca_de")
        self.actionAcerca_de.triggered.connect(self.acerca_d)

        self.menuAyuda.addAction(self.actionManualUsu)
        self.menuAyuda.addAction(self.actionManualTec)
        self.menuAyuda.addAction(self.actionAcerca_de)
        
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuEjecutar.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuReportes.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.barraHerramientas1 = MainWindow.addToolBar("Archivo")
        self.barraHerramientas1.addAction(self.actionAbrir)
        self.barraHerramientas1.addAction(self.actionNuevo)
        self.barraHerramientas1.addAction(self.actionGuardar)
        self.barraHerramientas1.addAction(self.actionGuardar_como)
        
        self.barraHerramientas2 = MainWindow.addToolBar("Editar")
        self.barraHerramientas2.addAction(self.actionCopiar)
        self.barraHerramientas2.addAction(self.actionCortar)
        self.barraHerramientas2.addAction(self.actionPegar)
        self.barraHerramientas2.addAction(self.actionBuscar)
        self.barraHerramientas2.addAction(self.actionDeshacer)
        self.barraHerramientas2.addAction(self.actionRehacer)

        self.barraHerramientas3 = MainWindow.addToolBar("Ejecutar")
        self.barraHerramientas3.addAction(self.actionEjecutarAscendente)
        self.barraHerramientas3.addAction(self.actionEjecutarDescendente)
        self.barraHerramientas3.addAction(self.actionDebug)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("MainWindow", "Terminal"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))
        self.menuReportes.setTitle(_translate("MainWindow", "Reportes"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.menuEjecutar.setTitle(_translate("MainWindow", "Ejecutar"))
        self.menuOpciones.setTitle(_translate("MainWindow", "Opciones"))
        self.actionAcerca_de.setText(_translate("MainWindow", "Acerca de..."))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_como.setText(_translate("MainWindow", "Guardar como"))
        self.actionCerrar.setText(_translate("MainWindow", "Cerrar"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))

    #Acciones de los botones y menus
    def nuevo(self):
        print("selecciono nuevo")
        self.ruta_archivo = ""
        self.crear_pestania("",1)   

    def abrir(self):
        print("seleccion abrir")
        ruta = QFileDialog.getOpenFileName(MainWindow,'Abrir')
        print("La ruta dele archivos es >>>> " + ruta[0])

        if ruta[0] != "":
            try:
                self.ruta_archivo = ruta[0]
                nombre_temp = self.ruta_archivo.split("/")
                self.nombre_archivo = nombre_temp[len(nombre_temp) - 1]
                archiv = open(self.ruta_archivo, 'r')
                
                with archiv:
                    data = archiv.read()
                    self.crear_pestania(data,2)
                
                archiv.close()
            except:
                self.pop_ups_error("no se ha podido abrir el archivo")

    def guardar(self):
        print("selecciono guardar")
        try:
            temp = self.tbTab.currentIndex()

            if self.array_rutas[temp] != "":
                archiv = open(str(self.array_rutas[temp]),'w')
                self.temp2 = self.array_editores[temp]
                data = self.temp2.toPlainText()
                archiv.write(data)
                archiv.close()
            else:
                self.guardar_como()
        except:
            self.pop_ups_error("No existen pestañas para guardar")

    def guardar_como(self):
        print("selecciono guardar como")
        
        if len(self.tbTab) > 0:
            ruta = QFileDialog.getSaveFileName(MainWindow, 'Guardar Como')

            if ruta[0] != "":
                try:
                    self.ruta_archivo = ruta[0]
                    nombre_temp = self.ruta_archivo.split("/")
                    self.nombre_archivo = nombre_temp[len(nombre_temp) - 1]
                    archiv = open(self.ruta_archivo, 'w')
                    self.temp = QtWidgets.QPlainTextEdit()
                    self.temp = self.array_editores[self.tbTab.currentIndex()]
                    data = self.temp.toPlainText()
                    archiv.write(data)
                    archiv.close()
                except:
                    self.pop_ups_error("No se ha podido abrir el archivo")

        else:
            self.pop_ups_error("No exiten pestañas para guardar")

    def cerrar(self):
        print("selecciono cerrar")
        print(self.ruta_iconos + "\\favicon.png")

    def salir(self):
        print("selecciono salir")
        sys.exit()

    def copiar(self):
        print("copiar")
        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            self.temp.copy
        else:
            self.pop_ups_error("No exiten pestañas")        

    def cortar(self):
        print("cortar")
        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            self.temp.cut
        else:
            self.pop_ups_error("No exiten pestañas")

    def pegar(self):
        print("pegar")
        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            self.temp.paste
        else:
            self.pop_ups_error("No exiten pestañas")

    def deshacer(self):
        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            self.temp.undo
        else:
            self.pop_ups_error("No exiten pestañas")

    def hacer(self):       
        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            self.temp.redo
        else:
            self.pop_ups_error("No exiten pestañas")

    def buscar(self):
        print("buscar")

    def reemplazar(self):
        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            texto = self.temp.toPlainText()
            
            palabra_a_buscar, resultado1 = QtWidgets.QInputDialog.getText(MainWindow, 'Buscar', 'Ingrese palabra a buscar:', QtWidgets.QLineEdit.Normal, "")
            palabra_a_reemplazar, resultado2 = QtWidgets.QInputDialog.getText(MainWindow, "Reemplazar", "Ingrese el reemplazo:")

            if resultado1 == True & resultado2 == True:
                texto_nuevo = texto.replace(str(palabra_a_buscar), str(palabra_a_reemplazar))
                self.temp.setPlainText(texto_nuevo)

        else:
            self.pop_ups_error("No exiten pestañas")

    def cambiar_color_fondo(self):

        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            color = QtWidgets.QColorDialog.getColor()
            if not color.isValid():
                self.pop_ups_error("No exiten pestañas")
                return
            self.temp.setStyleSheet("QPlainTextEdit {background-color: %s}" % color.name())
        else:
            self.pop_ups_error("No exiten pestañas")
            
    def crear_pestania(self, texto, opcion):
        nombre_pestaña = ""
        if opcion == 1:
            nombre_pestaña = "Documento " + str(len(self.tbTab) + 1)
        else:
            nombre_pestaña = self.nombre_archivo
        
        self.array_nombre_tab = nombre_pestaña
        self.tab = QtWidgets.QWidget()
        self.txtTab = Editor_Codigo.QCodeEditor(self.tab)
        self.txtTab.setGeometry(QtCore.QRect(0, 0, 764, 464))
        self.txtTab.setPlainText(texto)
        self.txtTab.setFont(self.Fuente2)
        self.array_editores.append(self.txtTab)
        self.array_rutas.append(self.ruta_archivo)
        
        self.tbTab.addTab(self.tab, nombre_pestaña)

    def pop_ups_error(self, mensaje):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error!")
        msg.setText(str(mensaje))
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        x = msg.exec_()

    def ejecutar_asc(self):
        if len(self.tbTab) > 0:
            self.indice = -1
            Lista_errores.clear()
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            instrucciones = minic.parse(self.temp.toPlainText())
            print("todo bien");
            if len(Lista_errores) < 1:
                translate = traducir(instrucciones)
                resultado = translate.inizializar_tablas()
                if resultado != False:
                    print("todo bien 2")
                    resultado = translate.verificar_tipos()
                    if resultado != False:
                        print("todo bien 3")
                        codigo_aug = translate.comenzar_traduccion()
                        self.crear_pestania(codigo_aug,1)
                        print(codigo_aug)
            '''instrucciones = p.parse(self.temp.toPlainText())
            self.tabla_global = tabla.Tabla_Simbolos()
            self.tabla_global.clear()

            try:
                if len(Lista_errores) < 1:
                    self.txtConsola.setPlainText("--------------Ejecutando Ascendente--------------\n")
                    Ejec1.iniciar_ejecucion(instrucciones, self.tabla_global, self.txtConsola, MainWindow)
                    ast = AST()
                    ast.iniciar_ejecucion(instrucciones)
                    reporte = Reporte_AST.Reporte_AST()
                    reporte.crear_reporte(ast.raiz)
                else:
                    reporte = Reporte_Errores.Reporte_Errores()
                    reporte.crear_reporte(Lista_errores)
                    self.txtConsola.setPlainText(
                    self.txtConsola.toPlainText() + "No se pudo ejecutar el codigo debido a errores lexicos o sintacticos \n")

            except:
                print("Problemas en la ejecucion")
                self.txtConsola.setPlainText(self.txtConsola.toPlainText() + "Problemas en la ejecucion \n")'''

        else:
            self.pop_ups_error("No exiten pestañas")

    def ejecutar_des(self):
        if len(self.tbTab) > 0:
            self.indice = -1
            Lista_errores.clear()
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            instrucciones = asc.parse(self.temp.toPlainText())
            self.tabla_global = tabla.Tabla_Simbolos()
            self.tabla_global.clear()

            try:
                if len(Lista_errores) < 1:
                    self.txtConsola.setPlainText("--------------Ejecutando Descendente--------------\n")
                    Ejec1.iniciar_ejecucion(instrucciones, self.tabla_global, self.txtConsola, MainWindow)
                    ast = AST()
                    ast.iniciar_ejecucion(instrucciones)
                    reporte = Reporte_AST.Reporte_AST()
                    reporte.crear_reporte(ast.raiz)
                else:
                    reporte = Reporte_Errores.Reporte_Errores()
                    reporte.crear_reporte(Lista_errores)
                    self.txtConsola.setPlainText(
                    self.txtConsola.toPlainText() + "No se pudo ejecutar el codigo debido a errores lexicos o sintacticos \n")

            except:
                print("Problemas en la ejecucion")
                self.txtConsola.setPlainText(self.txtConsola.toPlainText() + "Problemas en la ejecucion \n")

        else:
            self.pop_ups_error("No exiten pestañas")

    def debuger(self):
        if len(self.tbTab) > 0:
            self.temp = self.array_editores[self.tbTab.currentIndex()]
            texto = self.temp.toPlainText()
            Lista_errores.clear()
            instrucciones = p.parse(texto)
            if self.indice < 0:
                self.tabla_global = tabla.Tabla_Simbolos()
                self.tabla_global.clear()

            try:
                if len(Lista_errores) < 1:
                    self.indice = Ejec1.iniciar_debbug(texto,self.indice, instrucciones, self.tabla_global, self.txtConsola, MainWindow)
                    ast = AST()
                    ast.iniciar_ejecucion(instrucciones)
                    reporte = Reporte_AST.Reporte_AST()
                    reporte.crear_reporte(ast.raiz)
                    self.abrir_tabla_s()
                else:
                    reporte = Reporte_Errores.Reporte_Errores()
                    reporte.crear_reporte(Lista_errores)
                    self.txtConsola.setPlainText(
                        self.txtConsola.toPlainText() + "No se pudo ejecutar el codigo debido a errores lexicos o sintacticos \n")

            except:
                print("Problemas en la ejecucion")
                self.txtConsola.setPlainText(self.txtConsola.toPlainText() + "Problemas en la ejecucion \n")
        else:
            self.pop_ups_error("No exiten pestañas")

    def abrir_tabla_s(self):
        reporte = Reporte_Tabla_Simbolos.Reporte_Simbolos()
        reporte.crear_reporte(self.tabla_global)
        escena = QtWidgets.QGraphicsScene()
        map = QtGui.QPixmap("Reportes/Reporte_Tabla_Simbolos.png")
        escena.addPixmap(map)
        self.visor.setScene(escena)

    def abrir_reporte_err(self):
        reporte = Reporte_Errores.Reporte_Errores()
        reporte.crear_reporte(Lista_errores)
        escena = QtWidgets.QGraphicsScene()
        map = QtGui.QPixmap("Reportes/Reporte_Error.png")
        escena.addPixmap(map)
        self.visor.setScene(escena)

    def abrir_AST(self):
        escena = QtWidgets.QGraphicsScene()
        map = QtGui.QPixmap("Reportes/Reporte_AST.png")
        escena.addPixmap(map)
        self.visor.setScene(escena)

    def acerca_d(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("<b>Acerca De Augus<\b>")
        self.msg.setInformativeText("Es código intermedio para fines académicos. Específicamente para ser utilizado "
                                    "en el curso de Compiladores 2​ de la Universidad de San Carlos de Guatemala.\n"
                                    "Desarrollado por: Luis Alfonso Ordoñez ")
        self.msg.setWindowTitle("Acerca De Augus 3APHP")
        self.msg.exec_()

    def ver_manual_usuario(self):
        coso =str(os.getcwd()) +  "\Manuales\Manual_usuario.pdf"
        os.startfile(coso)

    def ver_manual_tec(self):
        coso = str(os.getcwd()) + "\Manuales\Manual_tecnico.pdf"
        os.startfile(coso)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
