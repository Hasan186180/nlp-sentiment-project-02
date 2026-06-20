#streamlit_app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Set Page Config
st.set_page_config(
    page_title="AI Duygu Analiz Sistemi",
    page_icon="🧠",
    layout="centered"
)

# Inject CSS for stunning aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Dark elegant background */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
        font-family: 'Outfit', sans-serif;
        color: #f3f4f6;
    }
    
    /* Title gradient */
    .title-text {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa 0%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
        padding-top: 10px;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        color: #9ca3af;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Glassmorphic cards */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 25px;
        backdrop-filter: blur(12px);
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* Custom Button styling */
    div.stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        height: auto !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.45) !important;
        background: linear-gradient(90deg, #4f46e5 0%, #9333ea 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Text Area Styling */
    .stTextArea textarea {
        background: rgba(17, 24, 39, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #f3f4f6 !important;
        font-size: 1.05rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.2) !important;
    }

    /* Result box styling */
    .result-container {
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.02);
    }
    
    .sentiment-label-pos {
        font-size: 1.5rem;
        font-weight: 700;
        color: #34d399;
        text-align: center;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.2);
    }
    
    .sentiment-label-neg {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f87171;
        text-align: center;
        text-shadow: 0 0 10px rgba(248, 113, 113, 0.2);
    }

    .footer {
        text-align: center;
        color: #4b5563;
        font-size: 0.85rem;
        margin-top: 40px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="title-text">🧠 AI Müşteri Yorum Analizi</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Müşteri geri bildirimlerinin duygusal tonunu saniyeler içinde analiz edin.</div>', unsafe_allow_html=True)

# Main Input Container
st.markdown('<div class="card">', unsafe_allow_html=True)

text = st.text_area(
    "Analiz edilecek müşteri yorumunu buraya yazın veya yapıştırın:",
    height=160,
    placeholder="Örn: Ürünü çok beğendim, kargo çok hızlıydı ve satıcı çok ilgiliydi. Kesinlikle tavsiye ederim!"
)

API_URL = "http://127.0.0.1:8000/predict"
API_KEY = os.getenv("API_KEY", "sentiment_analysis_secure_key_2026")

st.markdown('</div>', unsafe_allow_html=True)

if st.button("Duygu Durumunu Analiz Et"):
    if not text.strip():
        st.warning("Lütfen analiz etmek için bir metin girin.")
    else:
        headers = {"x-api-key": API_KEY}
        with st.spinner("Yapay zeka yorumu analiz ediyor..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"text": text},
                    headers=headers
                )

                if response.status_code == 200:
                    result = response.json()
                    pos = result['positive']
                    neg = result['negative']
                    
                    st.success("Analiz tamamlandı!")
                    
                    # Columns for metrics
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Pozitif Oran", f"{pos:.2%}")
                    with col2:
                        st.metric("Negatif Oran", f"{neg:.2%}")
                    
                    # Verdict
                    st.divider()
                    if pos > neg:
                        st.markdown('<div class="sentiment-label-pos">😊 Pozitif Duygu Durumu</div>', unsafe_allow_html=True)
                        st.write("")
                        st.markdown("<p style='text-align: center; color: #9ca3af;'>Bu müşteri yorumu genel olarak <strong>olumlu</strong> bir deneyimi ve memnuniyeti ifade ediyor.</p>", unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="sentiment-label-neg">😔 Negatif Duygu Durumu</div>', unsafe_allow_html=True)
                        st.write("")
                        st.markdown("<p style='text-align: center; color: #9ca3af;'>Bu müşteri yorumu genel olarak <strong>olumsuz</strong> bir deneyimi, şikayeti veya memnuniyetsizliği ifade ediyor.</p>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                elif response.status_code == 401:
                    st.error("API Anahtarı hatası (Unauthorized). Lütfen .env dosyanızı veya API Key ayarınızı kontrol edin.")
                else:
                    st.error(f"API hatası oluştu. Durum Kodu: {response.status_code}")
            except Exception as e:
                st.error(f"Backend sunucusuna bağlanılamadı. Lütfen sunucunun (FastAPI) çalıştığından emin olun. Hata detayı: {e}")

# Footer
st.markdown("""
<div class="footer">
    <p>AI Destekli Müşteri Yorum Analiz Sistemi &copy; 2026</p>
    <p style="font-size: 11px; color: #4b5563;">Altyapı: DistilBERT (PyTorch) | FastAPI | Streamlit</p>
</div>
""", unsafe_allow_html=True)

