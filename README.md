\# Agente Lector



Agente de inteligencia artificial que te permite organizar tu lista de lecturas, agendar sesiones en Google Calendar y guardar reseñas de libros.



Construido con Python, NVIDIA NIM (gratuito) y Google Calendar API (gratuita).



\## ¿Qué puede hacer?



\- Agregar libros a tu lista con estado: pendiente, leyendo o terminado

\- Ver y filtrar tu lista de libros

\- Actualizar el estado de un libro

\- Agendar sesiones de lectura en Google Calendar

\- Guardar y ver reseñas con calificación del 1 al 5

\- Recordar toda la conversación aunque refresques la página



\## Requisitos



\- Python 3.10 o superior

\- Una cuenta gratuita en NVIDIA NIM (https://build.nvidia.com)

\- Una cuenta de Google con acceso a Google Calendar



\## Instalación



\### 1. Clona el repositorio



git clone https://github.com/TU\_USUARIO/agente\_lector.git

cd agente\_lector



\### 2. Crea y activa el entorno virtual



En Windows:

python -m venv venv

venv\\Scripts\\activate



En Mac/Linux:

python -m venv venv

source venv/bin/activate



\### 3. Instala las dependencias



pip install -r requirements.txt



\### 4. Configura tu API key de NVIDIA



Crea un archivo llamado .env en la carpeta del proyecto con este contenido:



NVIDIA\_API\_KEY=tu\_api\_key\_aqui



Obtén tu API key gratis en: https://build.nvidia.com



\### 5. Configura Google Calendar



Sigue estos pasos para obtener tus credenciales:



1\. Ve a https://console.cloud.google.com

2\. Crea un proyecto nuevo

3\. Activa la API de Google Calendar

4\. Crea credenciales OAuth para aplicación de escritorio

5\. Descarga el archivo JSON y renómbralo a credentials.json

6\. Coloca credentials.json en la carpeta del proyecto



La primera vez que corras el agente, se abrirá el navegador para que des permiso de acceso a tu calendario. Esto solo pasa una vez.



\### 6. Corre el agente



python app.py



Luego abre tu navegador en: http://127.0.0.1:7860



\## Estructura del proyecto



agente\_lector/

&#x20;   app.py              <- interfaz web con Gradio

&#x20;   agente.py           <- cerebro del agente

&#x20;   tools.py            <- herramientas del agente

&#x20;   database.py         <- base de datos SQLite

&#x20;   calendar\_tool.py    <- conexión con Google Calendar

&#x20;   requirements.txt    <- lista de dependencias

&#x20;   .env                <- tu API key (NO se sube a GitHub)

&#x20;   credentials.json    <- credenciales de Google (NO se sube a GitHub)

&#x20;   token.json          <- token de acceso (se genera automáticamente)

&#x20;   lecturas.db         <- tu base de datos (se genera automáticamente)



\## Modelo de IA utilizado



Este agente usa mistral-nemotron de NVIDIA NIM, disponible completamente gratis en https://build.nvidia.com.

No requiere tarjeta de crédito.



\## Costos



\- NVIDIA NIM: GRATIS (40 solicitudes por minuto)

\- Google Calendar API: GRATIS (hasta 1 millón de solicitudes al día)

\- Gradio: GRATIS

\- SQLite: GRATIS

