# Archivo: load/load_ventana_modelos_LangChain.py
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class LoadVentanaLangChain(QtWidgets.QDialog):
    
    def __init__(self, 
                 chain_1, chain_2, chain_3, chain_4, 
                 chain_5, chain_6, chain_7, chain_8, 
                 parent=None):
        
        super().__init__(parent)
        # Cargamos la interfaz visual
        uic.loadUi("interfaces/ventana_modelos_LangChain.ui", self)
        
        # Guardamos los modelos que recibimos del main
        self.chain_1 = chain_1
        self.chain_2 = chain_2
        self.chain_3 = chain_3
        self.chain_4 = chain_4 # <--- Este es el resumidor
        self.chain_5 = chain_5
        self.chain_6 = chain_6
        self.chain_7 = chain_7
        self.chain_8 = chain_8
        
        # --- CONFIGURACIÓN VISUAL DE LA VENTANA ---
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        # Botón Salir y Mover Ventana
        self.boton_salir.clicked.connect(self.close)
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        
        # Menú Lateral Animado
        self.boton_menu.clicked.connect(self.mover_menu)
        self.ancho_menu_visible = 200 
        self.frame_lateral.setMinimumWidth(0)
        self.frame_lateral.setMaximumWidth(0) 

        # --- BOTONES DE NAVEGACIÓN (Cambiar de Página) ---
        self.btn_lc_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_1))
        self.btn_lc_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_2))
        self.btn_lc_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_3))
        self.btn_lc_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_4))
        self.btn_lc_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_5))
        self.btn_lc_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_6))
        self.btn_lc_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_7))
        self.btn_lc_8.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_lc_8))
        
        # --- CONEXIÓN DE BOTONES DE ENVIAR (AQUÍ ESTABA LA FALLA) ---
        self.btn_enviar_lc_1.clicked.connect(self.logica_enviar_lc_1)
        self.btn_enviar_lc_2.clicked.connect(self.logica_enviar_lc_2)
        self.btn_enviar_lc_3.clicked.connect(self.logica_enviar_lc_3)
        self.btn_enviar_lc_4.clicked.connect(self.logica_enviar_lc_4)
        self.btn_enviar_lc_5.clicked.connect(self.logica_enviar_lc_5)
        self.btn_enviar_lc_6.clicked.connect(self.logica_enviar_lc_6)
        self.btn_enviar_lc_7.clicked.connect(self.logica_enviar_lc_7)
        self.btn_enviar_lc_8.clicked.connect(self.logica_enviar_lc_8)
    # ==========================================
    #           LÓGICA VISUAL
    # ==========================================
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

    # MOTOR 1: Básico
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

    # MOTOR 2: Secuencial
    def logica_enviar_lc_2(self):
        if not self.chain_2:
            self.output_lc_2.setText("Error: Motor 2 no cargado.")
            return
        idioma = self.input_idioma_lc_2.text()
        texto = self.input_lc_2.text()
        if not idioma or not texto:
            self.output_lc_2.setText("Llena ambos campos.")
            return
        self.output_lc_2.setText("Procesando...")
        self.output_lc_2.repaint()
        try:
            datos = {"texto_original": texto, "idioma_destino": idioma}
            respuesta = self.chain_2.invoke(datos)
            self.output_lc_2.setText(f"RESUMEN ({idioma.upper()}):\n\n{respuesta}")
        except Exception as e:
            self.output_lc_2.setText(f"Error: {e}")

    # MOTOR 3: Dinámico 3 Pasos
    def logica_enviar_lc_3(self):
        if not self.chain_3:
            self.output_lc_3.setText("Error: Motor 3 no cargado.")
            return
        orden1 = self.input_instruccion_1_lc_3.text()
        orden2 = self.input_instruccion_2_lc_3.text()
        tema = self.input_lc_3.text()
        if not orden1 or not orden2 or not tema:
            self.output_lc_3.setText("Llena los 3 campos.")
            return
        self.output_lc_3.setText("Ejecutando secuencia...")
        self.output_lc_3.repaint()
        try:
            datos = {"instruccion_1": orden1, "instruccion_2": orden2, "input": tema}
            respuesta = self.chain_3.invoke(datos)
            self.output_lc_3.setText(f"RESULTADO:\n\n{respuesta}")
        except Exception as e:
            self.output_lc_3.setText(f"Error: {e}")

    # MOTOR 4: RESUMIDOR (Tu código original)
    def logica_enviar_lc_4(self):
        # 1. Validar que el motor existe
        if not self.chain_4:
            self.output_lc_4.setText("Error: El Motor 4 no se cargó correctamente en main.")
            return
        
        # 2. Obtener texto de la ÚNICA caja
        # Asegúrate que en tu XML la caja se llame 'input_lc_4'
        texto_usuario = self.input_lc_4.text()
        
        if not texto_usuario:
            self.output_lc_4.setText("Por favor, pega un texto largo para resumir.")
            return
            
        self.output_lc_4.setText("Generando resumen conciso...")
        self.output_lc_4.repaint()
        
        try:
            # 3. Invocar
            # Usamos "input" porque así lo definimos en el prompt de lc_4_parseo.py
            diccionario = {"input": texto_usuario}
            
            respuesta = self.chain_4.invoke(diccionario)
            
            # Como usamos StrOutputParser, respuesta ya es texto limpio
            self.output_lc_4.setText(f"RESUMEN GENERADO:\n\n{respuesta}")
            
        except Exception as e:
            self.output_lc_4.setText(f"Error al ejecutar: {e}")
            
    def logica_enviar_lc_5(self):
        if not self.chain_5:
            self.output_lc_5.setText("Error: Motor 5 no cargado.")
            return
        
        texto = self.input_lc_5.text()
        
        if not texto:
            self.output_lc_5.setText("Ingresa un texto.")
            return
            
        self.output_lc_5.setText("Procesando (Resumiendo -> Traduciendo)...")
        self.output_lc_5.repaint()
        
        try:
            # El prompt inicial espera {input}
            diccionario = {"input": texto}
            
            respuesta = self.chain_5.invoke(diccionario)
            
            self.output_lc_5.setText(f"RESULTADO FINAL:\n\n{respuesta}")
            
        except Exception as e:
            self.output_lc_5.setText(f"Error: {e}")
            
    # MOTOR 6: Chat con Memoria
    def logica_enviar_lc_6(self):
        # Validar
        if not self.chain_6:
            self.output_lc_6.append("Error: Sistema de memoria no cargado.")
            return
        
        texto_usuario = self.input_lc_6.text()
        if not texto_usuario:
            return # No hacemos nada si está vacío
            
        # 1. Mostrar mensaje del usuario en la pantalla grande
        self.output_lc_6.append(f"<b>Tú:</b> {texto_usuario}")
        self.input_lc_6.clear() # Limpiar caja pequeña
        self.output_lc_6.repaint()
        
        try:
            # 2. Invocar función con memoria
            # self.chain_6 es la función 'ejecutar_con_memoria'
            respuesta_ia = self.chain_6(texto_usuario)
            
            # 3. Mostrar respuesta de la IA
            self.output_lc_6.append(f"<b>IA:</b> {respuesta_ia}")
            self.output_lc_6.append("-" * 30) # Separador visual
            
            # Auto-scroll hacia abajo
            cursor = self.output_lc_6.textCursor()
            cursor.movePosition(cursor.End)
            self.output_lc_6.setTextCursor(cursor)
            
        except Exception as e:
            self.output_lc_6.append(f"<i>Error: {e}</i>")
    # MOTOR 7: Persistencia (JSON)
    def logica_enviar_lc_7(self):
        if not self.chain_7:
            self.output_lc_7.append("Error: Motor 7 no cargado.")
            return
        
        texto_usuario = self.input_lc_7.text()
        if not texto_usuario:
            return
            
        # 1. Mostrar lo que escribiste
        self.output_lc_7.append(f"<b>Tú:</b> {texto_usuario}")
        self.input_lc_7.clear()
        self.output_lc_7.repaint()
        
        try:
            # 2. Ejecutar (Esto guardará en 'memoria.json' automáticamente)
            respuesta_ia = self.chain_7(texto_usuario)
            
            # 3. Mostrar respuesta
            self.output_lc_7.append(f"<b>IA (Persistente):</b> {respuesta_ia}")
            self.output_lc_7.append("-" * 30)
            
            # Auto-scroll
            cursor = self.output_lc_7.textCursor()
            cursor.movePosition(cursor.End)
            self.output_lc_7.setTextCursor(cursor)
            
        except Exception as e:
            self.output_lc_7.append(f"Error: {e}")
    
    # MOTOR 8: RAG (PDF)
    def logica_enviar_lc_8(self):
        if not self.chain_8:
            self.output_lc_8.setText("Error: Motor RAG no cargado.\n\nVerifica:\n1. Tener carpeta 'documentos/fuente.pdf'\n2. Librerías instaladas (faiss-cpu, sentence-transformers).")
            return
        
        pregunta = self.input_lc_8.text()
        if not pregunta:
            return
            
        self.output_lc_8.setText("Buscando en el documento y generando respuesta...")
        self.output_lc_8.repaint()
        
        try:
            # En RAG Simple, invocamos directo con el string de la pregunta
            respuesta = self.chain_8.invoke(pregunta)
            
            self.output_lc_8.setText(f"RESPUESTA DEL DOCUMENTO:\n\n{respuesta}")
            
        except Exception as e:
            self.output_lc_8.setText(f"Error: {e}")