import streamlit as st

st.set_page_config(page_title="狩歌 練習アプリ", layout="centered")

# スマホでの余白を完全に削る最強のCSS
st.markdown(
    """
    <style>
    /* 画面全体の余白を調整 */
    .block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    /* 横並びブロックの間隔をゼロにする */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        margin-bottom: 2px !important;
    }
    /* カラムの余白を強制削除 */
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: unset !important;
        padding: 0px 1px !important;
    }
    /* ボタン自体の大きさと隙間を調整 */
    .stButton > button {
        width: 100% !important;
        height: 2.3em !important;
        font-size: 13px !important;
        font-weight: bold;
        padding: 0px !important;
        margin: 0px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎵 狩歌 練習アプリ")
st.write("曲を流しながら、聴こえた単語のカードをクリックしていこう！")

# デフォルトの単語リスト
default_words = (
    "君 愛 涙 未来 夜 光 夢 心 世界 さよなら 約束 風 今 空 星 手"
)

# 画面上の入力欄
input_text = st.text_area(
    "曲の単語（スペースやカンマ、改行区切りで入力）",
    value=default_words,
    height=80,
)

# 単語のリスト化
raw_words = input_text.replace(",", " ").replace("\n", " ").split()
song_words = [w for w in raw_words if w.strip()]

# セッション状態の初期化
if "taken" not in st.session_state:
  st.session_state.taken = {}

# リセットボタン
if st.button("🔄 ゲームスタート / リセット", use_container_width=True):
  st.session_state.taken = {word: False for word in song_words}

# 単語変更時の初期化
if len(st.session_state.taken) != len(song_words) or not all(
    w in st.session_state.taken for w in song_words
):
  st.session_state.taken = {word: False for word in song_words}

st.write("---")

# スコア表示
taken_count = sum(1 for v in st.session_state.taken.values() if v)
st.subheader(f"取った札: {taken_count} / {len(song_words)} 枚")

# カードを4列ずつ配置
cols_per_row = 4
rows = [
    song_words[i : i + cols_per_row]
    for i in range(0, len(song_words), cols_per_row)
]

for row in rows:
  cols = st.columns(4)
  for idx, word in enumerate(row):
    with cols[idx]:
      if st.session_state.taken.get(word, False):
        st.button(f"✅ {word}", key=f"btn_{word}", disabled=True)
      else:
        if st.button(word, key=f"btn_{word}_active"):
          st.session_state.taken[word] = True
          st.rerun()
