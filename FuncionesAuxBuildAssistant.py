import openai
import os

def obtenerClient():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    return openai.Client(api_key=OPENAI_API_KEY)

def find_assistant(client, name):
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            return assistant
    return None

def find_vector_store(client, categoria):
    vector_stores = client.beta.vector_stores.list()
    for vector_store in vector_stores.data:
        if vector_store.name == categoria:
            return vector_store
    return None

def delete_vector_store(client, vector_store_id):
    client.beta.vector_stores.delete(vector_store_id=vector_store_id)

def obtenerTxts(categoria, directory_path="./documentos"):
    all_files = os.listdir(directory_path)
    txt_files = [
        os.path.join(directory_path, f)
        for f in all_files
        if f.lower().endswith('.txt') and categoria.lower() in f.lower()
    ]
    return txt_files

def create_or_update_assistant(client, assistant_name, vector_store_id=None):
    instructions = """
    Rol:

    Búsqueda Vectorial:
    Antes de responder, realiza una búsqueda vectorial en la base de datos para asegurar que tu respuesta esté basada en información actualizada.
    No uses datos de entrenamiento ni inventes información.
    Si un programa no está disponible, no lo ofrezcas.

    Personalidad:
    Eres una asistente amigable con los estudiantes, y tendras muchos documentos en tu disposicion.
    Solo puedes responderles en base a los documentos que tengas. No te enviarles textos grandes a los
    estudiantes por que consideras que mucha informacion les puede agobiar, por lo que prefieres resumirselo
    lo mas posible y si es posible enviar el link de los documentos que tienes si es que los tienes.
    Instrucciones:

    Restricciones:

    """
    tools = [
        {"type": "file_search"},
        {
            "type": "function",
            "function": {
                "name": "request_dni_for_courses",
                "description": "Solicita el DNI del usuario para consultar sobre cursos relacionados a su ciclo matriculado.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_intent": {
                            "type": "string",
                            "description": "La intención del usuario de preguntar sobre cursos."
                        },
                    },
                    "required": ["user_intent"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "consultar_dni",
                "description": "Cuando te brindan el DNI después de que se lo solicitaste, usaras el dni para obtener informacion del usuario",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dni": {
                            "type": "string",
                            "description": "Número de identificación del ciudadano"
                        }
                    },
                    "required": ["dni"],
                    "additionalProperties": False
                }
            }
        }
    ]
    existing_assistant = find_assistant(client, assistant_name)
    if not existing_assistant:
        print(f"Creando el asistente '{assistant_name}'...")
        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            model="gpt-4o-mini",
            tools=tools
        )
    else:
        print(f"Actualizando el asistente '{assistant_name}'...")
        assistant = client.beta.assistants.update(
            assistant_id=existing_assistant.id,
            instructions=instructions,
            model="gpt-4o-mini",
            tools=tools,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}} if vector_store_id else {}
        )
    return assistant
