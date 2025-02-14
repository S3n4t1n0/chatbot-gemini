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
        .stTextInput > div > div > input {
            background-color: white;
            color: black;
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            border: 1px solid #30363d;
        }
        .stTextInput > div > div > input::placeholder {
            color: grey;
        }
        .stButton > button {
            background-color: black;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            transition: 0.3s;
        }
        .stButton > button:hover {
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
            border-radius: 10px;
            margin: 5px 0;
            text-align: right;
        }
        .chat-bubble-bot {
            background-color: white;
            color: black;
            padding: 10px;
            margin: 5px 0;
            text-align: left;
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
            st.markdown(f'<div class="chat-bubble-user">{chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">{chat["message"]}</div>', unsafe_allow_html=True)

# Entrada del usuario
st.session_state.user_input = st.text_input("", placeholder="Envía un mensaje a Gemini IA", value=st.session_state.user_input, key="user_input_input")

# Botón de enviar
if st.button("Enviar"):
    if st.session_state.user_input.strip():
        # Guardar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "message": st.session_state.user_input})

        # Obtener respuesta de Gemini
        response = chat_with_gemini(st.session_state.user_input)

        # Guardar respuesta del bot
        st.session_state.chat_history.append({"role": "assistant", "message": response})

        # Limpiar input
        st.session_state.user_input = ""

        # Refrescar la interfaz mostrando la conversación actualizada
        st.rerun()

# Botón para limpiar el historial
if st.button("🔄 Reiniciar Chat"):
    st.session_state.chat_history = []
    st.rerun()
