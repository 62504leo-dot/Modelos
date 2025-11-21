# Contenido COMPLETO para: load/load_ventana_principal.py
from PyQt5 import QtWidgets, uic

# --- Importamos las clases de las VENTANAS ---
from .load_ventana_modelos_basicos import Load_ventana_modelos_basicos
from .load_ventana_modelos_LangChain import LoadVentanaLangChain

# --- Importamos los "MOTORES BÁSICOS" ---
from main import crear_modelo_simple
from main_historial import crear_modelo_historial
from main_memoria import crear_modelo_chat_limitado

# --- Importamos los "MOTORES LANGCHAIN" ---
# Motor 1: Básico
from lc_1_llmchain import crear_chain_llmchain 
# Motor 2: Secuencial (¡NUEVO!)
from lc_2_sequientialchain import crear_chain_secuencial 

from lc_3_simplesequientialchain import crear_chain_simple_secuencial

class Load_ventana_principal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaces/ventana_principal.ui", self)
        self.showMaximized()

        print("Cargando modelos... (Esto puede tardar un momento)")
        
        # --- 1. Cargamos los motores BÁSICOS ---
        try:
            self.modelo_simple_cargado = crear_modelo_simple()
            self.modelo_historial_cargado = crear_modelo_historial()
            self.modelo_chat_cargado = crear_modelo_chat_limitado()
        except Exception as e:
            print(f"Error cargando básicos: {e}")
        
        # --- 2. Cargamos los motores LANGCHAIN ---
        try:
            self.lc_chain_1 = crear_chain_llmchain()      # Motor 1
            self.lc_chain_2 = crear_chain_secuencial()    # Motor 2 (¡Agregado!)
            self.lc_chain_3 = crear_chain_simple_secuencial()   
        except Exception as e:
            print(f"Error cargando LangChain: {e}")
            self.lc_chain_1 = None
            self.lc_chain_2 = None
            self.lc_chain_3= None

        print("¡Modelos cargados y listos!")

        # Conectamos las acciones del menú
        self.actionBasicos.triggered.connect(self.abrirVentanaBasico)
        self.actionLangChain.triggered.connect(self.abrirVentanaLangchain)
        self.actionSalir.triggered.connect(self.cerrarVentana)
    
    def abrirVentanaBasico(self):
        self.basicos = Load_ventana_modelos_basicos(
            modelo_simple=self.modelo_simple_cargado,
            modelo_memoria=self.modelo_historial_cargado,
            modelo_chat=self.modelo_chat_cargado
        )
        self.basicos.exec_()
    
    
    def abrirVentanaLangchain(self):
        # Aquí pasamos los motores a la ventana
        self.LangChain = LoadVentanaLangChain(
            chain_1=self.lc_chain_1, 
            chain_2=self.lc_chain_2, # <--- ¡AQUÍ CONECTAMOS EL MOTOR 2!
            chain_3=self.lc_chain_3,
            chain_4=None,
            chain_5=None,
            chain_6=None,
            chain_7=None,
            chain_8=None
        )
        self.LangChain.exec_()

    def cerrarVentana(self):
        self.close()