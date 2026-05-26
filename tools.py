from database import (
    db_agregar_libro, db_ver_libros, db_actualizar_estado,
    db_buscar_libro, db_guardar_resena, db_ver_resenas
)
from calendar_tool import agregar_evento_calendario, ver_eventos_proximos

# HERRAMIENTAS DEL AGENTE

def agregar_libro(titulo: str, autor: str = "Desconocido", estado: str = "pendiente") -> str:
    libro_id = db_agregar_libro(titulo, autor, estado)
    return f"✅ Libro '{titulo}' de {autor} agregado correctamente con ID {libro_id}. Estado: {estado}."

def ver_libros(estado: str = None) -> str:
    libros = db_ver_libros(estado)
    if not libros:
        return "📚 No hay libros en tu lista todavía."
    resultado = "📚 **Tu lista de libros:**\n\n"
    for libro in libros:
        id_, titulo, autor, estado_libro, fecha = libro
        resultado += f"- [{id_}] **{titulo}** — {autor} | Estado: {estado_libro} | Agregado: {fecha}\n"
    return resultado

def actualizar_estado_libro(libro_id: int, nuevo_estado: str) -> str:
    estados_validos = ["pendiente", "leyendo", "terminado"]
    if nuevo_estado not in estados_validos:
        return f"❌ Estado no válido. Usa uno de: {', '.join(estados_validos)}"
    db_actualizar_estado(libro_id, nuevo_estado)
    return f"✅ Estado del libro ID {libro_id} actualizado a '{nuevo_estado}'."

def guardar_resena(titulo_libro: str, texto: str, calificacion: int) -> str:
    if not (1 <= calificacion <= 5):
        return "❌ La calificación debe ser un número del 1 al 5."
    libros = db_buscar_libro(titulo_libro)
    if not libros:
        return f"❌ No encontré ningún libro con el título '{titulo_libro}'. ¿Ya lo agregaste a tu lista?"
    libro = libros[0]
    libro_id = libro[0]
    titulo_real = libro[1]
    db_guardar_resena(libro_id, texto, calificacion)
    estrellas = "⭐" * calificacion
    return f"✅ Reseña guardada para '{titulo_real}'. Calificación: {estrellas}"

def ver_resenas() -> str:
    resenas = db_ver_resenas()
    if not resenas:
        return "📝 No has escrito ninguna reseña todavía."
    resultado = "📝 **Tus reseñas:**\n\n"
    for titulo, calificacion, texto, fecha in resenas:
        estrellas = "⭐" * calificacion
        resultado += f"### {titulo} {estrellas}\n"
        resultado += f"{texto}\n"
        resultado += f"*{fecha}*\n\n"
    return resultado


# DEFINICIÓN DE HERRAMIENTAS PARA EL AGENTE

TOOLS_DEFINITION = [
    {
        "name": "agregar_libro",
        "description": "Agrega un libro nuevo a la lista de lecturas del usuario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo": {"type": "string", "description": "Título del libro"},
                "autor": {"type": "string", "description": "Autor del libro"},
                "estado": {
                    "type": "string",
                    "description": "Estado del libro: 'pendiente', 'leyendo' o 'terminado'",
                    "enum": ["pendiente", "leyendo", "terminado"]
                }
            },
            "required": ["titulo"]
        }
    },
    {
        "name": "ver_libros",
        "description": "Muestra la lista de libros del usuario, con opción de filtrar por estado.",
        "input_schema": {
            "type": "object",
            "properties": {
                "estado": {
                    "type": "string",
                    "description": "Filtrar por estado: 'pendiente', 'leyendo' o 'terminado'. Si no se pasa, muestra todos.",
                    "enum": ["pendiente", "leyendo", "terminado"]
                }
            }
        }
    },
    {
        "name": "actualizar_estado_libro",
        "description": "Actualiza el estado de lectura de un libro (ej: de pendiente a leyendo).",
        "input_schema": {
            "type": "object",
            "properties": {
                "libro_id": {"type": "integer", "description": "ID numérico del libro"},
                "nuevo_estado": {
                    "type": "string",
                    "enum": ["pendiente", "leyendo", "terminado"]
                }
            },
            "required": ["libro_id", "nuevo_estado"]
        }
    },
    {
        "name": "guardar_resena",
        "description": "Guarda una reseña de un libro que el usuario ya terminó de leer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo_libro": {"type": "string", "description": "Título del libro a reseñar"},
                "texto": {"type": "string", "description": "El texto de la reseña"},
                "calificacion": {"type": "integer", "description": "Calificación del 1 al 5"}
            },
            "required": ["titulo_libro", "texto", "calificacion"]
        }
    },
    {
        "name": "ver_resenas",
        "description": "Muestra todas las reseñas que el usuario ha escrito.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "agregar_evento_calendario",
        "description": "Agrega una sesión de lectura u otro evento al Google Calendar del usuario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo": {"type": "string", "description": "Nombre del evento, ej: 'Lectura: La Odisea'"},
                "fecha": {"type": "string", "description": "Fecha en formato YYYY-MM-DD, ej: '2026-05-25'"},
                "hora_inicio": {"type": "string", "description": "Hora de inicio en formato HH:MM, ej: '08:00'"},
                "hora_fin": {"type": "string", "description": "Hora de fin en formato HH:MM, ej: '08:30'"},
                "descripcion": {"type": "string", "description": "Descripción opcional del evento"}
            },
            "required": ["titulo", "fecha", "hora_inicio", "hora_fin"]
        }
    },
    {
        "name": "ver_eventos_proximos",
        "description": "Muestra los eventos del calendario de los próximos días.",
        "input_schema": {
            "type": "object",
            "properties": {
                "dias": {"type": "integer", "description": "Cuántos días hacia adelante revisar (default: 7)"}
            }
        }
    }
]


# MAPA DE HERRAMIENTAS

TOOLS_MAP = {
    "agregar_libro": agregar_libro,
    "ver_libros": ver_libros,
    "actualizar_estado_libro": actualizar_estado_libro,
    "guardar_resena": guardar_resena,
    "ver_resenas": ver_resenas,
    "agregar_evento_calendario": agregar_evento_calendario,
    "ver_eventos_proximos": ver_eventos_proximos,
}