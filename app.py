
import streamlit as st
import json,os



# --- Total Players Counter ---
if not os.path.exists("players.json"):
    with open("players.json", "w") as f:
        json.dump({"count": 0}, f)

with open("players.json", "r") as f:
    data = json.load(f)  # <- Ab `data` define ho gaya = No Error


st.set_page_config(page_title="Debug Sprint", layout="centered", menu_items=None)




if "started" not in st.session_state:
    data["count"] += 1
    with open("players.json", "w") as f:
        json.dump(data, f)
    st.session_state.started = True

st.title("🐛 Debug Sprint")
st.caption("7 Levels. Find the bug. Fix it fast.")
st.metric(label="Total Players", value=data["count"])

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
