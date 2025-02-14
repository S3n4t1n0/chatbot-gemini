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
            border-radius: 10px;
            display: inline-block;
            max-width: 60%;
        }
        .chat-bubble-bot {
            background-color: white;
            color: black;
            padding: 10px;
            border-radius: 10px;
            display: inline-block;
            max-width: 60%;
        }
        .input-container {
            position: relative;
            width: 80%;
            margin: auto;
        }
        .input-box {
            width: 100%;
            padding: 12px;
            border-radius: 30px;
            border: 1px solid #30363d;
            font-size: 16px;
            padding-right: 50px;
        }
        .send-button {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background-color: black;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .send-button:hover {
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

# Input y botón en el mismo contenedor
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.session_state.user_input = st.text_input("", placeholder="Envía un mensaje a Gemini IA", value=st.session_state.user_input, key="user_input_input", label_visibility="collapsed")
if st.button("✈️", key="send", help="Enviar mensaje", args=(st.session_state.user_input,)):
    if st.session_state.user_input.strip():
        st.session_state.chat_history.append({"role": "user", "message": st.session_state.user_input})
        response = chat_with_gemini(st.session_state.user_input)
        st.session_state.chat_history.append({"role": "assistant", "message": response})
        st.session_state.user_input = ""
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Botón para limpiar el historial
if st.button("🔄 Reiniciar Chat"):
    st.session_state.chat_history = []
    st.rerun()


