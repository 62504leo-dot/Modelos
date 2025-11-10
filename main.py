# Contenido para: main.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# 
# === ESTA ES LA FUNCIÓN QUE IMPORTARÁ TU GUI ===
#
def crear_modelo_simple():
    """
    Crea un chain simple que responde de forma general,
    sin memoria.
    """
    
    # Cargar variables del archivo .env
    load_dotenv()

    # Obtener la clave API
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("La variable GOOGLE_API_KEY no está definida en el archivo .env")

    # Crear el modelo LLM (esto ya lo tenías)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )
    
    # --- ¡CAMBIO AQUÍ! ---
    # En lugar de un "system" prompt de poeta, solo
    # le pasamos la entrada humana directamente.
    prompt = ChatPromptTemplate.from_messages([
        # ("system", "Eres un poeta experto..."), <-- Eliminamos esta línea
        ("human", "{input}") # ¡Aquí entrará el texto del botón!
    ])
    
    output_parser = StrOutputParser()

    # Creamos el "motor" (chain)
    chain = prompt | llm | output_parser
    
    # La función DEVUELVE el motor, no lo ejecuta
    return chain

# --- Bloque de prueba (esto no lo usa la GUI) ---
if __name__ == '__main__':
    # También actualicé los mensajes de prueba para que no digan "Poeta"
    print("Probando el modelo 'Simple (General)'...")
    chain_de_prueba = crear_modelo_simple()
    
    print("Escribe tu consulta (o 'salir'):\n")
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() in ["salir", "exit"]:
            break

        # Aquí sí lo invocamos, pero con el input del usuario
        respuesta = chain_de_prueba.invoke({"input": mensaje})
        print("IA:", respuesta)