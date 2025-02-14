import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9ImlFo2TO-liWy7eyCNu3kZI6V1IQfRw"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Aplicar estilo oscuro con CSS
st.markdown(
    """
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #333;
            color: white;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton > button {
            background-color: #0084ff;
            color: white;
            border-radius: 10px;
            padding: 8px 16px;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #005bb5;
        }
        .chat-bubble-user {
            background-color: #0084ff;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: right;
        }
        .chat-bubble-bot {
            background-color: #333;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: left;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar historial de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Función para chatear con Gemini
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Título y diseño de la interfaz
st.title("💬 Chatbot con Gemini AI")
st.write("Escribe un mensaje y recibe una respuesta de Gemini AI.")

# Mostrar historial de chat
st.subheader("📝 Historial de Conversación")
chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">{chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">{chat["message"]}</div>', unsafe_allow_html=True)

# Entrada del usuario
user_input = st.text_input("Escribe tu mensaje:", key="user_input")

# Botón de enviar
if st.button("Enviar"):
    if user_input:
        # Guardar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "message": user_input})

        # Obtener respuesta de Gemini
        response = chat_with_gemini(user_input)

        # Guardar respuesta del bot
        st.session_state.chat_history.append({"role": "assistant", "message": response})

        # Limpiar el input sin recargar la página
        st.session_state.user_input = ""

        # Refrescar la interfaz mostrando la conversación actualizada
        st.experimental_set_query_params(dummy=str(os.urandom(8)))  # Truco para actualizar UI sin recarga

        # Volver a mostrar el historial actualizado
        st.rerun()

# Botón para limpiar el historial
if st.button("🆕 Nuevo Chat"):
    st.session_state.chat_history = []
    st.rerun()
