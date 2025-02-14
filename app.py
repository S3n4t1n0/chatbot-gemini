import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9ImlFo2TO-liWy7eyCNu3kZI6V1IQfRw"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para chatear con Gemini
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Interfaz en Streamlit
st.title("Chatbot con Gemini AI")
user_input = st.text_input("Escribe tu pregunta: ")

if st.button("Enviar"):
    if user_input:
        respuesta = chat_with_gemini(user_input)
        st.write(respuesta)
