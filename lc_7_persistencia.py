# Contenido para: lc_7_persistencia.py
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# --- Configuración Inicial ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

MEMORY_FILE = "memoria.json"

# 1. Modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# 2. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente amable que recuerda toda la conversación anterior (incluso si se reinicia el programa)."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# 3. Crear memoria global
memory = ConversationBufferMemory(return_messages=True)

# --- Funciones de Archivo (JSON) ---

def guardar_memoria():
    """Guarda el historial actual en un archivo JSON."""
    data = memory.load_memory_variables({})
    history_text = []
    
    # Convertimos los objetos complejos en diccionarios simples
    for msg in data.get("history", []):
        if hasattr(msg, "type") and hasattr(msg, "content"):
            history_text.append({"type": msg.type, "content": msg.content})
            
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": history_text}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando memoria: {e}")

def cargar_memoria():
    """Lee el JSON y restaura la memoria de LangChain."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Limpiamos memoria actual para no duplicar al recargar
                memory.clear() 
                
                for msg in data.get("history", []):
                    if msg["type"] == "human":
                        memory.chat_memory.add_user_message(msg["content"])
                    elif msg["type"] == "ai":
                        memory.chat_memory.add_ai_message(msg["content"])
        except Exception as e:
            print(f"Error cargando memoria: {e}")

# Cargamos la memoria apenas se importa este archivo
cargar_memoria()

# --- Función Principal que llamará la Ventana ---
def ejecutar_con_persistencia(texto):
    """Ejecuta el modelo, guarda en memoria RAM y luego en Disco (JSON)."""
    
    # 1. Cargar contexto actual de la RAM
    history = memory.load_memory_variables({}).get("history", [])
    
    # 2. Cadena
    chain = prompt | llm
    
    # 3. Invocar
    response = chain.invoke({"history": history, "input": texto})
    
    # 4. Guardar en RAM
    memory.save_context({"input": texto}, {"output": response.content})
    
    # 5. Guardar en DISCO (Persistencia Real)
    guardar_memoria()
    
    return response.content.strip()