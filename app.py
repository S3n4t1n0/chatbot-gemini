import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9ImlFo2TO-liWy7eyCNu3kZI6V1IQfRw"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Inicializar el historial de conversación en la sesión de Streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Función para chatear con Gemini
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Diseño de la interfaz en Streamlit
st.title("💬 Chatbot con Gemini AI")

# Mostrar el historial de chat
st.subheader("Historial de Conversación")
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["message"])

# Entrada de usuario
user_input = st.text_input("Escribe tu mensaje:", key="user_input")

# Botón de enviar
if st.button("Enviar"):
    if user_input:
        # Guardar el mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "message": user_input})

        # Obtener respuesta de Gemini
        response = chat_with_gemini(user_input)

        # Guardar la respuesta del chatbot
        st.session_state.chat_history.append({"role": "assistant", "message": response})

        # Refrescar la página para actualizar la conversación
        st.experimental_rerun()

# Botón para limpiar el historial
if st.button("🆕 Nuevo Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()
