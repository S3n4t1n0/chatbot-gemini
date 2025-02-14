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

        /* Ocultamos el texto del botón y agregamos una imagen de fondo */
        button[data-testid="stFormSubmitButton"] {
            background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAdVBMVEX///8AAADc3NzNzc3m5ub39/f6+vqMjIyvr6/T09Ozs7NnZ2eRkZHl5eWsrKzq6uphYWGHh4c/Pz/w8PAgICA0NDSjo6MVFRXJyclqampbW1s8PDwmJiZ3d3dVVVW3t7dKSkoPDw99fX3BwcEtLS2ZmZmXl5ccVvkXAAAEj0lEQVR4nO2ciXaiQBBF0xjADUVU3KPEJP//idMmnCQzIdhAd1U18+4X9D08oRbk4QEAAAAAAAAAAAAAAAAAAAAAAAAAAABgTJKH3EdwTKCKRcJ9CKcESjPZch/DIe+GSh3H3AdxRmmoWTxyn8UNX4Z9Det3Q6XWQ+7z2Odvw1tY59xHsswPQx3WAfehrFJhqFQ261EZUGmodBnQm7D+YqhJexLW3w37EtY6Q6VWPSgD6g01e9/DetdQlwF+h9XAUKlN7HGDZWTodVhNDXWDNYu4D9sKc0ONl2FtZOhlGdDQ8HZn5T5yQxobKt/C2sbQr7C2M1Tq4E1Y2xpqYj8arA6GnkwDOhl60WB1NFTyw9rdUHrNasNQdljtGOoGS+wGy5ahEhtWi4ZKvQwFhtWqociwWjbUpMI2WPYNlToOJU0DXBgqUetWR4aC1q3ODMWsWx0aKhnrVreGEsLq2vA2DeC9s7o3VMxhJTFknQYQGeoGi6tmJTO81awsYSU0VDxzVlpDfWclDyu1IX2DRW+oiKcBLIZKvdCNrpgMlSrioOeGiurOymlI824Ar6EiWLcuF6enFa8jQc0ahck1j58KNke6dwPm23GcHlguKenoKkpG19dTeihoHekbrGg5H+TxKaNzzLimAWFwzp8vBYkk6zQgDK6z533m+lfK/yLLMhmdp6f9iztHIevWcPmonzDp0YnjRtBSQF/TwTmfrDe2JeWtW+eja37aZxZND8Mlt1QV+lc6i0+XwoqjwHXrJ9HtCbO4dJeUF9Z/SbbDxb5THXiU+G7AD0JdB76d9uuWkv68z6qfMNs83rUQ5S8DGhKO8qeGjiuiqU5XPqr55ldxNRWwaq0nevzoyJqqvXMZi77ZJO9ddYfqbjLiVqjG0hOxmMorbJaPwXhqqaq5jCW9evSwHG3z5/Rir3/ciYmn7i5edwfb3YWAeEbLxFmHmPF+iCRMAl2DpW1rsPvwxTMKtuNFmrnp6z9543i4hyOqaduaOJ66xppRTkwJH+7z9zu/zZnEfYo3kvHTfHB+m7j+pVWxdvxw594+pQ7jGQXnKfMG8ei2NWLfAWeuWyNmQ4K7J6fhiuSPfXyGVJ07lyFd7cliSNq5MxhmtJ07uSF5a0RsyDD3pDQ8sHTudIY7pt0DlSHfWJ7EkLpzpzZknnu6NtxMuV8ccWv4cuYfy7s0lLE1cma4irnjWeLI0Hnnbo4TQ5eDpcbYN1zF/Fuj79g2lLdzt2soZ6n5hU1DYfEssWZI3LmbY8mQqzUywIqh6DeWuhvydO7mdDWU/2HBboai41nSwdD1UtMSrQ3lx7OknWEhpTUyoI3hWlztWUdzQ2/iWdLQUEznbk4jQ0GduzkNDEV17uaYGm58eLhXYmZ48eKvOdWYGMqYe7blvqH0bz3f445hJuPbh12oNRTcuZtTY+h7PEt+MxTyaU4LVBv6VnvWUWXoz382TfhheOxNPEv+MfS09qzju+GqX/Es+TJce1x71hH0N54lQX/jWRIwfh2WhuCpRw93AAAAAAAAAAAAAAAAAAAAAAAAAAAA/nf+AKHCTVKRBPClAAAAAElFTkSuQmCC"); /* Reemplaza con tu URL */
            background-repeat: no-repeat;
            background-position: center;
            background-size: 20px 20px;
            background-color: black;
            color: transparent; /* Oculta el texto de la etiqueta */
            border-radius: 50%;
            width: 40px;
            height: 40px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }
        button[data-testid="stFormSubmitButton"]:hover {
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

# Título
st.markdown("<h1 style='text-align: center;'>¿En qué puedo ayudarte?</h1>", unsafe_allow_html=True)
st.write("")

# Mostrar historial de conversación
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(
                f'<div class="chat-wrapper">'
                f'<div class="chat-bubble-user">{chat["message"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-wrapper-bot">'
                f'<div class="chat-bubble-bot">{chat["message"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# Formulario para enviar mensajes
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])  # Ajusta el tamaño del input y del botón
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Envía un mensaje a Gemini IA",
            key="user_input"
        )
    with col2:
        # El label se deja vacío para que no se muestre texto en el botón
        submit_button = st.form_submit_button(" ")

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

# Alinear el botón "New Chat" a la derecha
colA, colB = st.columns([8, 1])
with colB:
    if st.button("🔄 New Chat"):
        st.session_state.chat_history = []
        st.rerun()

