import streamlit as st
import requests
import time
import random
import json

st.set_page_config(page_title="DebugSprint", layout="centered")

# ========= CONFIG =========
import pandas as pd
import os

def save_to_csv(player_id, xp, level):
    data = {'Player_ID': [player_id], 'XP': [xp], 'Level': [level], 'Time': [pd.Timestamp.now()]}
    df = pd.DataFrame(data)
    file_exists = os.path.isfile('leaderboard.csv')
    df.to_csv('leaderboard.csv', mode='a', header=not file_exists, index=False)
ADMIN_PASS = "aL19zX82pQ" 

BUGS = [
    {"code": "x = 5\nprint(x)", "fix": "x = 5\nprint(x)", "hint": "Indentation is already correct here"}, # Bug 1
    {"code": "x = 5\\nprint(x)", "fix": "x = 5\nprint(x)", "hint": "Check for double backslash \\n"}, # Bug 2 FIXED
    {"code": "for i in range(5)\n print(i)", "fix": "for i in range(5)\n print(i)", "hint": "Both ')' and ':' are missing"}, # Bug 3 FIXED
    {"code": "def add(a b):\n return a+b", "fix": "def add(a, b):\n return a+b", "hint": "Missing comma between parameters"},
    {"code": "print('Hello'", "fix": "print('Hello')", "hint": "Missing closing bracket )"},
    {"code": "name = 'Ali\nprint(name)", "fix": "name = 'Ali'\nprint(name)", "hint": "Missing closing quote '"},
    {"code": "list = [1,2,3\nprint(list)", "fix": "list = [1,2,3]\nprint(list)", "hint": "Missing closing bracket ]"},
    {"code": "x=10\nif x>5\nprint('big')", "fix": "x=10\nif x>5:\nprint('big')", "hint": "Missing colon : after if"},
]# ========= BUGS LIST =========



# ========= FUNCTIONS =========

    

        
    

def check_answer(user_code, bug):
    return user_code.strip() == bug["fix"].strip()

# ========= SESSION STATE =========
if "player_id" not in st.session_state:
    st.session_state.player_id = f"player_{random.randint(1000,9999)}"
if "level" not in st.session_state: st.session_state.level = 1
if "xp" not in st.session_state: st.session_state.xp = 0
if "bug_index" not in st.session_state: st.session_state.bug_index = 0
if "is_admin" not in st.session_state: st.session_state.is_admin = False

# ========= UI =========
st.title("🐛 DebugSprint: Fix the Code, Win XP")

# Admin Login
with st.expander("🔑 Admin Panel"):
    pwd = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASS:
            st.session_state.is_admin = True
            st.success("Admin Mode ON")
        else: st.error("Wrong Password")

if st.session_state.is_admin:
    st.subheader("Admin Dashboard")
    
    # YE 5 LINES NAYI ADD KI HAIN 👇
    if os.path.exists("leaderboard.csv"):
        df = pd.read_csv("leaderboard.csv")
        st.dataframe(df, use_container_width=True) # <- Sab bacho ka data yahan
        st.write(f"Total Players: {df['Player_ID'].nunique()}") # <- Kitne bache
    else:
        st.warning("Abhi tak koi khela nahi. Jab 1 bacha Submit karega tab table banega.")

    st.write(f"Current Level: {st.session_state.level}")
    st.write(f"Current XP: {st.session_state.xp}")
    if st.button("Reset Game"):
        st.session_state.level = 1; st.session_state.xp = 0; st.session_state.bug_index = 0
        st.rerun()
    st.divider()

# Game
bug = BUGS[st.session_state.bug_index]
st.subheader(f"Level {st.session_state.level} | XP: {st.session_state.xp}")
st.code(bug["code"], language="python")

user_code = st.text_area("Paste your fixed code here:", height=150)

col1, col2, col3 = st.columns(3) # 2 ki jaga 3 button

with col1:
    if st.button("Submit Fix"):
        if check_answer(user_code, bug):
            st.session_state.xp += 10
            st.session_state.level += 1
            st.session_state.bug_index = (st.session_state.bug_index + 1) % len(BUGS)
            save_to_csv(st.session_state.player_id, 10, st.session_state.level) # <- Sheet ki jaga CSV
            st.success(f"✅ Correct! +10 XP. Level Up!")
            time.sleep(1); st.rerun()
        else:
            st.session_state.xp = max(0, st.session_state.xp - 5) # -5 XP
            st.error(f"❌ Wrong. -5 XP")

with col2:
    if st.button("💡 Hint -5 XP"): # <- Ye raha Alag Hint Button
        st.session_state.xp = max(0, st.session_state.xp - 5)
        st.info(f"Hint: {bug['hint']}")
        st.rerun()

with col3:
    if st.button("Skip -5 XP"):
        st.session_state.xp = max(0, st.session_state.xp - 5)
        st.session_state.bug_index = (st.session_state.bug_index + 1) % len(BUGS)
        st.rerun()

