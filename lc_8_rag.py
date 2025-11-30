# Contenido para: lc_8_rag.py
import os
import time
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_rag():
    """
    Motor 8: RAG Ajustado para PDFs pequeños (Evita error n_neighbors).
    """
    pdf_path = "documentos/fuente.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Advertencia: Falta {pdf_path}")
        return None

    try:
        print("1. Procesando PDF...")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # --- CAMBIO 1: Cortar en trozos más pequeños (500 letras) ---
        # Esto ayuda a que incluso un PDF de 1 página genere 2 o 3 fragmentos
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = splitter.split_documents(pages)
        print(f"   -> Se generaron {len(docs)} fragmentos de texto.")

        print("2. Embeddings (text-embedding-004)...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        time.sleep(1)

        print("3. Índice (Scikit-Learn)...")
        vectorstore = SKLearnVectorStore.from_documents(
            documents=docs, 
            embedding=embeddings
        )

        # --- CAMBIO 2: Lógica de Seguridad para 'k' ---
        # Si tenemos menos de 3 fragmentos, pedimos solo los que existan (k=1)
        # para evitar el error "Expected n_neighbors <= n_samples_fit"
        k_neighbors = 1 if len(docs) < 3 else 3
        
        retriever = vectorstore.as_retriever(search_kwargs={"k": k_neighbors})

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

        template = """Responde basándote solo en esto: {context} Pregunta: {question}"""
        prompt = ChatPromptTemplate.from_template(template)

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt | llm | StrOutputParser()
        )
        
        return rag_chain

    except Exception as e:
        print(f"Error RAG: {e}")
        return None