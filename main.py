from PreguntasFrecuentes import PreguntasFrecuentesAlumni,PreguntasFrecuentesAlumno
from ScrapingAlumni import ScrapingAlumni
from ScrapingAlumno import ScrapingAlumno
from ScrapingOficinaDeTesis import ScrapingOficinaDeTesis
from FuncionesAuxScraping import limpiar_carpeta_documentos
from FuncionesAuxBuildAssistant import obtenerTxts
from CRUD_Assistant import CRUD_Assistant
from dotenv import load_dotenv

# Punto de entrada principal
if __name__ == "__main__":
    load_dotenv()
    limpiar_carpeta_documentos()
    ScrapingAlumni()
    ScrapingAlumno()
    ScrapingOficinaDeTesis()
    PreguntasFrecuentesAlumni()
    PreguntasFrecuentesAlumno()
    print("Programa ejecutado correctamente.")
    CRUD_Assistant()
