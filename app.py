import streamlit as st
import random

st.set_page_config(page_title="DebugSprint", page_icon="🐛", layout="wide")

# --- Dark Theme CSS ---
st.markdown("""
<style>
.stApp { background-color: #1e1e2e; }
h1, h2, h3, p, label, div { color: #cdd6f4!important; }
.stButton>button { background-color: #89b4fa; color: #1e1e2e; font-weight: bold; border-radius: 8px; }
.stTextArea textarea { background-color: #313244; color: #cdd6f4; font-family: Consolas; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.title("🐛 DebugSprint")
st.caption("Fix the bug, earn XP")

# --- THE MASTER PROBLEM BANK ---
CHALLENGES = {
    "Core Syntax": [
        {
            "buggy": "def is_even(num):\n if num % 2 = 0:\n return True\n else:\n return False",
            "hint": "Assignment `=` vs Comparison `==`",
            "concept": "Conditional Operators",
            "explain": "Remember: `=` is for creating variables. `==` is for checking if things are equal.",
            "ideal_lines": 1,
            "doc_keyword": "controlFlow"
        },
        {
            "buggy": "def get_total(price, tax)\n return price * tax",
            "hint": "Missing something at the end of line 1",
            "concept": "Function Headers",
            "explain": "Don't forget your colons `:` at the end of def, if, for, and while lines!",
            "ideal_lines": 2,
            "doc_keyword": "functions"
        }
    ],
    "Data Structures": [
        {
            "buggy": "my_list = [10, 20, 30]\nprint(my_list[3])",
            "hint": "Lists start counting from 0, not 1",
            "concept": "Indexing",
            "explain": "The last item in a list of 3 items is at index 2, not 3.",
            "ideal_lines": 1,
            "doc_keyword": "lists"
        }
    ]
}

# --- Session State Setup ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = random.choice(CHALLENGES["Core Syntax"])

challenge = st.session_state.current_challenge

# --- UI Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Concept: {challenge['concept']}")
    st.code(challenge['buggy'], language='python')
    if st.button("💡 Need a Hint? -10 XP"):
        st.warning(challenge['hint'])
        st.session_state.score -= 10

with col2:
    st.subheader("Your Fix:")
    user_code = st.text_area("Edit the code here:", value=challenge['buggy'], height=200, label_visibility="collapsed")

    if st.button("✅ Check My Fix"):
        try:
            exec(user_code)
            st.success("Code Runs! No Syntax Errors.")
            st.session_state.score += 50
            st.balloons()
        except Exception as e:
            st.error(f"Still Broken: {e}")

st.divider()
st.metric("Your XP", st.session_state.score)

if st.button("🔄 Next Bug"):
    st.session_state.current_challenge = random.choice(CHALLENGES["Core Syntax"])
    st.rerun()