import streamlit as st
import requests
import time
import random
import os

# =========================
# BACKEND CONFIG (IMPORTANT)
# =========================
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"  # fallback for local dev
)
API_URL = f"{BACKEND_URL}/convert"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Currency Converter",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM STYLES (SPACING FIXED)
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

/* Reset default margins */
h1, p {
    margin: 0 !important;
    padding: 0 !important;
}

/* App background */
.stApp {
    background: linear-gradient(135deg, #0a0e27, #1a1a2e, #16213e);
    font-family: 'Orbitron', sans-serif;
}

/* Title */
.title {
    background: linear-gradient(90deg, #ffd700, #ffed4e, #ffd700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.8rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 6px;
}

/* Subtitle (NO GAP BELOW) */
.subtitle {
    text-align: center;
    color: #50fa7b;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 18px; /* controlled spacing */
}

/* Floating currency symbols */
.currency-symbol {
    position: fixed;
    font-size: 2rem;
    opacity: 0.15;
    animation: float 18s linear infinite;
    pointer-events: none;
}

@keyframes float {
    0% { transform: translateY(100vh) rotate(0deg); }
    100% { transform: translateY(-100vh) rotate(360deg); }
}

/* Main container */
.main-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 28px;
    padding: 40px;
    backdrop-filter: blur(16px);
    border: 2px solid rgba(255, 215, 0, 0.3);
    box-shadow: 0 0 40px rgba(0,0,0,0.5);
    max-width: 850px;
    margin: auto;
}

/* Input */
.stTextInput input {
    background: rgba(0,0,0,0.4);
    border: 2px solid #ffd700;
    border-radius: 16px;
    color: white;
    font-size: 1.1rem;
    padding: 14px;
}

/* Button */
.stButton button {
    background: linear-gradient(135deg, #ffd700, #50fa7b);
    border-radius: 18px;
    font-size: 1.3rem;
    font-weight: 900;
    padding: 14px;
    width: 100%;
    border: none;
    color: black;
    cursor: pointer;
}

.stButton button:hover {
    transform: scale(1.04);
}

/* Footer text */
.footer {
    text-align: center;
    color: #888;
    font-size: 0.9rem;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FLOATING SYMBOLS
# =========================
symbols = ['$', '€', '£', '¥', '₹', '₽', '₩', '₪']
for _ in range(7):
    st.markdown(
        f"<div class='currency-symbol' style='left:{random.randint(5,95)}%; animation-delay:{random.randint(0,10)}s'>{random.choice(symbols)}</div>",
        unsafe_allow_html=True
    )

# =========================
# HEADER (NO EXTRA SPACE)
# =========================
st.markdown("<div class='title'>💰 CURRENCY EXCHANGE 💰</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>💸 Real-Time Global Currency Conversion Powered by AI 💸</div>", unsafe_allow_html=True)

# =========================
# MAIN UI
# =========================
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

with st.expander("💡 Quick Examples"):
    st.markdown("""
- Convert 100 USD to INR  
- How much is 50 EUR in JPY?  
- Convert 250 AUD to USD  
""")

query = st.text_input(
    "💱 Enter your conversion request",
    "Convert 100 USD to INR"
)

if st.button("💸 CONVERT NOW"):
    with st.spinner("Calculating exchange rate..."):
        try:
            time.sleep(0.6)
            res = requests.post(API_URL, json={"query": query}, timeout=15)

            if res.status_code == 200:
                result = res.json().get("result", "No result")
                st.success(f"✅ {result}")
                st.balloons()
            else:
                st.error(f"❌ Backend error ({res.status_code})")

        except requests.exceptions.ConnectionError:
            st.error("🔌 Backend not reachable. Check BACKEND_URL.")
        except Exception as e:
            st.error(str(e))

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("<div class='footer'>🏦 Built with FastAPI • LangChain • Streamlit</div>", unsafe_allow_html=True)
