import streamlit as st
import os
import fitz
import io

@st.cache_data
def load_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def load_txt(file_bytes):
    return file_bytes.decode('utf-8')

def process_uploaded_files(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        file_bytes = uploaded_file.getvalue()
        
        if filename.endswith('.pdf'):
            content = load_pdf(file_bytes)
        elif filename.endswith('.txt'):
            content = load_txt(file_bytes)
        else:
            content = "Nieobsługiwany plik"
        
        documents.append({"filename": filename, "content": content[:500] + "..." if len(content) > 500 else content})
    return documents

st.set_page_config(page_title="Chat z plikami", layout="wide")

# Panel boczny
with st.sidebar:
    st.header("Wgrywanie plików")
    uploaded_files = st.file_uploader(
        "Wybierz plik",
        accept_multiple_files=True,
        type=None
    )
    
    if uploaded_files:
        documents = process_uploaded_files(uploaded_files)
        st.subheader("Wgrane pliki")
        for doc in documents:
            with st.expander(doc["filename"]):
                st.text_area("Podgląd", doc["content"], height=200)
        
        if 'documents' not in st.session_state:
            st.session_state.documents = []
        st.session_state.documents = documents
        
        st.success(f"Wgrano {len(documents)} plików!")

st.header("Chat z dokumentami")
if 'documents' in st.session_state and st.session_state.documents:
    st.info(f"Dostępne dokumenty: {', '.join([d['filename'] for d in st.session_state.documents])}")
else:
    st.warning("Wgraj pliki w bocznym panelu")

if prompt := st.chat_input("Wpisz wiadomość..."):
    st.chat_message("user").write(prompt)
