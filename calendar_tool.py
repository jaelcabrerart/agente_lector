import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# El permiso que pedimos: solo crear y leer eventos
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Archivos de credenciales
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def obtener_servicio_calendar():
    """
    Maneja la autenticación con Google y regresa el servicio de Calendar.
    La primera vez abre el navegador para que des permiso.
    Las siguientes veces usa el token guardado automáticamente.
    """
    creds = None

    # Si ya existe un token guardado, lo cargamos
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Si no hay token o ya expiró, pedimos autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Renovamos el token automáticamente si expiró
            creds.refresh(Request())
        else:
            # Primera vez: abre el navegador para dar permiso
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardamos el token para la próxima vez
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def agregar_evento_calendario(
    titulo: str,
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    descripcion: str = ""
) -> str:
    """
    Crea un evento en Google Calendar.
    
    Parámetros:
    - titulo: nombre del evento (ej: "Lectura: El Principito")
    - fecha: en formato YYYY-MM-DD (ej: "2026-05-25")
    - hora_inicio: en formato HH:MM (ej: "08:00")
    - hora_fin: en formato HH:MM (ej: "08:30")
    - descripcion: texto opcional del evento
    """
    try:
        servicio = obtener_servicio_calendar()

        # Construimos el evento en el formato que espera Google
        evento = {
            "summary": titulo,
            "description": descripcion,
            "start": {
                "dateTime": f"{fecha}T{hora_inicio}:00",
                "timeZone": "America/Mexico_City",
            },
            "end": {
                "dateTime": f"{fecha}T{hora_fin}:00",
                "timeZone": "America/Mexico_City",
            },
        }

        # Insertamos el evento en el calendario principal
        resultado = servicio.events().insert(
            calendarId="primary",
            body=evento
        ).execute()

        link = resultado.get("htmlLink", "")
        return f"✅ Evento '{titulo}' creado para el {fecha} de {hora_inicio} a {hora_fin}. Ver en calendario: {link}"

    except Exception as e:
        return f"❌ Error al crear el evento: {str(e)}"


def ver_eventos_proximos(dias: int = 7) -> str:
    """
    Muestra los eventos de los próximos N días en tu calendario.
    """
    try:
        servicio = obtener_servicio_calendar()

        ahora = datetime.datetime.utcnow().isoformat() + "Z"
        limite = (datetime.datetime.utcnow() + datetime.timedelta(days=dias)).isoformat() + "Z"

        resultado = servicio.events().list(
            calendarId="primary",
            timeMin=ahora,
            timeMax=limite,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        eventos = resultado.get("items", [])

        if not eventos:
            return f"No tienes eventos en los próximos {dias} días."

        respuesta = f"**Tus próximos eventos ({dias} días):**\n\n"
        for evento in eventos:
            inicio = evento["start"].get("dateTime", evento["start"].get("date"))
            respuesta += f"- {evento['summary']} — {inicio}\n"

        return respuesta

    except Exception as e:
        return f"Error al obtener eventos: {str(e)}" 
