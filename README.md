# 📚 Agente Lector

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![NVIDIA NIM](https://img.shields.io/badge/NVIDIA%20NIM-Gratis-brightgreen)
![Google Calendar](https://img.shields.io/badge/Google%20Calendar-API-orange)

Un agente de inteligencia artificial que te permite organizar tu lista de lecturas, agendar sesiones en Google Calendar y guardar reseñas de tus libros favoritos.

Construido con Python, NVIDIA NIM (gratuito) y la API de Google Calendar (gratuita).
Este agente está impulsado por mistral-nemotron a través de NVIDIA NIM.
Está disponible de manera completamente gratuita en NVIDIA Build y no requiere ingresar tarjeta de crédito.

---

## ✨ ¿Qué puede hacer?

* **Gestionar lecturas:** Agrega libros a tu lista con estados claros (*pendiente*, *leyendo* o *terminado*).
* **Explorar tu biblioteca:** Ve y filtra tu lista de libros fácilmente.
* **Actualizar el progreso:** Cambia el estado de un libro conforme avanzas.
* **Agendar sesiones:** Crea bloques de tiempo para leer directamente en tu Google Calendar.
* **Reseñar:** Guarda y consulta reseñas de tus libros con una calificación del 1 al 5.
* **Memoria conversacional:** El agente recuerda toda la conversación, incluso si refrescas la página.

---

## 🛠️ Requisitos

* Python 3.10 o superior.
* Una cuenta gratuita en [NVIDIA NIM](https://build.nvidia.com).
* Una cuenta de Google con acceso a Google Calendar.

---

## 🚀 Instalación

### 1. Clona el repositorio

git clone [https://github.com/TU_USUARIO/agente_lector.git](https://github.com/TU_USUARIO/agente_lector.git)
cd agente_lector

### 2. Crea y activa el entorno virtual

En Windows:
python -m venv venv
venv\Scripts\activate

En Mac / Linux:
python -m venv venv
source venv/bin/activate

### 3. Instala las dependencias

pip install -r requirements.txt

### 4. Configura tu API key de NVIDIA

Crea un archivo llamado .env en la raíz del proyecto y agrega tu clave de la siguiente manera:
Fragmento de código: NVIDIA_API_KEY=tu_api_key_aqui
Nota: Puedes obtener tu API key completamente gratis en NVIDIA Build.

### 5. Configura Google Calendar

-- Sigue estos pasos para obtener tus credenciales y permitir que el agente agende por ti:
-- Ve a Google Cloud Console.
-- Crea un proyecto nuevo.
-- Activa la API de Google Calendar.
-- Crea credenciales OAuth para una aplicación de escritorio.
-- Descarga el archivo JSON generado y renómbralo a credentials.json.
-- Mueve credentials.json a la carpeta principal de este proyecto.

Importante: La primera vez que corras el agente, se abrirá una ventana en tu navegador para que autorices el acceso a tu calendario. Esto solo se te pedirá una vez.

### 6. Corre el agente

python app.py
Una vez que esté corriendo, abre tu navegador y visita: http://127.0.0.1:7860

## Estructura del proyecto

agente_lector/
├── app.py              # Interfaz web con Gradio
├── agente.py           # Cerebro del agente (Lógica principal)
├── tools.py            # Herramientas adicionales del agente
├── database.py         # Gestión de la base de datos SQLite
├── calendar_tool.py    # Conexión e interacción con Google Calendar
├── requirements.txt    # Lista de dependencias del proyecto
├── .env                # 🔒 Tu API key (NO se sube a GitHub)
├── credentials.json    # 🔒 Credenciales de Google (NO se sube a GitHub)
├── token.json          # Token de acceso (Se genera automáticamente)
└── lecturas.db         # Tu base de datos (Se genera automáticamente)
