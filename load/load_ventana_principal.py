# Archivo: load/load_ventana_principal.py
from PyQt5 import QtWidgets, uic

# 1. Importar ventanas secundarias
from .load_ventana_modelos_basicos import Load_ventana_modelos_basicos
from .load_ventana_modelos_LangChain import LoadVentanaLangChain

# 2. Importar lógica de modelos básicos
# (Asegúrate de que main.py, main_historial.py, etc. existan y funcionen)
try:
    from main import crear_modelo_simple
    from main_historial import crear_modelo_historial
    from main_memoria import crear_modelo_chat_limitado
except ImportError as e:
    print(f"Advertencia: No se pudieron importar modelos básicos: {e}")

# 3. Importar lógica de LangChain
# (Asegúrate de que estos archivos existan en la carpeta principal)
try:
    from lc_1_llmchain import crear_chain_llmchain 
    from lc_2_sequientialchain import crear_chain_secuencial 
    from lc_3_simplesequientialchain import crear_chain_simple_secuencial
    from lc_4_parseo import crear_chain_parser
    from lc_5_varios_pasos import crear_chain_varios_pasos
    from lc_6_memoria import ejecutar_con_memoria
    from lc_7_persistencia import ejecutar_con_persistencia
    from lc_8_rag import crear_chain_rag
except ImportError as e:
    
    print(f"Advertencia: No se pudieron importar modelos LangChain: {e}")


class Load_ventana_principal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el UI
        try:
            uic.loadUi("interfaces/ventana_principal.ui", self)
        except Exception as e:
            print(f"Error cargando UI principal: {e}")
            return

        self.showMaximized()
        print("Cargando modelos...")
        
        # --- INICIALIZAR MODELOS BÁSICOS ---
        self.modelo_simple_cargado = None
        self.modelo_historial_cargado = None
        self.modelo_chat_cargado = None
        
        try:
            self.modelo_simple_cargado = crear_modelo_simple()
            self.modelo_historial_cargado = crear_modelo_historial()
            self.modelo_chat_cargado = crear_modelo_chat_limitado()
           
        except Exception as e:
            print(f"Error inicializando básicos: {e}")

        # --- INICIALIZAR MODELOS LANGCHAIN ---
        self.lc_chain_1 = None
        self.lc_chain_2 = None
        self.lc_chain_3 = None
        self.lc_chain_4 = None
        self.lc_chain_5 = None
        self.lc_chain_6 = None
        self.lc_chain_7= None
        self.lc_chain_8= None
        try:
            self.lc_chain_1 = crear_chain_llmchain()
            self.lc_chain_2 = crear_chain_secuencial()
            self.lc_chain_3 = crear_chain_simple_secuencial()
            self.lc_chain_4 = crear_chain_parser()
            self.lc_chain_5 = crear_chain_varios_pasos()
            self.lc_chain_6= ejecutar_con_memoria
            self.lc_chain_7 = ejecutar_con_persistencia
            self.lc_chain_8 = crear_chain_rag()
         
        except Exception as e:
            print(f"Error inicializando LangChain (Verifica tus archivos lc_*.py): {e}")

        print("¡Sistema listo!")

        # Conectar Botones del Menú
        # (Asegúrate de que estos nombres coincidan con tu ventana_principal.ui)
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
        self.LangChain = LoadVentanaLangChain(
            chain_1=self.lc_chain_1, 
            chain_2=self.lc_chain_2,
            chain_3=self.lc_chain_3,
            chain_4=self.lc_chain_4,
            chain_5=self.lc_chain_5,
            chain_6=self.lc_chain_6,
            chain_7=self.lc_chain_7,
            chain_8=self.lc_chain_8,
        )
        self.LangChain.exec_()

    def cerrarVentana(self):
        self.close()