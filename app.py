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

    .hiragana-line {
        border-bottom: 2px solid #444;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    .emoji {
        margin-right: 10px;
    }

    /* 往上移整個頁面 */
    .css-18e3th9 {
        padding-top: 10px;  /* 原本可能是 50px~，改小讓頁面往上 */
    }
    </style>
""", unsafe_allow_html=True)


# ====== Google Sheet 設定 ======
SHEET_ID = "1fu6Lm3J54fo-hYOXmoYwHtylNSKIH8rDd6Syvpc9wuA"

def get_csv_url(sheet_name):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


def load_data(sheet_name):
    CSV_URL = get_csv_url(sheet_name)
    r = requests.get(CSV_URL)
    r.encoding = 'utf-8-sig'
    df = pd.read_csv(io.StringIO(r.text))
    return df

# ====== 初始化 session state ======
if "word" not in st.session_state:
    st.session_state.word = None
    st.session_state.hiragana = ""
    st.session_state.chinese = ""
    st.session_state.example = ""
    st.session_state.used_indices = set()

# ====== 載入資料 ======
st.session_state.data = load_data("媽媽的日文")

# ====== 產生新題目 ======
def new_question():
    df = st.session_state.data
    available_indices = set(df.index) - st.session_state.used_indices
    if not available_indices:
        st.success("全部看完囉！")
        return
    idx = random.choice(list(available_indices))
    st.session_state.used_indices.add(idx)

    row = df.loc[idx]
    st.session_state.word = row["word"]
    st.session_state.katakana = row["hiragana"]
    st.session_state.chinese = row["chinese"]
    st.session_state.example = row["example"]

# ====== 顯示畫面 ======
if st.session_state.word is None:
    new_question()

if st.session_state.word:
    # 第一行：單字
    st.markdown(f"<div class='big-text'>{st.session_state.word}</div>", unsafe_allow_html=True)

    # 第二行：平假名 + 分隔線
    st.markdown(f"<div class='big-text hiragana-line'>{st.session_state.hiragana}</div>", unsafe_allow_html=True)

    # 第三行：中文前加 emoji
    st.markdown(f"<div class='big-text'>👉 {st.session_state.chinese}</div>", unsafe_allow_html=True)

    # 第四行：例句前加 emoji
    st.markdown(f"<div class='big-text'>👉 {st.session_state.example}</div>", unsafe_allow_html=True)

# 下一頁按鈕
st.button("下一頁", on_click=new_question)
