import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Speech Recognition App", page_icon="🎤")

st.title("🎙️ Speech-to-Text + Summary App")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

audio_file = st.file_uploader("Upload an audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if audio_file:
    st.audio(audio_file)

    # --- TRANSCRIBE ---
    with st.spinner("Transcribing with Whisper..."):
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    text = transcription.text
    st.subheader("📝 Transcription")
    st.write(text)

    # --- SUMMARY ---
    with st.spinner("Summarizing..."):
        summary_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize this text clearly."},
                {"role": "user", "content": text}
            ]
        )

    summary = summary_resp.choices[0].message["content"]

    st.subheader("📌 Summary")
    st.write(summary)

    # --- DOWNLOAD BUTTONS ---
    st.download_button("⬇️ Download Transcription", text, "transcription.txt")
    st.download_button("⬇️ Download Summary", summary, "summary.txt")
