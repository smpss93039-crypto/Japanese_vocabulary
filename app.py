import streamlit as st
import pandas as pd
import random
import requests
import io

# ====== Google Fonts & CSS ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

    html, body, [class*="css"] {
        font-family: "宋体", "SimSun", "Times New Roman", serif;
    }

    .big-text {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== Google Sheet 設定 ======
SHEET_ID = "1fu6Lm3J54fo-hYOXmoYwHtylNSKIH8rDd6Syvpc9wuA"

def get_csv_url(sheet_name):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

@st.cache_data
def load_data(sheet_name):
    CSV_URL = get_csv_url(sheet_name)
    r = requests.get(CSV_URL)
    r.encoding = 'utf-8-sig'
    df = pd.read_csv(io.StringIO(r.text))
    return df

# ====== 初始化 session state ======
if "question" not in st.session_state:
    st.session_state.word = None
    st.session_state.katakana = ""
    st.session_state.chinese = ""
    st.session_state.example = ""
    st.session_state.used_indices = set()

# ====== 載入資料（固定「媽媽的日文」） ======
st.session_state.data = load_data("媽媽的日文")

# ====== 產生新題目（不重複） ======
def new_question():
    df = st.session_state.data
    available_indices = set(df.index) - st.session_state.used_indices
    if not available_indices:
        st.success("全部看完囉！")
        return
    idx = random.choice(list(available_indices))
    st.session_state.used_indices.add(idx)

    row = df.loc[idx]
    st.session_state.word = row["word"]       # 單字（日文/漢字）
    st.session_state.katakana = row["katakana"]   # 片假名
    st.session_state.chinese = row["chinese"]     # 中文意思
    st.session_state.example = row["example"]     # 日文例句

# ====== 畫面顯示 ======
if st.session_state.word is None:
    new_question()

if st.session_state.word:
    st.markdown(f"<div class='big-text'>{st.session_state.word}</div>", unsafe_allow_html=True)     # 單字
    st.markdown(f"<div class='big-text'>{st.session_state.katakana}</div>", unsafe_allow_html=True) # 片假名
    st.markdown(f"<div class='big-text'>{st.session_state.chinese}</div>", unsafe_allow_html=True)  # 中文意思
    st.markdown(f"<div class='big-text'>{st.session_state.example}</div>", unsafe_allow_html=True)  # 例句

st.button("下一頁", on_click=new_question)
