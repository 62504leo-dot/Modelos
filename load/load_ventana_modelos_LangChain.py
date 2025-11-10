# Contenido COMPLETO para: load/load_ventana_modelos_LangChain.py
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class LoadVentanaLangChain(QtWidgets.QDialog):
    
    # --- PASO 1: El init ACEPTA los 8 motores ---
    # (No pasa nada si los 7 últimos son "None")
    def __init__(self, 
                 chain_1, chain_2, chain_3, chain_4, 
                 chain_5, chain_6, chain_7, chain_8, 
                 parent=None):
        
        super().__init__(parent)
        uic.loadUi("interfaces/ventana_modelos_LangChain.ui", self)
        
        # --- PASO 2: Guardamos los motores ---
        self.chain_1 = chain_1
        self.chain_2 = chain_2
        self.chain_3 = chain_3
        self.chain_4 = chain_4
        self.chain_5 = chain_5
        self.chain_6 = chain_6
        self.chain_7 = chain_7
        self.chain_8 = chain_8
        
        # --- Lógica de la ventana (sin bordes, cerrar, etc.) ---
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.boton_salir.clicked.connect(self.close)
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        
        # --- Lógica del menú lateral ---
        self.boton_menu.clicked.connect(self.mover_menu)
        self.ancho_menu_visible = 200 # Ancho del frame_lateral
        self.frame_lateral.setMaximumWidth(0) # Inicia oculto

        # --- PASO 3: Conectar botones de NAVEGACIÓN (laterales) ---
        self.btn_lc_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_1))
        self.btn_lc_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_2))
        self.btn_lc_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_3))
        self.btn_lc_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_4))
        self.btn_lc_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_5))
        self.btn_lc_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_6))
        self.btn_lc_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_7))
        self.btn_lc_8.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_8))
        
        # --- PASO 4: Conectar botones de "ENVIAR" ---
        self.btn_enviar_lc_1.clicked.connect(self.logica_enviar_lc_1)
        self.btn_enviar_lc_2.clicked.connect(self.logica_enviar_lc_2)
        self.btn_enviar_lc_3.clicked.connect(self.logica_enviar_lc_3)
        self.btn_enviar_lc_4.clicked.connect(self.logica_enviar_lc_4)
        self.btn_enviar_lc_5.clicked.connect(self.logica_enviar_lc_5)
        self.btn_enviar_lc_6.clicked.connect(self.logica_enviar_lc_6)
        self.btn_enviar_lc_7.clicked.connect(self.logica_enviar_lc_7)
        self.btn_enviar_lc_8.clicked.connect(self.logica_enviar_lc_8)

    # --- Funciones de Lógica (Slots para "Enviar") ---

    def logica_enviar_lc_1(self):
        # El único que funciona por ahora
        if not self.chain_1:
            self.output_lc_1.setText("Error: El motor 1 no fue cargado.")
            return
            
        texto_usuario = self.input_lc_1.text()
        if not texto_usuario:
            self.output_lc_1.setText("Por favor, escribe un tema.")
            return
            
        self.output_lc_1.setText("Procesando...")
        try:
            # Tu chain_1 espera la variable "tema"
            respuesta = self.chain_1.invoke({"tema": texto_usuario})
            self.output_lc_1.setText(respuesta.content) 
        except Exception as e:
            self.output_lc_1.setText(f"Error en LangChain: {e}")

    # --- Lógica para los 7 motores PENDIENTES ---
    # (Solo muestran un error amigable)

    def logica_enviar_lc_2(self):
        if not self.chain_2:
            self.output_lc_2.setText("Motor 2 (SequentialChain) no implementado.")
            return
        # Aquí iría la lógica del motor 2...
        
    def logica_enviar_lc_3(self):
        if not self.chain_3:
            self.output_lc_3.setText("Motor 3 (SimpleSequential) no implementado.")
            return
        
    def logica_enviar_lc_4(self):
        if not self.chain_4:
            self.output_lc_4.setText("Motor 4 (Parseo) no implementado.")
            return

    def logica_enviar_lc_5(self):
        if not self.chain_5:
            self.output_lc_5.setText("Motor 5 (Varios Pasos) no implementado.")
            return

    def logica_enviar_lc_6(self):
        if not self.chain_6:
            self.output_lc_6.setText("Motor 6 (Memoria) no implementado.")
            return

    def logica_enviar_lc_7(self):
        if not self.chain_7:
            self.output_lc_7.setText("Motor 7 (Persistencia) no implementado.")
            return

    def logica_enviar_lc_8(self):
        if not self.chain_8:
            self.output_lc_8.setText("Motor 8 (RAG) no implementado.")
            return

    # --- Funciones para mover ventana y menú ---

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        
    def mover_ventana(self, event):
        if self.isMaximized() == False:     
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
    
    def mover_menu(self):
        width = self.frame_lateral.maximumWidth() # Usar maximumWidth
        
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