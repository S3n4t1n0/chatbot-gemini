import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9ImlFo2TO-liWy7eyCNu3kZI6V1IQfRw"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Aplicar nuevos estilos personalizados
st.markdown(
    """
    <style>
        body { background-color: #121212; color: #ffffff; font-family: 'Arial', sans-serif; }
        [data-testid="stAppViewContainer"] { max-width: 800px; margin: auto; }
        .chat-container { padding: 15px; border-radius: 12px; background-color: #1e1e1e; width: 100%; margin-top: 20px; }
        .chat-bubble { padding: 14px; border-radius: 12px; margin: 10px 0; display: block; max-width: 85%; font-size: 16px; }
        .chat-user { background-color: #0078ff; color: white; align-self: flex-end; text-align: right; }
        .chat-bot { background-color: #272727; color: #dddddd; align-self: flex-start; text-align: left; }
        .chat-wrapper { display: flex; flex-direction: column; align-items: flex-end; }
        .chat-wrapper-bot { display: flex; flex-direction: column; align-items: flex-start; }
        .stTextInput input { background-color: transparent; color: white; padding: 14px; font-size: 16px; border: 2px solid #0078ff; border-radius: 12px; outline: none; }
        .stTextInput input::placeholder { color: #bbbbbb; }
        .send-button { background-color: #0078ff; color: white; border: none; border-radius: 8px; padding: 12px 16px; cursor: pointer; transition: 0.3s; font-size: 16px; }
        .send-button:hover { background-color: #005bb5; }
        .new-chat-container { display: flex; justify-content: center; margin-top: 20px; }
        .new-chat-button { background-color: #ff4444; color: white; padding: 12px 24px; border-radius: 8px; border: none; font-size: 16px; cursor: pointer; transition: 0.3s; }
        .new-chat-button:hover { background-color: #cc0000; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar historial de conversación en session_state
st.session_state.setdefault("chat_history", [])

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(prompt).text

st.markdown("<h1 style='text-align: center; color: #0078ff;'>Asistente IA</h1>", unsafe_allow_html=True)

# Mostrar historial de conversación
for chat in st.session_state.chat_history:
    role_class = "chat-user" if chat["role"] == "user" else "chat-bot"
    align_class = "chat-wrapper" if chat["role"] == "user" else "chat-wrapper-bot"
    st.markdown(
        f'<div class="{align_class}"><div class="chat-bubble {role_class}">{chat["message"]}</div></div>',
        unsafe_allow_html=True
    )

# Entrada de usuario
user_input = st.text_input("", placeholder="Escribe tu mensaje aquí...", key="user_input", label_visibility="collapsed")
if st.button("Enviar", key="send_button", help="Enviar mensaje", use_container_width=True):
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        response = chat_with_gemini(user_input)
        st.session_state.chat_history.append({"role": "assistant", "message": response})
        st.rerun()

# Botón para nueva conversación
st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
if st.button("Nueva Conversación", key="new_chat", help="Reiniciar chat"):
    st.session_state.chat_history.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
