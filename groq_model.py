import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
import PyPDF2
from docx import Document

# Set your Groq API Key here (for testing, you can hardcode it — but use env vars in production)
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your_groq_api_key_here"

# Set Page Config
st.set_page_config(page_title="AI Text Summarizer", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stButton button { background-color: #4CAF50; color: white; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg", width=100)
st.sidebar.title("⚡ AI Summarizer")
st.sidebar.markdown("Summarize your text or documents in seconds.")

# Main Header
st.title("📄 AI-Powered Text Summarizer")
st.write("Summarize PDF, DOCX, or typed text instantly!")

# Function to extract text from different file types
def extract_text(file):
    file_type = file.name.split(".")[-1].lower()
    text = ""
    
    if file_type == "pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    elif file_type == "docx":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file format! Please upload a PDF or DOCX file.")
        return None
    
    return text

# Function to summarize text using Groq API
def summarize_text(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Simplified prompt
    prompt = f"""
Summarize the following text in a single, well-constructed sentence, capturing the main ideas, key arguments, and significant details. Ensure the summary is clear, concise, and written in a neutral tone, preserving the original intent of the text without adding personal opinions, while avoiding redundant or minor details. Start the summary directly without any introductory phrases like 'Summary:'. Text to summarize:
{text}
"""

    payload = {
        "model": "llama-3.3-70b-versatile",  
        "messages": [
            {"role": "system", "content": "You are an expert summarizer AI."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2048,
        "top_p": 1,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API Error: {str(e)}"

# File Upload and Text Input
uploaded_file = st.file_uploader("📂 Upload a file (PDF/DOCX)", type=["pdf", "docx"])
text_input = st.text_area("📝 Or type/paste text here:", height=250)

text = ""
if uploaded_file:
    text = extract_text(uploaded_file)
    if text:
        st.success("✅ File uploaded successfully!")
elif text_input:
    text = text_input

# Summary Button
if st.button("📝 Generate Summary"):
    if text:
        with st.spinner("🧠 Summarizing..."):
            summary = summarize_text(text)
        st.subheader("🔍 Summary:")
        st.text_area("Summary Output", summary, height=300)
        st.download_button("⬇️ Download Summary", summary, file_name="summary.txt")
    else:
        st.warning("⚠️ Please upload a file or enter text.")

# Footer
st.markdown("---")
st.markdown("👨‍💻 **AI Summarizer** | 🔗 [GitHub](https://github.com/1sahmuel)")
