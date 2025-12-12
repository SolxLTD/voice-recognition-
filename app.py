import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎙️ Speech-to-Text + Summary App")

audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])

if audio_file:
    st.audio(audio_file)

    with st.spinner("Transcribing..."):
        # Read the uploaded file as bytes
        audio_bytes = audio_file.read()
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_bytes
        )

    text = transcription.text
    st.subheader("Transcription")
    st.write(text)
