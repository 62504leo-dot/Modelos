try:
    from langchain.memory import ConversationBufferMemory
    print("✅ ¡ENCONTRADO! La memoria está lista para usarse.")
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print("El paquete 'langchain' (a secas) no está instalado o está corrupto.")