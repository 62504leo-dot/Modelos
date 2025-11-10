# Contenido para: main_memoria.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory 
from dotenv import load_dotenv
import os

#
# === 1. LA FUNCIÓN (ESTÁ PERFECTA) ===
#
def crear_modelo_chat_limitado():
    """
    Crea un chain de conversación que solo recuerda
    los últimos 5 PARES de interacciones (k=5).
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("La variable GOOGLE_API_KEY no está definida en el archivo .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )

    # La memoria k=5 (recuerda 5 pares) está bien
    memory = ConversationBufferWindowMemory(k=5)

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True 
    )
    return conversation


#
# === 3. EL BLOQUE DE PRUEBA (AQUÍ HACEMOS LOS CAMBIOS) ===
#
if __name__ == '__main__':
    print("Probando el modelo de 'Chat Limitado (k=5)'...")
    
    chain_de_prueba = crear_modelo_chat_limitado()
    
    # --- CAMBIO 1: Definimos el límite e inicializamos el contador ---
    limite_preguntas = 5
    contador_preguntas = 0
    
    print(f"Chat con Gemini (Se detendrá a las {limite_preguntas} preguntas). Escribe 'salir' para terminar.\n")
    
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() in ["salir", "exit"]:
            break
        
        # --- CAMBIO 2: Invocamos el modelo (esto estaba bien) ---
        respuesta_dict = chain_de_prueba.invoke({"input": mensaje})
        print("Gemini:", respuesta_dict.get('response', 'Error: No hubo respuesta'))
        
        # --- CAMBIO 3: Incrementamos el contador DESPUÉS de la respuesta ---
        contador_preguntas += 1
        
        # --- CAMBIO 4: Comprobamos si llegamos al límite ---
        if contador_preguntas >= limite_preguntas:
            print(f"\n--- Has alcanzado el límite de {limite_preguntas} preguntas. Terminando chat. ---")
            break