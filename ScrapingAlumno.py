import requests
from bs4 import BeautifulSoup
from FuncionesAuxScraping import RobotEspecialistaLimpiar,reemplazar_tildes,guardar_documento_txt
# URL de la página
def ScrapingAlumno():
    url = 'https://centrum.pucp.edu.pe/alumnos/'
    # Realizar solicitud HTTP
    response = requests.get(url)
    if response.status_code == 200:
        # Analizar el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # Lista de etiquetas HTML a eliminar
        etiquetas_a_eliminar = ['form', 'head',"style","script"]
        clases_a_eliminar = ["limit header__main", "limit footer_bottom__container", "jh-banner__breadcrumb", "header__title","-active-anim-"]
        # Eliminar elementos por etiqueta
        for etiqueta in etiquetas_a_eliminar:
            elementos = soup.find_all(etiqueta)
            for elemento in elementos:
                elemento.decompose()
        # Eliminar elementos por clase
        for clase in clases_a_eliminar:
            elementos = soup.find_all(class_=clase)
            for elemento in elementos:
                elemento.decompose()
        # Construir una estructura ordenada línea por línea
        contenido_ordenado = []
        for element in soup.descendants:
            if element.name == 'a':  # Si es un enlace
                url = element.get('href')
                texto = element.get_text(strip=True)
                if url:
                    contenido_ordenado.append(f'[ {url} ]')  # Formato para los enlaces
            elif element.string:  # Si es texto plano
                text = element.string.strip()
                if text:  # Evitar líneas vacías
                    contenido_ordenado.append(text)
        # Guardar en una variable local
        contenido_completo = "\n".join(contenido_ordenado)
        resultado = contenido_completo.replace("html", "")
        documento_generado=RobotEspecialistaLimpiar(resultado)
        documento_generado=reemplazar_tildes(documento_generado)
        guardar_documento_txt("Informacion-para-los-alumnos.txt", documento_generado)
        # Mostrar el resultado (opcional)
    else:
        print(f'Error al acceder a la página: {response.status_code}')