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
        body { background-color: #1a1a2e; color: #e0e0e0; font-family: 'Helvetica Neue', sans-serif; }
        [data-testid="stAppViewContainer"] { max-width: 900px; margin: auto; }
        .chat-container { padding: 20px; border-radius: 10px; background-color: #16213e; width: 100%; margin-top: 20px; }
        .chat-bubble { padding: 12px; border-radius: 15px; margin: 8px 0; display: inline-block; max-width: 80%; }
        .chat-user { background-color: #0f3460; color: #ffffff; text-align: right; align-self: flex-end; }
        .chat-bot { background-color: #e94560; color: white; text-align: left; align-self: flex-start; }
        .chat-wrapper { display: flex; flex-direction: column; align-items: flex-end; }
        .chat-wrapper-bot { display: flex; flex-direction: column; align-items: flex-start; }
        .stTextInput input { background-color: #0f3460; color: white; border-radius: 20px; padding: 14px; font-size: 16px; border: none; }
        .stTextInput input::placeholder { color: #e0e0e0; }
        .send-button { background-color: #e94560; color: white; border: none; border-radius: 50%; width: 50px; height: 50px; cursor: pointer; transition: 0.3s; font-size: 20px; }
        .send-button:hover { background-color: #ff2e63; }
        .new-chat-container { display: flex; justify-content: center; margin-top: 20px; }
        .new-chat-button { background-color: #0f3460; color: white; padding: 12px 24px; border-radius: 8px; border: none; font-size: 16px; cursor: pointer; transition: 0.3s; }
        .new-chat-button:hover { background-color: #1b4965; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar historial de conversación en session_state
st.session_state.setdefault("chat_history", [])

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(prompt).text

st.markdown("<h1 style='text-align: center; color: #e94560;'>Chat con IA</h1>", unsafe_allow_html=True)

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
    user_input = st.text_input("", placeholder="Escribe tu mensaje aquí...", key="user_input", label_visibility="collapsed")
    submit_button = st.form_submit_button("➤")

if submit_button and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    st.session_state.chat_history.append({"role": "assistant", "message": chat_with_gemini(user_input)})
    st.rerun()

# Botón para nueva conversación
st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
if st.button("Nueva Conversación", key="new_chat", help="Iniciar un nuevo chat"):
    st.session_state.chat_history.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
