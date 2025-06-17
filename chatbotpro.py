import streamlit as st

temas = ['Atardecer', 'Noche', 'Mar']

modelos = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768']

# CONFIGURAR PAGINA
def aplicar_tema(tema, font_size):
    if tema == "Noche":
        bg_color = "#0b0c10"
        text_color = "#66fcf1"
        chat_bg = "#1f2833"
        border_color = "#45a29e"
        input_bg = "#12192b"
        input_text = "#a3f0f5"
    elif tema == "Mar":
        bg_color = "#d0f0fd"
        text_color = "#03396c"
        chat_bg = "#b6e0fe"
        border_color = "#005b96"
        input_bg = "#c0ddff"
        input_text = "#002855"
    else:  # Atardecer
        bg_color = "#fbe8a6"
        text_color = "#bb5500"
        chat_bg = "#ffd97d"
        border_color = "#cc7000"
        input_bg = "#fff2cc"
        input_text = "#7a3e00"

    st.markdown(f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
            font-size: {font_size}px;
        }}

        .chat-card {{
            background-color: {chat_bg};
            border-left: 5px solid {border_color};
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 10px;
            word-wrap: break-word;
        }}

        .role-user {{
            font-weight: 700;
            margin-bottom: 5px;
        }}
        .role-assistant {{
            font-style: italic;
            margin-bottom: 5px;
        }}

        .stButton>button {{
            background-color: {border_color} !important;
            color: white !important;
            border-radius: 8px !important;
        }}

        .css-1d391kg,
        .css-1v3fvcr,
        textarea,
        input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-radius: 8px !important;
        }}

        .css-1v3fvcr {{
            padding: 10px !important;
        }}

        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}
    </style>
    """, unsafe_allow_html=True)


st.set_page_config(page_title="RoboAlfred", page_icon="🤖", layout="wide")

# CREAR UN CLIENTE GROQ => NOSOTROS
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)
    
with st.sidebar:
    st.title("⚙️ Configuración")
    parmodelo = st.selectbox("Modelo AI:", modelos)
    tema = st.selectbox("Tema visual:", temas)
    font_size = st.slider("Tamaño de fuente", min_value=12, max_value=24, value=16)
    if st.button("🧹 Limpiar historial"):
        st.session_state.messages = []
        st.experimental_rerun()

aplicar_tema(tema, font_size)

#INICIALIZAR EL ESTADO DEL CHAT
#streamlit => variable especial llamada session_state. {mensajes => []}
def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #lista
#MOSTRAR MENSAJES REVIOS

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes: # recorrer los mensajes de st.session_state.mensaje
        with st.chat_message(mensaje["role"]): #quien lo envia ??
            st.markdown(mensaje["content"]) #que envia?

#OBTENER MENSAJE USUARIO
def obtener_mensaje_usuario():
    return st.chat_input("Envia tu mensaje")

#GUARDAR LOS MENSAJES
def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

#MOSTRAR LOS MENSAJES EN PANTALLA
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)
    

#llamar DEL MODELO DE GROQ
def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream= False
    )
    return respuesta.choices[0].message.content
    
    
    

def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    
    inicializar_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    obtener_mensajes_previos()
    
    if mensaje_usuario:
        agregar_mensajes_previos("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)
    
        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo,st.session_state.mensajes )

        agregar_mensajes_previos("assistant",respuesta_contenido)
        mostrar_mensaje("assistant",respuesta_contenido)
    
    
# EJECUTAR LA APP( si __name__ es igual a __main__ se ejecuta la funcion, y __main__ es mi archivo principal)
if __name__ == '__main__':
    ejecutar_chat()

