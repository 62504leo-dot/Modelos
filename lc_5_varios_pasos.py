# Contenido para: lc_5_varios_pasos.py
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_varios_pasos():
    """
    Motor 5: Pipeline Fijo (Resume -> Traduce al Inglés)
    Hace exactamente lo que tu código original hacía.
    """
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    # Paso A: Resumir
    prompt_resumen = PromptTemplate.from_template("Resume el siguiente texto: {input}")
    
    # Paso B: Traducir (Recibe el resumen anterior)
    prompt_traduccion = PromptTemplate.from_template("Tradúcelo al inglés: {input}")

    # --- LA TUBERÍA ---
    # 1. Prompt Resumen -> 2. LLM -> 3. Limpiar Texto -> 4. Prompt Traducción -> 5. LLM -> 6. Limpiar Texto
    chain = (
        prompt_resumen 
        | llm 
        | StrOutputParser() 
        | prompt_traduccion 
        | llm 
        | StrOutputParser()
    )
    
    return chain