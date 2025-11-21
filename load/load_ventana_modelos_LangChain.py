from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class LoadVentanaLangChain(QtWidgets.QDialog):
    
    def __init__(self, 
                 chain_1, chain_2, chain_3, chain_4, 
                 chain_5, chain_6, chain_7, chain_8, 
                 parent=None):
        
        super().__init__(parent)
        # Asegúrate de que este nombre coincida con tu archivo .ui real
        uic.loadUi("interfaces/ventana_modelos_LangChain.ui", self)
        
        # Guardamos los motores
        self.chain_1 = chain_1
        self.chain_2 = chain_2
        self.chain_3 = chain_3
        self.chain_4 = chain_4
        self.chain_5 = chain_5
        self.chain_6 = chain_6
        self.chain_7 = chain_7
        self.chain_8 = chain_8
        
        # --- CONFIGURACIÓN DE LA VENTANA ---
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        # Botón Salir
        self.boton_salir.clicked.connect(self.close)
        
        # Mover ventana con el mouse
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        
        # --- CORRECCIÓN DEL MENÚ LATERAL ---
        self.boton_menu.clicked.connect(self.mover_menu)
        self.ancho_menu_visible = 200 
        self.frame_lateral.setMinimumWidth(0)
        self.frame_lateral.setMaximumWidth(0) 

        # --- BOTONES DE NAVEGACIÓN (Páginas) ---
        self.btn_lc_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_1))
        self.btn_lc_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_2))
        self.btn_lc_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_3))
        self.btn_lc_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_4))
        self.btn_lc_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_5))
        self.btn_lc_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_6))
        self.btn_lc_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_7))
        self.btn_lc_8.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_8))
        
        # --- BOTONES DE ENVIAR (Conexiones Lógicas) ---
        self.btn_enviar_lc_1.clicked.connect(self.logica_enviar_lc_1)
        self.btn_enviar_lc_2.clicked.connect(self.logica_enviar_lc_2)
        
        # ¡¡AQUÍ ESTABA EL ERROR!! Faltaba esta línea:
        self.btn_enviar_lc_3.clicked.connect(self.logica_enviar_lc_3)

    # --- LOGICA ANIMACIÓN MENÚ ---
    def mover_menu(self):
        width = self.frame_lateral.maximumWidth()
        if width == 0:
            extender = self.ancho_menu_visible
            self.boton_menu.setText("Ocultar")
        else:
            extender = 0
            self.boton_menu.setText("Menú")
            
        self.animacion = QtCore.QPropertyAnimation(self.frame_lateral, b'maximumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()

    # --- LOGICA MOVER VENTANA ---
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        
    def mover_ventana(self, event):
        if self.isMaximized() == False:     
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

    # ==========================================
    #           LÓGICA DE LOS MOTORES
    # ==========================================

    # --- MOTOR 1: Básico ---
    def logica_enviar_lc_1(self):
        if not self.chain_1:
            self.output_lc_1.setText("Error: Motor 1 no cargado.")
            return
            
        ctx = self.input_contexto_lc_1.text()
        tema = self.input_lc_1.text()
        
        if not ctx or not tema:
            self.output_lc_1.setText("Llena ambos campos.")
            return
            
        self.output_lc_1.setText("Procesando...")
        self.output_lc_1.repaint()
        
        try:
            diccionario = {"contexto": ctx, "tema": tema}
            respuesta = self.chain_1.invoke(diccionario)
            self.output_lc_1.setText(respuesta.content) 
        except Exception as e:
            self.output_lc_1.setText(f"Error: {e}")

    # --- MOTOR 2: Traductor Secuencial ---
    def logica_enviar_lc_2(self):
        if not self.chain_2:
            self.output_lc_2.setText("Error: Motor 2 no cargado.")
            return
        
        idioma = self.input_idioma_lc_2.text()
        texto = self.input_lc_2.text()
        
        if not idioma or not texto:
            self.output_lc_2.setText("Llena ambos campos.")
            return
            
        self.output_lc_2.setText(f"Resumiendo y traduciendo al {idioma}...")
        self.output_lc_2.repaint()
        
        try:
            datos = {"texto_original": texto, "idioma_destino": idioma}
            respuesta = self.chain_2.invoke(datos)
            self.output_lc_2.setText(f"RESUMEN EN {idioma.upper()}:\n\n{respuesta}")
        except Exception as e:
            self.output_lc_2.setText(f"Error: {e}")

    # --- MOTOR 3: Cadena Dinámica (2 Pasos) ---
    def logica_enviar_lc_3(self):
        if not self.chain_3:
            self.output_lc_3.setText("Error: Motor 3 no cargado.")
            return
        
        # Obtener los textos
        orden1 = self.input_instruccion_1_lc_3.text()
        orden2 = self.input_instruccion_2_lc_3.text()
        tema = self.input_lc_3.text()
        
        # Validar
        if not orden1 or not orden2 or not tema:
            self.output_lc_3.setText("Por favor, llena los 3 campos.")
            return
            
        self.output_lc_3.setText(f"Ejecutando:\n1. {orden1}\n2. {orden2}...")
        self.output_lc_3.repaint()
        
        try:
            datos = {
                "instruccion_1": orden1,
                "instruccion_2": orden2,
                "input": tema
            }
            # Invocamos
            respuesta = self.chain_3.invoke(datos)
            self.output_lc_3.setText(f"RESULTADO FINAL:\n\n{respuesta}")
            
        except Exception as e:
            self.output_lc_3.setText(f"Error: {e}")