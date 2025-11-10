from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QMessageBox  


class Load_ventana_modelos_basicos(QtWidgets.QDialog):

    def __init__(self, modelo_simple, modelo_memoria, modelo_chat, parent=None):
        super().__init__(parent)
        uic.loadUi("interfaces/ventana_modelos_basicos.ui", self)

        self.modelo_simple = modelo_simple
        self.modelo_memoria = modelo_memoria
        self.modelo_chat = modelo_chat

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.boton_cerrar.clicked.connect(lambda: self.close())
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.boton_menu.clicked.connect(self.mover_menu)

        self.pushButton.clicked.connect(self.mostrar_pagina_prompt)
        self.pushButton_2.clicked.connect(self.mostrar_pagina_memoria)
        self.pushButton_3.clicked.connect(self.mostrar_pagina_chat)

        self.boton_enviar.clicked.connect(self.logica_enviar_prompt)
        self.boton_enviar_2.clicked.connect(self.logica_enviar_memoria)
        self.boton_enviar_3.clicked.connect(self.logica_enviar_chat)

       
        self.contador_chat = 0
        self.limite_chat = 5

    
    def mostrar_pagina_prompt(self):
        self.stackedWidget.setCurrentWidget(self.page_prompt)

    def mostrar_pagina_memoria(self):
        self.stackedWidget.setCurrentWidget(self.page_memoria)

    def mostrar_pagina_chat(self):
        self.stackedWidget.setCurrentWidget(self.page_chat)

    
    def logica_enviar_prompt(self):
        texto_usuario = self.input_prompt.text()
        if not texto_usuario.strip():
            return
        respuesta_modelo = self.modelo_simple.invoke({"input": texto_usuario})
        self.output_response.setText(respuesta_modelo)
        self.input_prompt.clear()

    def logica_enviar_memoria(self):
        texto_usuario = self.input_prompt_2.text()
        if not texto_usuario.strip():
            return
        respuesta_dict = self.modelo_memoria.invoke({"input": texto_usuario})
        respuesta_modelo = respuesta_dict.get('response', 'Error al obtener respuesta')
        self.output_response_2.append(f"Usuario: {texto_usuario}\n")
        self.output_response_2.append(f"Modelo: {respuesta_modelo}\n")
        self.input_prompt_2.clear()

    
    def logica_enviar_chat(self):
        texto_usuario = self.input_prompt_3.text().strip()
        if not texto_usuario:
            return

        
        if self.contador_chat >= self.limite_chat:
            QMessageBox.warning(
                self,
                "Límite alcanzado",
                f"Ya realizaste {self.limite_chat} preguntas.\nNo puedes seguir enviando mensajes."
            )
            self.boton_enviar_3.setEnabled(False)
            self.input_prompt_3.setEnabled(False)
            return

        # Mostrar mensaje del usuario
        self.output_response_3.append(f"Tú: {texto_usuario}\n")

        try:
            respuesta_dict = self.modelo_chat.invoke({"input": texto_usuario})
            respuesta_modelo = respuesta_dict.get('response', 'Error al obtener respuesta')
        except Exception as e:
            respuesta_modelo = f"Error en el modelo: {e}"

        self.output_response_3.append(f"IA: {respuesta_modelo}\n")
        self.input_prompt_3.clear()

        
        self.contador_chat += 1

        
        if self.contador_chat >= self.limite_chat:
            self.boton_enviar_3.setEnabled(False)
            self.input_prompt_3.setEnabled(False)
            QMessageBox.information(
                self,
                "Fin del chat",
                f"Has llegado al límite de {self.limite_chat} preguntas.\n"
                "El chat ha sido bloqueado."
            )

    
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

    
    def mover_menu(self):
        width = self.frame_lateral.width()
        if width == 0:
            extender = 200
            self.boton_menu.setText("Menú")
        else:
            extender = 0
            self.boton_menu.setText("")

        self.animacion = QtCore.QPropertyAnimation(self.frame_lateral, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()