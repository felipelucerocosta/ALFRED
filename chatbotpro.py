import streamlit as st
from PIL import Image

# ================== Configuración ==================
client = Groq(api_key=st.secrets["ngroqAPIKey"])
modelos = ['llama3-8b-8192', 'llama3-70b-8192']
temas = ['Atardecer', 'Noche', 'Mar']

st.set_page_config(page_title="RoboAlfred", page_icon="🤖", layout="wide")

# ================== Aplicar tema personalizado ==================
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

# ================== Sidebar ==================
with st.sidebar:
    st.title("⚙️ Configuración")
    parmodelo = st.selectbox("Modelo AI:", modelos)
    tema = st.selectbox("Tema visual:", temas)
    font_size = st.slider("Tamaño de fuente", min_value=12, max_value=24, value=16)
    if st.button("🧹 Limpiar historial"):
        st.session_state.messages = []
        st.experimental_rerun()

aplicar_tema(tema, font_size)

# ================== Estado ==================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================== Funciones ==================
def generate_chat_responses(chat_completion):
    for chunk in chat_completion:
        try:
            content = chunk.choices[0].delta.content
        except Exception:
            content = chunk.get('choices', [{}])[0].get('delta', {}).get('content', '')
        if content:
            yield content

def export_chat_history():
    chat_log = ""
    for msg in st.session_state.messages:
        role = msg['role'].capitalize()
        content = msg['content']
        chat_log += f"{role}:\n{content}\n\n"
    return chat_log.encode('utf-8')

# ================== UI Principal ==================
st.title("🤖 RoboAlfred")

# Mostrar historial
for message in st.session_state.messages:
    role = message["role"]
    role_class = "role-user" if role == "user" else "role-assistant"
    st.markdown(f"""
        <div class="chat-card">
            <div class="{role_class}">{role.capitalize()}:</div>
            <div>{message['content'].replace('\n', '<br>')}</div>
        </div>
    """, unsafe_allow_html=True)

# Entrada del usuario
prompt = st.chat_input("💬 Escribe tu mensaje...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        chat_completion = client.chat.completions.create(
            model=parmodelo,
            messages=st.session_state.messages,
            stream=True
        )
        full_response = ""
        for chunk in generate_chat_responses(chat_completion):
            full_response += chunk
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Botón para descargar historial
if st.session_state.messages:
    chat_bytes = export_chat_history()
    st.download_button("📥 Descargar historial del chat", data=chat_bytes, file_name="chat_history.txt", mime="text/plain")
