from langchain_openai import ChatOpenAI
import os

#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

os.environ["OPENAI_API_KEY"] = "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"
model = ChatOpenAI(model="gpt-4o-mini")

respuesta = model.invoke("¿Qué es LangChain?")
print(respuesta.content)