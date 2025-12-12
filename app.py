import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="Speech Recognition App", page_icon="🎤")
st.title("🎙️ Speech-to-Text App (Streamlit Cloud Compatible)")

st.write("""
Upload an audio file (wav or mp3), choose your language, and select the recognition API. 
The app will transcribe your audio and allow you to save the transcription.
""")

# --- Sidebar options ---
st.sidebar.header("Settings")
language = st.sidebar.selectbox(
    "Choose Language", 
    options=["en-US", "fr-FR", "es-ES", "de-DE", "pt-BR"]
)

api_option = st.sidebar.selectbox(
    "Choose API",
    options=["Google Speech Recognition", "Sphinx (offline)"]
)

uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

if uploaded_file:
    st.audio(uploaded_file)
    
    # --- Transcription ---
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_filename = tmp_file.name

    try:
        with sr.AudioFile(tmp_filename) as source:
            audio_data = r.record(source)
            st.info("Transcribing...")
            
            if api_option == "Google Speech Recognition":
                text = r.recognize_google(audio_data, language=language)
            elif api_option == "Sphinx (offline)":
                text = r.recognize_sphinx(audio_data)
            else:
                text = ""
        
        st.subheader("📝 Transcription")
        st.write(text)

        # --- Save transcription ---
        st.download_button(
            "⬇️ Download Transcription",
            text,
            file_name="transcription.txt"
        )

    except sr.UnknownValueError:
        st.error("⚠️ Could not understand the audio. Try again with clearer audio.")
    except sr.RequestError as e:
        st.error(f"⚠️ API request error: {e}")
    finally:
        os.remove(tmp_filename)
