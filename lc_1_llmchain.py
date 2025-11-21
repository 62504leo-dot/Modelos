# Contenido para: 1_llmchain.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_llmchain():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    # --- AQUÍ ESTÁ EL CAMBIO ---
    # Ahora pedimos DOS variables: "contexto" y "tema"
    prompt = PromptTemplate(
        input_variables=["contexto", "tema"],
        template="Instrucción/Rol: {contexto}.\nEl tema a tratar es: {tema}."
    )

    chain = prompt | llm
    return chain