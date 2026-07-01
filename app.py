
import streamlit as st
import json,os



# --- Total Players Counter - No File Write ---
if "count" not in st.session_state:
    st.session_state.count = 1  # 1st visitor = 1
st.title("🐛 Debug Sprint")
st.metric(label="Total Players", value=st.session_state.count) 
st.caption("7 Levels. Find the bug. Fix it fast.")


if "lvl" not in st.session_state:
    st.session_state.lvl = 0
    st.session_state.score = 0

BUGS = [
  {"code": "x = 5\nif x = 5:\n print('ok')", "fix": "==", "hint": "Assignment vs Comparison"},
  
  {"code": "nums = [1,2,3]\nprint(nums[3])", "fix": "2", "hint": "Index starts at 0"},
  {"code": "for i in range(5)\n print(i)", "fix": ":", "hint": "Missing colon"},
  {"code": "name = input()\nif name == 5:\n print('ok')", "fix": "str", "hint": "Type mismatch"},
  {"code": "def add(a,b)\n return a+b", "fix": ":", "hint": "Missing colon"},
  {"code": "x = '5' + 5", "fix": "int", "hint": "Can't add str + int"},
  {"code": "while True: pass", "fix": "break", "hint": "Infinite loop"}
]

# GAME
if st.session_state.lvl >= len(BUGS):
    st.balloons()
    st.success(f"🎉 Game Complete! Final Score: {st.session_state.score}/{len(BUGS)}")
    st.info("Share this app with friends to challenge them.")
    if st.button("Play Again"):
        st.session_state.lvl = 0
        st.session_state.score = 0
        st.rerun()
else:
    b = BUGS[st.session_state.lvl]
    st.subheader(f"Level {st.session_state.lvl+1} / {len(BUGS)}")
    st.code(b["code"], language="python")
    ans = st.text_input("What's the fix?", key=st.session_state.lvl)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit"):
            if ans.strip().lower() == b["fix"]:
                st.success("Correct! +1")
                st.session_state.score += 1
                st.session_state.lvl += 1
                st.rerun()
            else:
                st.error("Wrong. Try again.")
    with col2:
        if st.button("Hint"):
            st.info(b["hint"])
    st.write(f"**Score:** {st.session_state.score}")
