import random
import streamlit as st

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
    height=100,
)

# 単語のリスト化とベースのリスト保持
raw_words = input_text.replace(",", " ").replace("\n", " ").split()
base_words = [w for w in raw_words if w.strip()]

# セッション状態の初期化
if "song_words" not in st.session_state:
  st.session_state.song_words = base_words.copy()

if "taken" not in st.session_state:
  st.session_state.taken = {word: False for word in st.session_state.song_words}

# 単語が新しく追加・変更された場合の同期
if set(base_words) != set(st.session_state.song_words):
  st.session_state.song_words = base_words.copy()
  st.session_state.taken = {word: False for word in st.session_state.song_words}

# リセットボタン（押すたびにランダムにシャッフルする）
if st.button("ゲームスタート / リセット（シャッフル）"):
  st.session_state.song_words = base_words.copy()
  random.shuffle(st.session_state.song_words)
  st.session_state.taken = {
      word: False for word in st.session_state.song_words
  }

# カードが未初期化の場合の安全策
if len(st.session_state.taken) != len(st.session_state.song_words) or not all(
    w in st.session_state.taken for w in st.session_state.song_words
):
  st.session_state.taken = {
      word: False for word in st.session_state.song_words
  }

st.write("---")

# 取った枚数のカウント
taken_count = sum(1 for v in st.session_state.taken.values() if v)
st.subheader(
    f"取った札: {taken_count} / {len(st.session_state.song_words)} 枚"
)

# カードをボタン形式でグリッド配置（シャッフルされた順序で表示）
cols_per_row = 4
rows = [
    st.session_state.song_words[i : i + cols_per_row]
    for i in range(0, len(st.session_state.song_words), cols_per_row)
]

for row in rows:
  cols = st.columns(len(row))
  for idx, word in enumerate(row):
    with cols[idx]:
      if st.session_state.taken.get(word, False):
        st.button(f"✅ {word}", key=f"btn_{word}", disabled=True)
      else:
        if st.button(word, key=f"btn_{word}__active"):
          st.session_state.taken[word] = True
          st.rerun()
