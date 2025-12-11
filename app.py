import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎙️ Speech to Text + Summary App")

audio_file = st.file_uploader("Upload an audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if audio_file:
    st.audio(audio_file)
    
    with st.spinner("Transcribing..."):
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    text = transcription.text
    st.subheader(" Transcription")
    st.write(text)

    
    with st.spinner("Summarizing..."):
        summary = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the text clearly."},
                {"role": "user", "content": text}
            ]
        ).choices[0].message["content"]

    st.subheader("📌 Summary")
    st.write(summary)

    
    st.download_button("Download Transcription", text, "transcription.txt")
    st.download_button("Download Summary", summary, "summary.txt")
