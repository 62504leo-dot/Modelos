# Contenido para: lc_3_simplesequentialchain.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

# Cargar API Key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_simple_secuencial():
    """
    Motor 3: Cadena Simple Dinámica (2 Pasos Libres).
    Hace lo mismo que tu código de referencia (encadenar 2 cosas),
    pero permite que las instrucciones vengan desde la ventana.
    """
    
    # Usamos el modelo estándar (puedes cambiar a gemini-2.5-flash si tienes acceso)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    # --- PASO 1: Primera Orden ---
    # Ejecuta la orden 1 sobre el input original
    # Ejemplo: "Resume esto": "Texto largo..."
    prompt_1 = PromptTemplate.from_template("{instruccion_1}: {input}")
    
    # Creamos el eslabón 1 (Prompt -> LLM -> Texto Limpio)
    chain_1 = prompt_1 | llm | StrOutputParser()

    # --- PASO 2: Segunda Orden ---
    # Ejecuta la orden 2 sobre el RESULTADO del paso 1
    # Ejemplo: "Traduce al inglés": "El resumen generado antes..."
    prompt_2 = PromptTemplate.from_template("{instruccion_2}: {resultado_paso_1}")
    
    # Creamos el eslabón 2
    chain_2 = prompt_2 | llm | StrOutputParser()

    # --- CONEXIÓN DE LA TUBERÍA ---
    # 1. Ejecuta chain_1 y guarda el resultado en la variable 'resultado_paso_1'
    # 2. Pasa todo a chain_2 (que usará esa variable)
    chain_completa = (
        RunnablePassthrough.assign(resultado_paso_1=chain_1)
        | chain_2
    )
    
    return chain_completa