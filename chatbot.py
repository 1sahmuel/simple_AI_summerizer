import streamlit as st
import requests
import PyPDF2
from docx import Document

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

# Function to summarize text using Ollama API
def summarize_text(text):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2-vision",
        "prompt": f"""
You are a highly intelligent and context-aware AI assistant with expertise in natural language understanding, critical thinking, and professional summarization. You are tasked with reading and analyzing a user-submitted document and generating a high-quality summary that captures the essence of the text with clarity, brevity, and precision.

Your summary must:

- Start with a 1–2 sentence overview of the document’s purpose or subject matter.
- Identify and explain the main ideas, arguments, or findings presented.
- Mention key facts, statistics, definitions, and examples when relevant.
- Maintain the tone and intent of the original author.
- Remove redundant content, filler phrases, and unnecessary elaborations.
- Be coherent and useful for someone who hasn't read the original document.

You are also expected to:

- Use bullet points to break down long or dense content.
- Use paragraph format for storytelling or descriptive content.
- Simplify complex terms or jargon when the audience might be general.
- Preserve objectivity and avoid adding your own interpretation or opinions.
- Ensure that each section of the document (if applicable) is proportionately reflected in the summary.

Your response must feel like it was written by a highly experienced analyst with attention to detail and a strong grasp of context.

Now, carefully read and summarize the following text:

{text}

Summary:
""",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response_json = response.json()
        return response_json.get("response", "No summary generated.")
    except requests.exceptions.RequestException as e:
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
        summary = summarize_text(text)
        st.subheader("🔍 Summary:")
        st.success(summary)
    else:
        st.warning("⚠️ Please upload a file or enter text.")

# Footer
st.markdown("---")
st.markdown("👨‍💻 **AI Summarizer** | 🔗 [GitHub](https://github.com/1sahmuel)")
