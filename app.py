import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9ImlFo2TO-liWy7eyCNu3kZI6V1IQfRw"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Aplicar estilos personalizados
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] { max-width: 1000px; margin: auto; }
        body { background-color: #0d1117; color: white; font-family: 'Arial', sans-serif; }
        .chat-container { padding: 20px; border-radius: 10px; background-color: #161b22; width: 100%; margin: auto; }
        .chat-bubble { padding: 10px; border-radius: 15px; margin: 5px 0; display: inline-block; max-width: 100%; }
        .chat-user { background-color: #6c757d; color: white; text-align: right; }
        .chat-bot { background-color: white; color: black; text-align: left; width: 100%; }
        .chat-wrapper { display: flex; flex-direction: column; align-items: flex-end; }
        .chat-wrapper-bot { align-items: flex-start; width: 100%; }
        .stTextInput input { background-color: white; color: black; border-radius: 20px; padding: 12px; font-size: 16px; }
        .stTextInput input::placeholder { color: grey; }
        .send-button { background-color: black; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; transition: 0.3s; font-size: 18px; }
        .send-button:hover { background-color: #333; }
        .new-chat-container { display: flex; justify-content: flex-end; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar historial de conversación en session_state
st.session_state.setdefault("chat_history", [])

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(prompt).text

st.markdown("<h1 style='text-align: center;'>¿En qué puedo ayudarte?</h1>", unsafe_allow_html=True)

# Mostrar historial de conversación
with st.container():
    for chat in st.session_state.chat_history:
        role_class = "chat-user" if chat["role"] == "user" else "chat-bot"
        align_class = "chat-wrapper" if chat["role"] == "user" else "chat-wrapper-bot"
        st.markdown(
            f'<div class="{align_class}"><div class="chat-bubble {role_class}">{chat["message"]}</div></div>',
            unsafe_allow_html=True
        )

# Entrada de usuario
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Envía un mensaje a Gemini IA", key="user_input", label_visibility="collapsed")
    submit_button = st.form_submit_button("➤")

if submit_button and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    st.session_state.chat_history.append({"role": "assistant", "message": chat_with_gemini(user_input)})
    st.rerun()

# Botón para nueva conversación
st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
if st.button("New Chat"):
    st.session_state.chat_history.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

