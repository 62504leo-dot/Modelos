from groq import Groq

class ModeloOpenAI:
    def __init__(self):
        pass

def modeloSimple(self):
    cliente = Groq(api_key='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')
    respuesta = cliente.chat.completions.create(model='llama-3.1-8b-instant',

    messages=[{'role':'user',
    'content':'crea un resumen de la pelicula gigantes de acero'}])

    print(respuesta.choices[0].message.content)