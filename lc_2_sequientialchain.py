# Contenido para: lc_2_sequential.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough # <--- IMPORTANTE
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_secuencial():
    """
    Cadena Secuencial Dinámica:
    1. Recibe {texto_original} y {idioma_destino}.
    2. Paso A: Resume {texto_original}.
    3. Paso B: Traduce ese resumen al {idioma_destino}.
    """
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    # --- PASO 1: RESUMIR ---
    prompt_resumen = PromptTemplate.from_template(
        "Resume el siguiente texto en un párrafo muy breve: {texto_original}"
    )
    chain_resumen = prompt_resumen | llm | StrOutputParser()
    
    # --- PASO 2: TRADUCIR ---
    # Este prompt necesita DOS cosas: el resumen (que viene del paso 1) y el idioma (que viene del inicio)
    prompt_traduccion = PromptTemplate.from_template(
        "Traduce el siguiente resumen al idioma {idioma_destino}: {resumen_generado}"
    )
    chain_traduccion = prompt_traduccion | llm | StrOutputParser()

    # --- CONEXIÓN MAESTRA ---
    # Usamos .assign para calcular el resumen y agregarlo al diccionario de datos,
    # sin perder la variable 'idioma_destino' que necesitamos después.
    chain_completa = (
        RunnablePassthrough.assign(resumen_generado=chain_resumen)
        | chain_traduccion
    )
    
    return chain_completa