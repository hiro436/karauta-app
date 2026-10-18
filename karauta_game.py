import streamlit as st

st.title("🎵 狩歌 練習アプリ")
st.write("曲を流しながら、聴こえた単語のカードをクリックしていこう！")

# デフォルトの単語リスト
default_words = (
    "君 愛 涙 未来 夜 光 夢 心 世界 さよなら 約束 風 今 空 星 手"
)

# 画面上の入力欄（ここで単語を自由に変更できます）
input_text = st.text_area(
    "曲の単語（スペースやカンマ、改行区切りで入力）", value=default_words, height=100
)

# 単語のリスト化
raw_words = input_text.replace(",", " ").replace("\n", " ").split()
song_words = [w for w in raw_words if w.strip()]

# セッション状態（ゲームのスコアや押した状態の保持）の初期化
if "taken" not in st.session_state:
  st.session_state.taken = {}

# リセットボタン
if st.button("ゲームスタート / リセット"):
  st.session_state.taken = {word: False for word in song_words}

# カードが未初期化または単語が変わった場合の初期化
if len(st.session_state.taken) != len(song_words) or not all(
    w in st.session_state.taken for w in song_words
):
  st.session_state.taken = {word: False for word in song_words}

st.write("---")

# 取った枚数のカウント
taken_count = sum(1 for v in st.session_state.taken.values() if v)
st.subheader(f"取った札: {taken_count} / {len(song_words)} 枚")

# カードをボタン形式でグリッド配置（4列）
cols_per_row = 4
rows = [
    song_words[i : i + cols_per_row]
    for i in range(0, len(song_words), cols_per_row)
]

for row in rows:
  cols = st.columns(len(row))
  for idx, word in enumerate(row):
    with cols[idx]:
      # すでに取られているか判定
      if st.session_state.taken.get(word, False):
        st.button(f"✅ {word}", key=f"btn_{word}", disabled=True)
      else:
        if st.button(word, key=f"btn_{word}__active"):
          st.session_state.taken[word] = True
          st.rerun()