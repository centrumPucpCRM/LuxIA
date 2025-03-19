import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import openai
import json
import html
import subprocess
import os

# Configurar API Key de OpenAI
OPENAI_API_KEY = ''
roj-DK30LN7T5Kvup-J-wlc5vYgF2EBt3pmD8HGMCHoM9hEwNFRhNoBDVCAXpi4nI1D-1wWS3Tw6R_T3BlbkFJztXkhLAwT85NwU6rAllvpRtwlEWpkMrb4CmMk0NKU_nJCBM612f5gdjCMlLyMN4SUt3vtL
# Función para usar OpenAI Whisper API
def transcribe_audio_openai(audio_path):
    with open(audio_path, "rb") as audio_file:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": audio_file},
            data={"model": "whisper-1"}
        )
    return response.json().get("text", "")

# Función para descargar audio de YouTube
def download_audio(youtube_url, output_path):
    command = ["yt-dlp", "--cookies-from-browser", "chrome", "-x", "--audio-format", "mp3", "-o", output_path, youtube_url]
    subprocess.run(command, check=True)

# Función para limpiar texto con OpenAI
def RobotEspecialistaLimpiar(mensaje):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": """
Eres un experto en organizar información. Se te entregará un texto muy extenso y tu tarea es reestructurarlo para que sea más claro y fácil de leer, sin perder ni omitir absolutamente ningún detalle del contenido original. Es fundamental que:

- Conserves cada palabra y cada detalle textual, sin resumir ni modificar nada.
- Si lo consideras necesario, puedes reubicarlas en subsecciones o notas, pero sin eliminarlas.
- No realices ningún tipo de condensación o resumen que implique pérdida de información.
- Asegures que el resultado final mantenga íntegro el contenido original, facilitando al lector acceder a toda la información.

El resultado debe ser claro y comprensible para un humano.
              """
          },
          {
              "role": "user",
              "content": mensaje,
          }
      ],
      model="gpt-4o-mini",
      temperature=0.1
    )
    return chat_completion.choices[0].message.content

# Función para extraer contenido de una página web
def scrape_text_and_links_in_order(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error al acceder a la página: {e}", []

    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup.find_all(['script', 'style', 'noscript', 'header', 'footer']):
        tag.decompose()
    for tag in soup.find_all(attrs={"data-elementor-type": ["header", "footer"]}):
        tag.decompose()
    # Eliminar todos los elementos con la clase 'dashicons'
    for tag in soup.find_all(class_=["dashicons", "elementor-pagination"]):
        tag.decompose()

    results = []

    def process_node(node):
        if isinstance(node, Tag):
            # Detectar videos de YouTube
            if node.has_attr("data-elementor-lightbox"):
                try:
                    raw_value = node["data-elementor-lightbox"]
                    decoded = html.unescape(raw_value)
                    data = json.loads(decoded)
                    if data.get("type") == "video" and data.get("videoType") == "youtube":
                        video_url = data.get("url", "")
                        if video_url:
                            results.append(("youtube_video", video_url))
                            print(f"Procesando transcripción para: {video_url}")

                            # Descargar y transcribir el audio
                            video_id = video_url.split("/")[-1].split("?")[0]
                            audio_filename = f"audio_{video_id}.mp3"

                            download_audio(video_url, audio_filename)
                            transcript = transcribe_audio_openai(audio_filename)

                            results.append(("transcription", transcript))
                            os.remove(audio_filename)  # Eliminar archivo después de procesarlo
                except Exception as e:
                    print(f"Error procesando video: {e}")

        if isinstance(node, NavigableString):
            parent = node.parent  # Obtener el elemento padre

            # Verificar si el padre es una etiqueta <span> con la clase "elementor-counter-number"
            if isinstance(parent, Tag) and "elementor-counter-number" in parent.get("class", []):
                print("==analizar==")
                print("node",node)
                print("parent",parent)
                print("Tag",Tag)
                data_to_value = parent.get("data-to-value", "").strip()  # Extraer "data-to-value"
                print("data_to_value",data_to_value)
                if data_to_value:
                    results.append(("text", data_to_value))  # Guardar el valor del contador
                else:
                    results.append(("text", node.strip()))  # En caso de que "data-to-value" esté vacío
            else:
                text = node.strip()
                if text:
                    results.append(("text", text))

        elif isinstance(node, Tag):
            if node.name == 'a':
                link_text = node.get_text(strip=True)
                href = node.get('href', '')
                if link_text:
                    results.append(("link", link_text, href))
            for child in node.children:
                process_node(child)

    process_node(soup)

    return results



# Ejecutar el script
if __name__ == "__main__":
    urls = [
        "https://centrumthink.pucp.edu.pe/nosotros/",
        "https://centrumthink.pucp.edu.pe/centros-de-investigacion/centro-de-estudios-empresariales/",
        "https://centrumthink.pucp.edu.pe/centros-de-investigacion/centro-de-investigacion-en-liderazgo-socialmente-responsable-mujer-y-equidad/",
        "https://centrumthink.pucp.edu.pe/centros-de-investigacion/centro-de-investigacion-en-innovacion-de-la-cadena-de-valor/",
        "https://centrumthink.pucp.edu.pe/centros-de-investigacion/centro-de-investigacion-para-la-sostenibilidad-y-la-innovacion-social/",
        "https://centrumthink.pucp.edu.pe/centros-de-investigacion/centro-de-investigacion-para-la-educacion-en-negocios/",
        "https://centrumthink.pucp.edu.pe/centros-de-investigacion/centro-de-investigacion-en-competitividad-finanzas-corporativas-y-politicas-publicas/",
        "https://centrumthink.pucp.edu.pe/eventos-con-stakeholders/",
        "https://centrumthink.pucp.edu.pe/hub-de-investigacion-y-desarrollo/",
        "https://centrumthink.pucp.edu.pe/observatorio/"
    ]

    for url in urls:
        results = scrape_text_and_links_in_order(url)

        message = ""
        for item in results:
            if item[0] == "text":
                message += item[1] + "\n"
            elif item[0] == "link":
                message += f"Link: {item[1]} -> {item[2]}\n"
            elif item[0] == "youtube_video":
                message += f"YouTube Video: {item[1]}\n"
            elif item[0] == "transcription":
                message += f"Transcripción: {item[1]}\n"

        # Procesar el texto con la IA
        cleaned_text = RobotEspecialistaLimpiar(message)

        # Crear un nombre de archivo basado en la URL
        file_name = url.strip("/").split("/")[-1] + ".txt"
        file_path = os.path.join("output", file_name)

        # Crear el directorio "output" si no existe
        os.makedirs("output", exist_ok=True)

        # Guardar el contenido en un archivo
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(cleaned_text)

        print(f"Archivo guardado: {file_path}")

