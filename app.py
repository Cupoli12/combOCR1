import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator


text = " "

# Función mejorada para convertir texto a voz
def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[0:20] if text else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# Eliminar archivos antiguos de mp3
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

# Configuración y personalización de la interfaz de Streamlit
st.set_page_config(page_title="OCR y Traductor", page_icon="🌐", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #D3D3D3; /* Color de fondo gris */
    }
    h1 {
        color: #FF6347;
        font-size: 45px;
        text-align: center;
        font-family: 'Helvetica';
    }
    .stButton button {
        background-color: #FF6347;
        color: white;
        border: none;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #FF4500;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Reconocimiento Óptico de Caracteres y Traductor")
st.subheader("Elige la fuente de la imagen; puede ser desde la cámara o cargando un archivo")

cam_ = st.checkbox("Usar Cámara", value=False)
img_file_buffer = st.camera_input("Toma una Foto") if cam_ else None

with st.sidebar:
    st.subheader("Procesamiento de Cámara")
    filtro = st.radio("Filtro para imagen con cámara", ('Sí', 'No'), index=1)

bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='Imagen Cargada.', use_column_width=True)
    
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())
    
    st.success(f"Imagen guardada como {uploaded_file.name}")
    img_cv = cv2.imread(uploaded_file.name)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("### Texto Extraído")
    st.write(f"**{text}**")

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("### Texto Extraído de la Imagen de la Cámara")
    st.write(f"**{text}**")

# Opciones de traducción en la barra lateral
with st.sidebar:
    st.subheader("Parámetros de Traducción")
    
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass
    
    translator = Translator()
    input_language = st.selectbox("Seleccione el idioma de entrada", ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"))
    input_language_code = {'Inglés': 'en', 'Español': 'es', 'Bengalí': 'bn', 'Coreano': 'ko', 'Mandarín': 'zh-cn', 'Japonés': 'ja'}[input_language]

    output_language = st.selectbox("Seleccione el idioma de salida", ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"))
    output_language_code = {'Inglés': 'en', 'Español': 'es', 'Bengalí': 'bn', 'Coreano': 'ko', 'Mandarín': 'zh-cn', 'Japonés': 'ja'}[output_language]

    accent = st.selectbox("Seleccione el acento para inglés", ("Por Defecto", "India", "Reino Unido", "Estados Unidos", "Canadá", "Australia", "Irlanda", "Sudáfrica"))
    accent_code = {"Por Defecto": "com", "India": "co.in", "Reino Unido": "co.uk", "Estados Unidos": "com", "Canadá": "ca", "Australia": "com.au", "Irlanda": "ie", "Sudáfrica": "co.za"}[accent]

    display_output_text = st.checkbox("Mostrar Texto Traducido", value=True)

    if st.button("Convertir"):
        result, output_text = text_to_speech(input_language_code, output_language_code, text, accent_code)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tu Audio:")
        st.audio(audio_bytes, format="audio/mp3")

        if display_output_text:
            st.markdown(f"## Texto Traducido:")
            st.write(f"**{output_text}**")





 
    
    
