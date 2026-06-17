import streamlit as st
import requests
from PIL import Image
import os
from datetime import datetime

st.set_page_config(page_title="Osaka Expat Helper", page_icon="🏯", layout="wide")

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #764ba2;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏯 Osaka Expat Helper</h1><p>Your AI assistant for Japanese documents</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📋 How It Works")
    st.markdown("1. Upload document photo\n2. AI analyzes\n3. Get translation")
    st.markdown("### 📞 Contact")
    st.markdown("support@osaka-expat-helper.com")

uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)
    
    if st.button("🚀 Translate Document", use_container_width=True):
        with st.spinner("Analyzing with AI..."):
            try:
                backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000")
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{backend_url}/translate", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("---")
                    st.markdown("### 📝 Summary")
                    st.markdown(f'<div class="result-box">{result["summary"]}</div>', unsafe_allow_html=True)
                    
                    if result["key_actions"]:
                        st.markdown("### ✅ Key Actions")
                        st.info(result["key_actions"])
                    
                    if result["deadline"] and result["deadline"] != "Not specified":
                        st.markdown(f"### ⏰ Deadline: {result['deadline']}")
                        st.warning(f"⚠️ {result['deadline']}")
                    
                    with st.expander("📖 Full Translation"):
                        st.write(result["english_translation"])
                    
                    with st.expander("🇯🇵 Original Text"):
                        st.write(result["original_text"])
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")