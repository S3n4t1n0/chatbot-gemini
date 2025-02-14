import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "TU_CLAVE_API_AQUI"
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
        .input-container {
            position: relative;
            width: 100%;
        }
        .stTextInput {
            width: 100%;
        }
        .stTextInput > div > div {
            position: relative;
            width: 100%;
        }
        .stTextInput > div > div > input {
            background-color: white;
            color: black;
            border-radius: 20px;
            padding: 12px 50px 12px 12px;
            font-size: 16px;
            border: 1px solid #30363d;
            width: 100%;
        }
        .stTextInput > div > div > input::placeholder {
            color: grey;
        }
        .send-button {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background-color: black;
            color: white;
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            cursor: pointer;
            transition: 0.3s;
        }
        .send-button:hover {
            background-color: #333;
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

# Contenedor principal del chat
st.markdown("<h1 style='text-align: center;'>💬 Chatbot con Gemini AI</h1>", unsafe_allow_html=True)
st.write("Escribe un mensaje y recibe una respuesta de Gemini AI.")

chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f'<div class="chat-wrapper"><div class="chat-bubble-user">{chat["message"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-wrapper-bot"><div class="chat-bubble-bot">{chat["message"]}</div></div>', unsafe_allow_html=True)

# Formulario para el input del usuario
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])  # Ajusta el tamaño del input y del botón

    with col1:
        user_input = st.text_input("", placeholder="Envía un mensaje a Gemini IA", key="user_input")

    with col2:
        submit_button = st.form_submit_button("➤")

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

# Botón para limpiar el historial
if st.button("🔄 Nuevo Chat"):
    st.session_state.chat_history = []
    st.rerun()

