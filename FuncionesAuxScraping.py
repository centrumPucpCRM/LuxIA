import requests
from bs4 import BeautifulSoup
import openai
import os
import shutil

def reemplazar_tildes(texto):
    """Reemplaza caracteres acentuados por sus equivalentes sin acento."""
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }
    for acentuado, sin_acento in reemplazos.items():
        texto = texto.replace(acentuado, sin_acento)
    return texto
def RobotEspecialistaLimpiar(mensaje):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                Eres un experto en ordenar informacion.
                A continuacion te pasaran un texto muy largo, tu objetivo es ordenar esa informacion sin perder ni resumir nada del contenido textual.
                Recuerda, no resumas informacion (esto es lo mas importante, ya que sino estaras haciendo que la persona que lo lea tenga menos informacion), pero si ves contenido redundante suprimelo
                """
            },
            {
                "role": "user",
                "content": mensaje,
            }
        ],
        model="gpt-4o-mini",
        temperature=0.5  # Establece la temperatura en 0
    )
    # Extrae y devuelve el contenido de la respuesta
    return chat_completion.choices[0].message.content
import os

def guardar_documento_txt(nombre_archivo, contenido):
    """Guarda el contenido en un archivo .txt dentro de la carpeta 'documentos'."""
    carpeta = "documentos"
    os.makedirs(carpeta, exist_ok=True)
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    with open(ruta_completa, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    print(f"Archivo guardado: {ruta_completa}")


def limpiar_carpeta_documentos(carpeta="documentos"):
    """Elimina todos los archivos de la carpeta especificada, sin borrar la carpeta."""
    if os.path.exists(carpeta):
        for archivo in os.listdir(carpeta):
            ruta_archivo = os.path.join(carpeta, archivo)
            try:
                if os.path.isfile(ruta_archivo) or os.path.islink(ruta_archivo):
                    os.unlink(ruta_archivo)  # Eliminar archivo o enlace simbólico
                elif os.path.isdir(ruta_archivo):
                    shutil.rmtree(ruta_archivo)  # Eliminar subcarpeta
            except Exception as e:
                print(f"No se pudo eliminar {ruta_archivo}. Error: {e}")
    else:
        os.makedirs(carpeta, exist_ok=True)  # Crear la carpeta si no existe
