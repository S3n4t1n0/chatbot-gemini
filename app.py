import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9ImlFo2TO-liWy7eyCNu3kZI6V1IQfRw"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.markdown(
    """
    <style>
        /* Aumentar el ancho de la app */
        [data-testid="stAppViewContainer"] {
            max-width: 1000px;
            margin: auto;
        }
        body {
            background-color: #0d1117;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .chat-container {
            padding: 20px;
            border-radius: 10px;
            background-color: #161b22;
            width: 100%;
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
        /* Forzar la alineación vertical en los bloques horizontales */
        [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        /* Estilos para el text input */
        .stTextInput input {
            background-color: white;
            color: black;
            border-radius: 20px;
            padding: 12px;
            font-size: 16px;
            border: 1px solid #30363d;
            height: 40px;
        }
        .stTextInput input::placeholder {
            color: grey;
        }
        /* Estilos para el botón de enviar */
        .send-button {
            background-color: black;
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            transition: 0.3s;
            font-size: 18px;
        }
        .send-button:hover {
            background-color: #333;
        }
        /* Alinear el botón New Chat a la derecha */
        .new-chat-container {
            display: flex;
            justify-content: flex-end;
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

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

st.markdown("<h1 style='text-align: center;'>¿En qué puedo ayudarte?</h1>", unsafe_allow_html=True)
st.write("")

# Mostrar historial de conversación
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(
                f'<div class="chat-wrapper"><div class="chat-bubble-user">{chat["message"]}</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-wrapper-bot"><div class="chat-bubble-bot">{chat["message"]}</div></div>',
                unsafe_allow_html=True
            )

# Formulario con columnas para alinear el input y el botón horizontalmente
with st.form(key="chat_form", clear_on_submit=True):
    cols = st.columns([9, 1])
    user_input = cols[0].text_input("", placeholder="Envía un mensaje a Gemini IA", key="user_input", label_visibility="collapsed")
    submit_button = cols[1].form_submit_button("➤")
    
if submit_button and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    response = chat_with_gemini(user_input)
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    st.rerun()

# Botón New Chat alineado a la derecha
st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
if st.button("New Chat"):
    st.session_state.chat_history = []
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
