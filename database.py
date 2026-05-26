 
import sqlite3
from datetime import datetime

# Este es el nombre del archivo donde vivirán todos tus datos
DB_NAME = "lecturas.db"

def conectar():
    """Abre la conexión con la base de datos. Si el archivo no existe, lo crea."""
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    """
    Crea las tablas si no existen todavía.
    Esta función se llama una vez al arrancar el agente.
    Si las tablas ya existen, no hace nada.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Tabla de libros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            estado TEXT DEFAULT 'pendiente',
            fecha_agregado TEXT
        )
    """)

    # Tabla de reseñas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER,
            texto TEXT,
            calificacion INTEGER,
            fecha TEXT,
            FOREIGN KEY (libro_id) REFERENCES libros(id)
        )
    """)

    # Tabla del historial de conversación
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()  # Guarda los cambios
    conn.close()   # Cierra la conexión


# ─────────────────────────────────────────
# Funciones para LIBROS
# ─────────────────────────────────────────

def db_agregar_libro(titulo, autor="Desconocido", estado="pendiente"):
    """Inserta un nuevo libro en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "INSERT INTO libros (titulo, autor, estado, fecha_agregado) VALUES (?, ?, ?, ?)",
        (titulo, autor, estado, fecha)
    )
    conn.commit()
    libro_id = cursor.lastrowid  # El ID que SQLite le asignó automáticamente
    conn.close()
    return libro_id

def db_ver_libros(estado=None):
    """
    Trae todos los libros. Si pasas un estado (ej: 'leyendo'),
    filtra solo los de ese estado.
    """
    conn = conectar()
    cursor = conn.cursor()
    if estado:
        cursor.execute("SELECT * FROM libros WHERE estado = ?", (estado,))
    else:
        cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    conn.close()
    return libros

def db_actualizar_estado(libro_id, nuevo_estado):
    """Cambia el estado de un libro (pendiente → leyendo → terminado)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE libros SET estado = ? WHERE id = ?",
        (nuevo_estado, libro_id)
    )
    conn.commit()
    conn.close()

def db_buscar_libro(titulo):
    """Busca un libro por título (búsqueda parcial, no necesita ser exacto)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM libros WHERE titulo LIKE ?",
        (f"%{titulo}%",)
    )
    resultado = cursor.fetchall()
    conn.close()
    return resultado


# ─────────────────────────────────────────
# Funciones para RESEÑAS
# ─────────────────────────────────────────

def db_guardar_resena(libro_id, texto, calificacion):
    """Guarda una reseña vinculada a un libro."""
    conn = conectar()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "INSERT INTO resenas (libro_id, texto, calificacion, fecha) VALUES (?, ?, ?, ?)",
        (libro_id, texto, calificacion, fecha)
    )
    conn.commit()
    conn.close()

def db_ver_resenas():
    """Trae todas las reseñas junto con el título del libro al que pertenecen."""
    conn = conectar()
    cursor = conn.cursor()
    # JOIN une dos tablas para traer el título del libro junto con la reseña
    cursor.execute("""
        SELECT libros.titulo, resenas.calificacion, resenas.texto, resenas.fecha
        FROM resenas
        JOIN libros ON resenas.libro_id = libros.id
    """)
    resenas = cursor.fetchall()
    conn.close()
    return resenas


# ─────────────────────────────────────────
# Funciones para el HISTORIAL de conversación
# ─────────────────────────────────────────

def db_guardar_mensaje(rol, mensaje):
    """Guarda un mensaje del historial (rol puede ser 'user' o 'assistant')."""
    conn = conectar()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO historial (rol, mensaje, timestamp) VALUES (?, ?, ?)",
        (rol, mensaje, timestamp)
    )
    conn.commit()
    conn.close()

def db_cargar_historial():
    """
    Carga todo el historial guardado.
    Esto es lo que permite que al refrescar la página,
    la conversación siga donde la dejaste.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT rol, mensaje FROM historial ORDER BY id ASC")
    mensajes = cursor.fetchall()
    conn.close()
    # Regresa una lista de diccionarios, que es el formato que espera Claude
    return [{"role": rol, "content": mensaje} for rol, mensaje in mensajes]