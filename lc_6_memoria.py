# Contenido para: lc_6_memoria.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Cargar variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# --- CONFIGURACIÓN GLOBAL (Para que la memoria persista) ---

# 1. Modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# 2. Prompt con historial
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil y recuerdas la conversación anterior."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# 3. Memoria (Global en este archivo)
memory = ConversationBufferMemory(return_messages=True)

def ejecutar_con_memoria(texto_usuario):
    """
    Función que llama la GUI.
    Toma el texto, inyecta la memoria, ejecuta y guarda el resultado.
    """
    # A) Cargar historial previo
    historial_actual = memory.load_memory_variables({}).get("history", [])
    
    # B) Crear la cadena (Chain)
    chain = prompt | llm
    
    # C) Invocar con el historial cargado
    # Pasamos 'history' explícitamente porque usamos un placeholder
    respuesta = chain.invoke({
        "history": historial_actual, 
        "input": texto_usuario
    })
    
    # D) Guardar el turno actual en la memoria
    memory.save_context(
        {"input": texto_usuario}, 
        {"output": respuesta.content}
    )
    
    # E) Retornar solo el texto
    return respuesta.content.strip()