import streamlit as st
import requests
import json
import uuid
import random
from datetime import datetime

st.set_page_config(page_title="Debug Sprint Game", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FA; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 10px; border: 0px; }
    .stButton>button:hover { background-color: #FF6B6B; }
    .stTextArea textarea { background-color: #262730; color: #FA; border: 1px solid #4B4B4B; }
    .stCodeBlock { border: 1px solid #4B4B4B; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# --- CONFIG ---
SHEET_URL = "https://script.google.com/macros/s/AKfycby9iP43-M2rKahJprHoF6KIwZ13C_BCq3B2h9mc2Y_6GkpSapgHeqKZLpYfxTql_TuC/exec"
ADMIN_PASS = "aL!9zX#2pQ"

# --- BUG DATA ---
BUGS = [
    {"code": "print('Hello'", "fix": "print('Hello')", "hint": "Close the bracket ')'"},
    {"code": "x = 5\\nprint(x)", "fix": "x = 5\nprint(x)", ...}
    {"code": "for i in range(5)\n print(i)", "fix": "for i in range(5):\n print(i)", "hint": "Both ')' and ':' are missing"},
    {"code": "if x = 5:", "fix": "if x == 5:", "hint": "Use '==' for comparison instead of '='"},
    {"code": "my_list = [1,2,3\nprint(my_list)", "fix": "my_list = [1,2,3]\nprint(my_list)", "hint": "']' square bracket is missing"},
    {"code": "def test\n print('ok')", "fix": "def test():\n print('ok')", "hint": "'()' and ':' are missing in function definition"},
]

# --- FUNCTIONS ---
def init_state():
    if 'player_id' not in st.session_state:
        st.session_state.player_id = str(uuid.uuid4())[:8]
        st.session_state.xp = 0
        st.session_state.level = 1
        st.session_state.current_bug = random.choice(BUGS)

def send_to_sheet(bug_id, score):
    payload = {
        "player_id": st.session_state.player_id,
        "bug_id": bug_id,
        "score": score,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        requests.post(SHEET_URL, data=json.dumps(payload), timeout=5)
    except Exception as e:
        st.error(f"Failed to send data: {e}")

def next_bug():
    st.session_state.current_bug = random.choice(BUGS)
    st.session_state.xp += 10
    if st.session_state.xp >= st.session_state.level * 50:
        st.session_state.level += 1

# --- APP UI ---
init_state()

st.title("🐛 Debug Sprint Game")
st.caption(f"Player ID: `{st.session_state.player_id}` | Level: {st.session_state.level} | XP: {st.session_state.xp}")

st.subheader("Fix This Bug:")
st.code(st.session_state.current_bug["code"], language="python")

user_fix = st.text_area("Write your fixed code here:", height=150, key="fix_box")

col1, col2 = st.columns(2)
with col1:
    if st.button("Submit Fix"):
        if user_fix.strip() == st.session_state.current_bug["fix"].strip():
            st.success("✅ Correct! +10 XP")
            send_to_sheet(st.session_state.current_bug["code"], 10)
            next_bug()
            st.rerun()
        else:
            st.error("❌ Incorrect. Try again.")
            send_to_sheet(st.session_state.current_bug["code"], 0)

with col2:
    if st.button("Show Hint"):
        st.info(f"💡 Hint: {st.session_state.current_bug['hint']}")

with st.expander("Admin Panel"):
    admin_pass_input = st.text_input("Enter Admin Password", type="password")
    if admin_pass_input == ADMIN_PASS:
        st.write("Admin Access Granted")
        st.write("Sheet URL:", SHEET_URL)
    elif admin_pass_input:
        st.error("Wrong Password")
