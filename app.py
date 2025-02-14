import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9ImlFo2TO-liWy7eyCNu3kZI6V1IQfRw"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Estilos personalizados con CSS
st.markdown(
    """
    <style>
        body {
            background-color: #0d1117;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .chat-container {
            padding: 20px;
            border-radius: 10px;
            background-color: #161b22;
            width: 80%;
            margin: auto;
        }
        .chat-bubble-user {
            background-color: #6c757d;
            color: white;
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
            text-align: right;
            display: inline-block;
            max-width: 60%;
        }
        .chat-bubble-bot {
            background-color: white;
            color: black;
            padding: 10px;
            margin: 5px 0;
            text-align: left;
            display: inline-block;
            max-width: 60%;
            border-radius: 10px;
        }
        .chat-wrapper {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        .chat-wrapper-bot {
            align-items: flex-start;
        }

        /* Ocultamos el texto del botón y agregamos una imagen de fondo */
        button[data-testid="stFormSubmitButton"] {
            background-image: url("https://cdn-icons-png.flaticon.com/128/11865/11865313.png"); /* Reemplaza con tu URL */
            background-repeat: no-repeat;
            background-position: center;
            background-size: 20px 20px;
            background-color: black;
            color: transparent; /* Oculta el texto de la etiqueta */
            border-radius: 50%;
            width: 40px;
            height: 40px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }
        button[data-testid="stFormSubmitButton"]:hover {
            background-color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar variables en session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Función para chatear con Gemini
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Título
st.markdown("<h1 style='text-align: center;'>¿En qué puedo ayudarte?</h1>", unsafe_allow_html=True)
st.write("")

# Mostrar historial de conversación
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(
                f'<div class="chat-wrapper">'
                f'<div class="chat-bubble-user">{chat["message"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-wrapper-bot">'
                f'<div class="chat-bubble-bot">{chat["message"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# Formulario para enviar mensajes
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])  # Ajusta el tamaño del input y del botón
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Envía un mensaje a Gemini IA",
            key="user_input"
        )
    with col2:
        # El label se deja vacío para que no se muestre texto en el botón
        submit_button = st.form_submit_button(" ")

# Lógica de envío del mensaje
if submit_button and user_input.strip():
    # Guardar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "message": user_input})

    # Obtener respuesta de Gemini
    response = chat_with_gemini(user_input)

    # Guardar respuesta del bot
    st.session_state.chat_history.append({"role": "assistant", "message": response})

    # Refrescar la interfaz mostrando la conversación actualizada
    st.rerun()

# Alinear el botón "New Chat" a la derecha
colA, colB = st.columns([8, 1])
with colB:
    if st.button("🔄 New Chat"):
        st.session_state.chat_history = []
        st.rerun()

