import streamlit as st
from openai import OpenAI

client = OpenAI()

st.title("🎙️ Speech to Text + Summary App")

st.write("Upload an audio file, and the app will transcribe + summarize it.")

audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])

if audio_file:
    st.audio(audio_file)
    
    st.write(" Transcribing... please wait")

    
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    text = transcription.text
    st.subheader("Transcription")
    st.write(text)

    
    st.subheader(" Summary")
    summary_prompt = f"Summarize this text in simple terms:\n\n{text}"

    summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize text clearly and simply."},
            {"role": "user", "content": summary_prompt}
        ]
    ).choices[0].message["content"]

    st.write(summary)

    
    st.download_button(" Download Transcription", text, file_name="transcription.txt")
    st.download_button(" Download Summary", summary, file_name="summary.txt")
