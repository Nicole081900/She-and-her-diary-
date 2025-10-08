import streamlit as st
from datetime import date
from PIL import Image
import json
import os
import time

# 设置页面
st.set_page_config(page_title="我的日记", page_icon="📔", layout="centered")

# 加载或创建设置
settings_file = "data/settings.json"
os.makedirs("data", exist_ok=True)

if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {}

# 背景图片设置
bg_url = st.text_input(
    "背景图片 URL（留空使用默认）",
    value=settings.get("bg_url", "https://images.unsplash.com/photo-1503264116251-35a269479413")
)

# 保存设置
settings["bg_url"] = bg_url
with open(settings_file, "w", encoding="utf-8") as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)

# 设置背景 CSS
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('{bg_url}');
        background-size: cover;
        background-attachment: fixed;
    }}
    section[data-testid="stAppViewContainer"] > div {{
        background-color: rgba(255,255,255,0.85);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 页面标题
st.title("📔 我的日记")
# 显示今日日期和鼓励语
st.markdown(f"📅 **{date.today()}**")
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">
    <style>
    .custom-font {
        font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 26px;
        color: #FF3366;
    }
    </style>
    <div class="custom-font">
        💖 亲爱的吴思楠，今天也要快乐啊！！！
    </div>
""", unsafe_allow_html=True)


# 表单输入
entry_date = st.date_input("日期", value=date.today())
uploaded_file = st.file_uploader("上传照片（可选）", type=["jpg", "jpeg", "png"])
score = st.slider("心情评分", 0.0, 10.0, 7.0, step=0.5)
note = st.text_area("今天记录", height=200)

# 保存逻辑
if st.button("💾 保存日记"):
    os.makedirs("uploads", exist_ok=True)

    image_path = ""
    if uploaded_file is not None:
        timestamp = int(time.time())
        fname = f"{timestamp}_{uploaded_file.name}"
        save_path = os.path.join("uploads", fname)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_path = save_path

    entry = {
        "date": str(entry_date),
        "score": float(score),
        "note": note,
        "image": image_path,
        "saved_at": int(time.time())
    }

    diary_file = os.path.join("data", "diary.json")
    if not os.path.exists(diary_file):
        with open(diary_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(diary_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append(entry)

    with open(diary_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    st.success("✅ 日记已保存！")
    st.balloons()

# 显示最近日记
st.markdown("---")
st.subheader("最近的日记")

diary_file = os.path.join("data", "diary.json")
if os.path.exists(diary_file):
    with open(diary_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data:
        for i, entry in enumerate(reversed(data[-10:])):
            idx_in_data = len(data) - 10 + i
            st.write(f"📅 {entry['date']}    评分：{entry['score']}")
            st.write(entry['note'])
            if entry.get("image"):
                try:
                    img = Image.open(entry["image"])
                    st.image(img, width=300)
                except Exception:
                    st.write("（显示图片失败）")
            if st.button(f"🗑️ 删除这条日记（{entry['date']}）", key=f"delete_{i}"):
                del data[idx_in_data]
                with open(diary_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                st.experimental_rerun()
            st.markdown("---")
    else:
        st.info("目前没有日记。")
else:
    st.info("目前没有日记文件。")
