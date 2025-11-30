# Contenido para: lc_4_parseo.py
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# CAMBIO CLAVE: Usamos StrOutputParser (Para texto limpio)
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_parser():
    """
    Motor 4: Output Parser (Resumidor de Texto)
    Este código coincide con la ventana de 1 sola caja de texto.
    """
    
    # Modelo
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    # 1. Prompt (Esperando variable {input})
    prompt = PromptTemplate.from_template(
        "Resume el siguiente texto en una oración clara y concisa:\n\n{input}"
    )

    # 2. Parser (Limpiador de texto)
    parser = StrOutputParser()

    # 3. Cadena
    chain = prompt | llm | parser
    
    return chain