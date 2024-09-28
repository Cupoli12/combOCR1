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

# Improved text-to-speech function
def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[0:20] if text else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# Remove old mp3 files
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

# Streamlit app layout and customization
st.set_page_config(page_title="OCR & Translator", page_icon="🌐", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #F0F2F6;
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

st.title("🌐 Optical Character Recognition & Translator")
st.subheader("Choose the source of the image, it can be from the camera or by uploading a file")

cam_ = st.checkbox("Use Camera", value=False)
img_file_buffer = st.camera_input("Take a Photo") if cam_ else None

with st.sidebar:
    st.subheader("Camera Processing")
    filtro = st.radio("Filter for camera image", ('Yes', 'No'), index=1)

bg_image = st.file_uploader("Upload an Image:", type=["png", "jpg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())
    
    st.success(f"Image saved as {uploaded_file.name}")
    img_cv = cv2.imread(uploaded_file.name)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("### Extracted Text")
    st.write(f"**{text}**")

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Yes':
        cv2_img = cv2.bitwise_not(cv2_img)
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("### Extracted Text from Camera Image")
    st.write(f"**{text}**")

# Sidebar for translation options
with st.sidebar:
    st.subheader("Translation Parameters")
    
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass
    
    translator = Translator()
    input_language = st.selectbox("Select Input Language", ("English", "Spanish", "Bengali", "Korean", "Mandarin", "Japanese"))
    input_language_code = {'English': 'en', 'Spanish': 'es', 'Bengali': 'bn', 'Korean': 'ko', 'Mandarin': 'zh-cn', 'Japanese': 'ja'}[input_language]

    output_language = st.selectbox("Select Output Language", ("English", "Spanish", "Bengali", "Korean", "Mandarin", "Japanese"))
    output_language_code = {'English': 'en', 'Spanish': 'es', 'Bengali': 'bn', 'Korean': 'ko', 'Mandarin': 'zh-cn', 'Japanese': 'ja'}[output_language]

    accent = st.selectbox("Select English Accent", ("Default", "India", "UK", "US", "Canada", "Australia", "Ireland", "South Africa"))
    accent_code = {"Default": "com", "India": "co.in", "UK": "co.uk", "US": "com", "Canada": "ca", "Australia": "com.au", "Ireland": "ie", "South Africa": "co.za"}[accent]

    display_output_text = st.checkbox("Show Translated Text", value=True)

    if st.button("Convert"):
        result, output_text = text_to_speech(input_language_code, output_language_code, text, accent_code)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Your Audio:")
        st.audio(audio_bytes, format="audio/mp3")

        if display_output_text:
            st.markdown(f"## Translated Text:")
            st.write(f"**{output_text}**")





 
    
    
