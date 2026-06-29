import streamlit as st
st.set_page_config(page_title="Debug Sprint", layout="wide", initial_sidebar_state="collapsed")

# --- DARK THEME FORCE ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FA; }
    h1, h2, h3, h4, h5, p, label, div { color: #FA !important; }
    .st-emotion-cache-1c7y2kd { background-color: #262730; } /* Tabs bg */
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 10px; border: 0px; }
    .stButton>button:hover { background-color: #FF6B6B; }
    .stTextArea textarea { background-color: #262730; color: #FA; border: 1px solid #4B4B4B; }
    .stCodeBlock { border: 1px solid #4B4B4B; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

import requests
import json
import uuid
import random
from datetime import datetime

# --- CONFIG ---
SHEET_URL = "https://script.google.com/macros/s/AKfycby9zPW3-W2rKahjprHoF6KlwZ1JC_BCqJ8Jh9mc2Y_6Gkp5mpqHeqMZLppYxTqL_TuC/exec" 
ADMIN_PASS = "aL!9zX#2pQ" 

# --- BUG DATA ---
BUGS = [
    {"code": "print('Hello' ", "fix": "print('Hello')", "hint": "Bracket close karo )"},
    {"code": "x = 5\nprint(x", "fix": "x = 5\nprint(x)", "hint": "Last bracket missing )"},
    {"code": "for i in range(5\n print(i)", "fix": "for i in range(5):\n print(i)", "hint": ") aur : dono missing"},
    {"code": "if x = 5:", "fix": "if x == 5:", "hint": "= ke bajaye == lagta hai check karne ke liye"},
    {"code": "my_list = [1,2,3\nprint(my_list)", "fix": "my_list = [1,2,3]\nprint(my_list)", "hint": "] square bracket missing hai"},
    {"code": "def test\n print('ok')", "fix": "def test():\n print('ok')", "hint": "() aur : missing hai function mein"},
]

# --- FUNCTIONS ---
def init_state():
    if 'player_id' not in st.session_state:
        st.session_state.player_id = str(uuid.uuid4())[:8]
        st.session_state.xp = 0
        st.session_state.level = 1
        st.session_state.current_bug = random.choice(BUGS)

def send_data(xp, level):
    data = {"time": datetime.now().isoformat(), "player_id": st.session_state.player_id, "xp": xp, "level": level}
    try:
        requests.post(SHEET_URL, json=data, timeout=5)
    except:
        pass # Agar net na ho to bhi game crash na ho

# --- UI ---
init_state()

st.title("🐛 Debug Sprint v1.0")
st.caption("Pakistan's 1st Anonymous Bug Fixing Game")
st.markdown(f"**Player ID:** `{st.session_state.player_id}` | **Level:** {st.session_state.level} | **XP:** {st.session_state.xp}")
st.divider()

tab1, tab2 = st.tabs(["🎮 Play", "🔒 Admin"])

with tab1:
    st.subheader("Bug #1: Syntax Error Fix Karo")
    st.code(st.session_state.current_bug["code"], language="python")
    
    user_fix = st.text_area("Apna sahi code yahan likho:", height=180, placeholder="Example: print('Hello')")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 Hint Lo -5 XP", use_container_width=True):
            st.info(f"Hint: {st.session_state.current_bug['hint']}")
            st.session_state.xp = max(0, st.session_state.xp - 5)
            send_data(st.session_state.xp, st.session_state.level)
            st.rerun()
            
    with col2:
        if st.button("✅ Submit Fix", type="primary", use_container_width=True):
            if user_fix.strip() == st.session_state.current_bug["fix"]:
                st.balloons()
                st.success("Correct! +20 XP Mil gaya")
                st.session_state.xp += 20
                st.session_state.level += 1
                st.session_state.current_bug = random.choice(BUGS)
                send_data(st.session_state.xp, st.session_state.level)
                st.rerun()
            else:
                st.error("Ghalat Hai. Dobara try karo.")

with tab2:
    st.warning("⚠️ Sirf Admin ke liye")
    pass_code = st.text_input("Admin Passcode:", type="password")
    if pass_code == ADMIN_PASS:
        st.success("Access Granted ✅")
        st.info("Saara data dekhne ke liye apni Google Sheet `DebugSprint Data` kholo.")
    elif pass_code:
        st.error("Wrong Passcode ❌")
