
from FuncionesAuxBuildAssistant import obtenerClient,find_assistant,find_vector_store,delete_vector_store,obtenerTxts,create_or_update_assistant
def CRUD_Assistant():
    client = obtenerClient()
    Tipo_asistant = "LuxAI"
    # Verificar o crear tienda de vectores
    vector_store_name = Tipo_asistant
    existing_vector_store = find_vector_store(client, vector_store_name)
    if existing_vector_store:
        print(f"Eliminando la tienda de vectores '{vector_store_name}'...")
        delete_vector_store(client, existing_vector_store.id)
    print(f"Creando una nueva tienda de vectores '{vector_store_name}'...")
    vector_store = client.beta.vector_stores.create(name=vector_store_name)
    # Subir archivos a la tienda de vectores
    file_paths = obtenerTxts(".")
    print(f"Archivos encontrados: {file_paths}")
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    print(f"Estado del batch: {file_batch.status}")
    print(f"Conteo de archivos: {file_batch.file_counts}")
    # Actualizar asistente con la tienda de vectores
    assistant = create_or_update_assistant(client, Tipo_asistant, vector_store_id=vector_store.id)
    print(f"Asistente listo: {assistant.id}")

