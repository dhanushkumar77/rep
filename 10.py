import streamlit as st
import PyPDF2
import os
import re
from collections import Counter

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    return Counter(words).most_common(20)

st.title("10th Class NCERT & Question Paper Analyzer")

# Upload NCERT textbook
st.header("📘 Upload NCERT Textbook (PDF)")
textbook = st.file_uploader("Upload textbook PDF", type="pdf")

# Upload Past Year Papers
st.header("📄 Upload Past Year Question Papers (3 PDFs)")
qps = st.file_uploader("Upload question papers", type="pdf", accept_multiple_files=True)

if textbook and qps:
    st.subheader("Analyzing...")
    
    # Extract textbook keywords
    textbook_text = extract_text_from_pdf(textbook)
    textbook_keywords = get_keywords(textbook_text)
    
    # Extract keywords from question papers
    all_qp_text = ""
    for qp in qps:
        all_qp_text += extract_text_from_pdf(qp)
    qp_keywords = get_keywords(all_qp_text)
    
    st.markdown("### 🔑 Common Important Topics:")
    common = set([k for k, v in textbook_keywords]) & set([k for k, v in qp_keywords])
    for word in common:
        st.write(f"✅ {word}")
    
    st.markdown("### 📘 Textbook Keywords:")
    st.write([k for k, v in textbook_keywords])
    
    st.markdown("### 📝 Question Paper Keywords:")
    st.write([k for k, v in qp_keywords])
