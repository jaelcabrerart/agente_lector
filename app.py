import gradio as gr
from agente import procesar_mensaje
from database import inicializar_db, db_cargar_historial

inicializar_db()


def responder(mensaje, historial_interfaz):
    respuesta = procesar_mensaje(mensaje)
    historial_interfaz.append({"role": "user", "content": mensaje})
    historial_interfaz.append({"role": "assistant", "content": respuesta})
    return "", historial_interfaz


def cargar_historial_inicial():
    mensajes = db_cargar_historial()
    historial_interfaz = []
    for msg in mensajes:
        if msg["role"] in ("user", "assistant"):
            historial_interfaz.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    return historial_interfaz


DESCRIPCION = (
    "# Agente Lector\n\n"
    "Tu asistente personal para organizar lecturas, agendar sesiones y escribir resenas.\n\n"
    "Puedes pedirme cosas como:\n"
    "- Agrega el libro Don Quijote de Cervantes a mi lista\n"
    "- Que libros tengo pendientes?\n"
    "- Agrega 30 minutos de lectura manana a las 7am\n"
    "- Quiero escribir una resena de La Odisea\n"
)

CSS = ".gradio-container { max-width: 800px !important; margin: auto; }"

with gr.Blocks(title="Agente Lector") as interfaz:

    gr.Markdown(DESCRIPCION)

    chatbot = gr.Chatbot(
        value=cargar_historial_inicial(),
        height=480,
        show_label=False
    )

    with gr.Row():
        texto_entrada = gr.Textbox(
            placeholder="Escribe tu mensaje aqui...",
            show_label=False,
            scale=9,
            autofocus=True
        )
        boton_enviar = gr.Button("Enviar", scale=1, variant="primary")

    gr.Examples(
        examples=[
            "Que puedes hacer?",
            "Muestrame mis libros pendientes",
            "Agrega una sesion de lectura manana de 9:00 a 9:30",
            "Quiero ver mis resenas",
        ],
        inputs=texto_entrada,
        label="Ejemplos rapidos"
    )

    boton_enviar.click(
        fn=responder,
        inputs=[texto_entrada, chatbot],
        outputs=[texto_entrada, chatbot]
    )

    texto_entrada.submit(
        fn=responder,
        inputs=[texto_entrada, chatbot],
        outputs=[texto_entrada, chatbot]
    )


if __name__ == "__main__":
    interfaz.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        theme=gr.themes.Soft(),
        css=CSS
    )