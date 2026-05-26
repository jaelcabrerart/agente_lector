import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from database import inicializar_db, db_guardar_mensaje, db_cargar_historial
from tools import TOOLS_DEFINITION, TOOLS_MAP

# Carga las variables del archivo .env
load_dotenv()

# Inicializa la base de datos al arrancar
inicializar_db()

# Crea el cliente apuntando a NVIDIA NIM
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

SYSTEM_PROMPT = """
Eres un asistente personal de lectura llamado Lector. Eres amigable, entusiasta 
y apasionado por los libros.

Ayudas al usuario a:
- Organizar su lista de lecturas (libros pendientes, en curso y terminados)
- Agregar sesiones de lectura a su calendario de Google
- Escribir y guardar reseñas de los libros que ha leído

REGLAS IMPORTANTES:
- Siempre usa las herramientas disponibles cuando el usuario quiera agregar, 
  ver o modificar libros o reseñas. No finjas hacerlo, hazlo de verdad.
- Cuando el usuario mencione un libro, pregunta por el autor si no lo sabes.
- Para reseñas, ayuda al usuario a estructurar sus pensamientos si lo necesita.
- Sé conciso pero cálido en tus respuestas.
- Responde siempre en español.
"""


def procesar_mensaje(mensaje_usuario: str) -> str:
    import json, re

    db_guardar_mensaje("user", mensaje_usuario)
    historial = db_cargar_historial()

    tools_openai = [{"type": "function", "function": {
        "name": t["name"],
        "description": t["description"],
        "parameters": t["input_schema"]
    }} for t in TOOLS_DEFINITION]

    respuesta = client.chat.completions.create(
        model="mistralai/mistral-nemotron",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial,
        tools=tools_openai,
        max_tokens=1024
    )

    # Loop principal del agente
    for _ in range(5):  # máximo 5 iteraciones para evitar loops infinitos
        mensaje = respuesta.choices[0].message
        finish_reason = respuesta.choices[0].finish_reason
        contenido = mensaje.content or ""

        # CASO 1: El modelo usa tool_calls correctamente
        if finish_reason == "tool_calls" and mensaje.tool_calls:
            historial.append({
                "role": "assistant",
                "content": contenido,
                "tool_calls": [tc.model_dump() for tc in mensaje.tool_calls]
            })

            for tool_call in mensaje.tool_calls:
                nombre_tool = tool_call.function.name
                argumentos = json.loads(tool_call.function.arguments)
                print(f"[Herramienta: {nombre_tool} | Args: {argumentos}]")

                resultado = TOOLS_MAP[nombre_tool](**argumentos) if nombre_tool in TOOLS_MAP else f"Error: herramienta '{nombre_tool}' no encontrada."

                historial.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": resultado
                })

        # CASO 2: El modelo devuelve el JSON de la herramienta como texto
        elif contenido and contenido.strip().startswith("{"):
            try:
                # Intentamos parsear el JSON que devolvió el modelo
                datos = json.loads(contenido.strip())
                nombre_tool = datos.get("name")
                argumentos = datos.get("parameters", datos.get("arguments", {}))

                if nombre_tool and nombre_tool in TOOLS_MAP:
                    print(f"[Herramienta (texto): {nombre_tool} | Args: {argumentos}]")
                    resultado = TOOLS_MAP[nombre_tool](**argumentos)

                    historial.append({"role": "assistant", "content": contenido})
                    historial.append({"role": "user", "content": f"Resultado de la herramienta: {resultado}"})
                else:
                    # No es una herramienta válida, es la respuesta final
                    break
            except json.JSONDecodeError:
                break

        # CASO 3: Respuesta final en texto normal
        else:
            break

        # Volvemos a llamar al modelo con los resultados
        respuesta = client.chat.completions.create(
            model="mistralai/mistral-nemotron",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial,
            tools=tools_openai,
            max_tokens=1024
        )

    # Extraemos la respuesta final
    respuesta_final = respuesta.choices[0].message.content or "No pude generar una respuesta."
    db_guardar_mensaje("assistant", respuesta_final)
    return respuesta_final

    # 4. Enviamos el mensaje a NVIDIA NIM
    respuesta = client.chat.completions.create(
        model="mistralai/mistral-nemotron",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial,
        tools=tools_openai,
        max_tokens=1024
    )

    # 5. Loop del agente: ejecutamos herramientas mientras sea necesario
    while respuesta.choices[0].finish_reason == "tool_calls":
        mensaje_asistente = respuesta.choices[0].message
        historial.append({
            "role": "assistant",
            "content": mensaje_asistente.content,
            "tool_calls": [tc.model_dump() for tc in mensaje_asistente.tool_calls]
        })

        for tool_call in mensaje_asistente.tool_calls:
            nombre_tool = tool_call.function.name
            argumentos = json.loads(tool_call.function.arguments)

            print(f"[Agente usando herramienta: {nombre_tool} con {argumentos}]")

            if nombre_tool in TOOLS_MAP:
                resultado = TOOLS_MAP[nombre_tool](**argumentos)
            else:
                resultado = f"Error: herramienta '{nombre_tool}' no encontrada."

            historial.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": resultado
            })

        respuesta = client.chat.completions.create(
            model="mistralai/mistral-nemotron",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial,
            tools=tools_openai,
            max_tokens=1024
        )

    # 6. Extraemos la respuesta final y la guardamos
    respuesta_final = respuesta.choices[0].message.content or "No pude generar una respuesta."
    db_guardar_mensaje("assistant", respuesta_final)
    return respuesta_final


# Permite probar el agente directamente desde la terminal
if __name__ == "__main__":
    print("Agente Lector iniciado. Escribe 'salir' para terminar.\n")
    while True:
        entrada = input("Tú: ").strip()
        if entrada.lower() == "salir":
            break
        if not entrada:
            continue
        respuesta = procesar_mensaje(entrada)
        print(f"\nLector: {respuesta}\n")
