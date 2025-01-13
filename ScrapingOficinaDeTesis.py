import requests
from bs4 import BeautifulSoup
from FuncionesAuxScraping import RobotEspecialistaLimpiar,reemplazar_tildes,guardar_documento_txt

def obtenerEnlacesOficinaTesis():
    # URL de la página
    url = 'https://sites.google.com/pucp.edu.pe/prolabcentrum/inicio'
    # Realizar solicitud HTTP
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Analizar el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # Encontrar todas las etiquetas <a>
        enlaces = soup.find_all('a')
        # Usar un conjunto para almacenar enlaces únicos que contengan "pucp.edu.pe"
        enlaces_unicos = set()
        for enlace in enlaces:
            href = enlace.get('href')  # Extraer el valor de href
            if href and "pucp.edu.pe/" in href:  # Filtrar enlaces que contengan "pucp.edu.pe"
                # Completar el enlace si es relativo
                if href.startswith('/'):
                    href = "https://sites.google.com" + href
                enlaces_unicos.add(href)  # Añadir al conjunto
        # Imprimir los enlaces únicos
    else:
        print(f'Error al acceder a la página: {response.status_code}')
    return enlaces_unicos



def obtenerInformacionOficinaTesisLink(url):
    # Realizar solicitud HTTP
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Analizar el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Lista de etiquetas HTML a eliminar
        etiquetas_a_eliminar = ['form', 'head', 'style', 'script', 'nav']
        clases_a_eliminar = ["limit header__main", "limit footer_bottom__container",
                                "jh-banner__breadcrumb", "header__title", "-active-anim-", "hUphyc",
                                "GG9xTc", "Xb9hP", "ndJi5d snByac", "VfPpkd-vQzf8d","GAuSPc"]

        # Eliminar elementos por etiqueta
        for etiqueta in etiquetas_a_eliminar:
            for elemento in soup.find_all(etiqueta):
                elemento.decompose()

        # Eliminar elementos por clase
        for clase in clases_a_eliminar:
            for elemento in soup.find_all(class_=clase):
                elemento.decompose()

        # Construir una estructura ordenada línea por línea
        contenido_ordenado = []
        for element in soup.descendants:
            if element.name == 'a':  # Si es un enlace
                url = element.get('href')
                texto = element.get_text(strip=True)
                if url and "pucp.edu.pe" in url:
                    contenido_ordenado.append(f'[ https://sites.google.com{url} ]')
            elif element.name == 'iframe' and element.has_attr('data-src'):  # Si es un iframe con data-src
                data_src = element['data-src']
                if '/preview' in data_src:
                    # Buscar el texto relacionado al iframe
                    parent = element.find_parent()
                    related_text = parent.get_text(strip=True) if parent else "Sin descripción"
                    contenido_ordenado.append("==\n==\n==\n"+f'{related_text}: [ {data_src} ]')  # Formato con descripción
            elif element.string:  # Si es texto plano
                text = element.string.strip()
                if text:  # Evitar líneas vacías
                    contenido_ordenado.append(text)

        # Eliminar duplicados sin alterar el orden
        seen = set()
        contenido_ordenado = [x for x in contenido_ordenado if not (x in seen or seen.add(x))]

        # Guardar el contenido en una variable local
        contenido_completo = "\n".join(contenido_ordenado)

        # Mostrar el resultado
        return contenido_completo
    else:
        print(f'Error al acceder a la página: {response.status_code}')

def ScrapingOficinaDeTesis():
    for i, enlace in enumerate(obtenerEnlacesOficinaTesis()):
        contenido_completo = obtenerInformacionOficinaTesisLink(enlace)
        documento_generado = RobotEspecialistaLimpiar(contenido_completo)
        documento_generado=reemplazar_tildes(documento_generado)
        # Nombre del archivo basado en el índice o parte del enlace
        nombre_archivo = f"{enlace.split('/')[-1]}.txt"
        # Guardar el documento generado como archivo .txt
        guardar_documento_txt(nombre_archivo, documento_generado)
        print(f"Contenido guardado en: {nombre_archivo}")
