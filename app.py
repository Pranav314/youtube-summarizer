import streamlit as st
from summarizer import get_transcript, chunk_text, summarize

st.set_page_config(page_title="YT Summarizer", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0f0f0f;
        color: #f0f0f0;
    }
    .main { padding: 2rem; }
    h1 {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4d4d, #ff9a3c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        color: #f0f0f0;
        padding: 0.8rem 1rem;
        font-size: 0.95rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff4d4d, #ff9a3c);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton>button:hover { opacity: 0.85; }
    .summary-box {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-top: 1.5rem;
        line-height: 1.8;
        font-size: 0.95rem;
        color: #e0e0e0;
    }
    .stAlert { border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>YT Summarizer</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Paste any YouTube URL and get an instant AI summary.</p>', unsafe_allow_html=True)

url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...")
clicked = st.button("Summarize")

try:
    if clicked:
        if not url:
            st.warning("Please enter a YouTube URL first.")
        else:
            with st.spinner("Fetching transcript and summarizing..."):
                transcript = get_transcript(url)
                if transcript:
                    chunks = chunk_text(transcript, 8000)
                    mini_summaries = []
                    for chunk in chunks:
                        mini_summaries.append(summarize(chunk))
                    final_summary = summarize(" ".join(mini_summaries))
                    st.markdown(f'<div class="summary-box">{final_summary}</div>', unsafe_allow_html=True)
                else:
                    st.error("Couldn't fetch transcript. Try a video with captions enabled.")
except Exception as e:
    st.error(f"Something went wrong. Please try again after few minutes")