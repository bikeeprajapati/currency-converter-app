import streamlit as st
import requests
import time
import random

API_URL = "http://localhost:8000/convert"

# Page config
st.set_page_config(
    page_title="AI Currency Converter",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with money/financial theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Animated money background */
    .stApp::before {
        content: '💵 💶 💷 💴 💰 💸 💵 💶 💷 💴 💰 💸';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        font-size: 3rem;
        opacity: 0.03;
        animation: float 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg); }
        100% { transform: translateY(-100vh) rotate(360deg); }
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(90deg, #ffd700 0%, #ffed4e 50%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 0rem !important;
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.5);
        animation: shimmer 3s ease-in-out infinite;
        letter-spacing: 2px;
    }
    
    @keyframes shimmer {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.3); }
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #50fa7b;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(80, 250, 123, 0.5);
    }
    
    /* Currency symbols floating */
    .currency-symbol {
        position: fixed;
        font-size: 2rem;
        opacity: 0.15;
        animation: drift 15s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes drift {
        0% { transform: translateY(100vh) translateX(0) rotate(0deg); }
        100% { transform: translateY(-100vh) translateX(50px) rotate(720deg); }
    }
    
    /* Input box styling */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.4);
        border: 2px solid #ffd700;
        border-radius: 20px;
        color: #ffffff;
        font-size: 1.2rem;
        padding: 18px 25px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        font-family: 'Orbitron', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #50fa7b;
        box-shadow: 0 0 30px rgba(80, 250, 123, 0.6), 
                    0 0 60px rgba(255, 215, 0, 0.3);
        background: rgba(0, 0, 0, 0.6);
        transform: scale(1.02);
    }
    
    /* Button styling - money theme */
    .stButton > button {
        background: linear-gradient(135deg, #ffd700 0%, #50fa7b 100%);
        color: #000000;
        border: 3px solid #ffd700;
        border-radius: 20px;
        padding: 18px 60px;
        font-size: 1.4rem;
        font-weight: 900;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.6),
                    inset 0 -3px 10px rgba(0, 0, 0, 0.2);
        width: 100%;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.8),
                    0 0 50px rgba(80, 250, 123, 0.5);
        border-color: #50fa7b;
    }
    
    .stButton > button:active {
        transform: translateY(0px) scale(0.98);
    }
    
    /* Success message - cash register style */
    .stSuccess {
        background: linear-gradient(135deg, rgba(80, 250, 123, 0.2) 0%, rgba(80, 250, 123, 0.05) 100%);
        border: 2px solid #50fa7b;
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(10px);
        animation: cashRegister 0.5s ease-out;
        box-shadow: 0 0 30px rgba(80, 250, 123, 0.3);
    }
    
    @keyframes cashRegister {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Error message */
    .stError {
        background: linear-gradient(135deg, rgba(255, 85, 85, 0.2) 0%, rgba(255, 85, 85, 0.05) 100%);
        border: 2px solid #ff5555;
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(255, 85, 85, 0.3);
    }
    
    /* Container styling - vault style */
    .main-container {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.08) 0%, rgba(80, 250, 123, 0.05) 100%);
        border-radius: 30px;
        padding: 50px;
        backdrop-filter: blur(20px);
        border: 3px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5),
                    inset 0 0 40px rgba(255, 215, 0, 0.1);
        margin: 20px auto;
        max-width: 900px;
        position: relative;
        overflow: hidden;
    }
    
    .main-container::before {
        content: '💰';
        position: absolute;
        top: -30px;
        right: -30px;
        font-size: 15rem;
        opacity: 0.05;
        transform: rotate(15deg);
    }
    
    /* Label styling */
    .stTextInput > label, .stSelectbox > label {
        color: #ffd700 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Metrics styling - money counters */
    [data-testid="stMetricValue"] {
        color: #50fa7b;
        font-size: 2rem;
        font-weight: 900;
        text-shadow: 0 0 15px rgba(80, 250, 123, 0.8);
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffd700;
        font-weight: 700;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 215, 0, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        color: #ffd700 !important;
        font-weight: 700;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #ffd700 !important;
        border-right-color: #50fa7b !important;
    }
    
    /* Coins falling animation */
    @keyframes coinFall {
        0% { 
            transform: translateY(-100px) rotate(0deg);
            opacity: 0;
        }
        50% { opacity: 1; }
        100% { 
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
    
    .coin {
        position: fixed;
        font-size: 2rem;
        animation: coinFall 5s linear;
        pointer-events: none;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

# Add floating currency symbols
symbols = ['$', '€', '£', '¥', '₹', '₽', '₩', '₪']
for i in range(8):
    st.markdown(
        f'<div class="currency-symbol" style="left: {random.randint(10, 90)}%; animation-delay: {random.randint(0, 10)}s;">{random.choice(symbols)}</div>',
        unsafe_allow_html=True
    )

# Header with money bag emoji
st.markdown("<h1>💰 CURRENCY EXCHANGE 💰</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>💸 Real-Time Global Currency Conversion Powered by AI 💸</p>", unsafe_allow_html=True)

# Main container
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # Example queries with money emoji
    with st.expander("💡 Quick Examples", expanded=False):
        st.markdown("""
        💵 **Convert 100 USD to INR**  
        💶 **How much is 50 EUR in JPY?**  
        💷 **What's 1000 GBP in CAD?**  
        💴 **Convert 250 AUD to USD**  
        💰 **Exchange 500 CHF to EUR**
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input field
    query = st.text_input(
        "💱 Enter Your Conversion Request:",
        "Convert 100 USD to INR",
        help="Type your currency conversion in natural language"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Convert button
    if st.button("💸 CONVERT NOW 💸"):
        # Add coin falling effect
        st.markdown(f'<div class="coin" style="left: {random.randint(20, 80)}%;">💰</div>', unsafe_allow_html=True)
        
        with st.spinner(" Calculating exchange rate..."):
            try:
                time.sleep(0.8)  # Dramatic pause
                
                res = requests.post(API_URL, json={"query": query}, timeout=10)
                
                if res.status_code == 200:
                    data = res.json()
                    result = data.get("result", "No result found")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.success(f"✅ {result}")
                    
                    # Money metrics
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("💹 Status", "SUCCESS", delta="✓")
                    with col_b:
                        st.metric("⚡ Speed", "< 1s", delta="Fast")
                    with col_c:
                        st.metric("🎯 Rate", "Live", delta="Real-time")
                    
                    # Celebration effect
                    st.balloons()
                else:
                    st.error(f"❌ Error {res.status_code}: Transaction Failed")
                    with st.expander("🔍 Error Details"):
                        st.code(res.text)
                        
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to API. Ensure backend is running on localhost:8000")
            except Exception as e:
                st.error(f"⚠️ Transaction Error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Stats footer
st.markdown("<br><br>", unsafe_allow_html=True)
stat1, stat2, stat3, stat4 = st.columns(4)
with stat1:
    st.markdown("<p style='text-align: center; color: #ffd700; font-size: 1.2rem; font-weight: 700;'>💱 150+ Currencies</p>", unsafe_allow_html=True)
with stat2:
    st.markdown("<p style='text-align: center; color: #50fa7b; font-size: 1.2rem; font-weight: 700;'>⚡ Real-Time Rates</p>", unsafe_allow_html=True)
with stat3:
    st.markdown("<p style='text-align: center; color: #ffd700; font-size: 1.2rem; font-weight: 700;'>🤖 AI Powered</p>", unsafe_allow_html=True)
with stat4:
    st.markdown("<p style='text-align: center; color: #50fa7b; font-size: 1.2rem; font-weight: 700;'>🔒 Secure</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 0.9rem;'>🏦 Built with FastAPI • LangChain • Streamlit 🏦</p>",
    unsafe_allow_html=True
)