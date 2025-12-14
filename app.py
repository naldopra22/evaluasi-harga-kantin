import streamlit as st
import re
import matplotlib.pyplot as plt

# =============================
# DATA KAMUS & KATEGORI
# =============================
custom_dict = {
    "harga murah": 5, "murah": 5, "cukup murah": 4,
    "harga sedang": 3, "standar": 3, "normal": 3,
    "harga mahal": 1, "mahal": 1, "agak mahal": 2,
    "terlalu mahal": 1, "kemahalan": 1,
    "makanan enak": 5, "porsi banyak": 4,
    "porsi sedikit": 1, "tidak enak": 1,
}

rating_category = {
    5: "Sangat Memuaskan",
    4: "Memuaskan",
    3: "Cukup Baik",
    2: "Perlu Evaluasi",
    1: "Banyak Keluhan",
}

solution_suggestion = {
    5: "Kualitas dan harga sangat baik. Pertahankan standar.",
    4: "Harga cukup baik. Variasi menu bisa ditingkatkan.",
    3: "Harga standar. Evaluasi berkala diperlukan.",
    2: "Pertimbangkan turunkan harga atau tambah porsi.",
    1: "Segera evaluasi harga. Banyak keluhan muncul.",
}

# =============================
# SESSION STATE
# =============================
if "counter" not in st.session_state:
    st.session_state.counter = {v: 0 for v in rating_category.values()}

# =============================
# FUNGSI ANALISIS
# =============================
def analyze_food(text):
    score, count = 0, 0
    complaints = []
    text = text.lower()

    for key in sorted(custom_dict, key=len, reverse=True):
        for _ in re.finditer(r"\b" + re.escape(key) + r"\b", text):
            val = custom_dict[key]
            score += val
            count += 1
            if val <= 2:
                complaints.append(key)

    if count == 0:
        return None, None

    rating = round(max(1, min(5, score / count)))
    return rating, complaints

# =============================
# UI STREAMLIT
# =============================
st.set_page_config(page_title="Evaluasi Harga Kantin ITPA", layout="centered")
st.title("📊 Evaluasi Opini Mahasiswa Tentang Harga Makanan di Kantin ITPA")

text = st.text_area("Masukkan Opini Mahasiswa")

if st.button("Proses Opini"):
    rating, complaints = analyze_food(text)

    if rating is None:
        st.warning("Kata harga tidak ditemukan.")
    else:
        cat = rating_category[rating]
        st.session_state.counter[cat] += 1

        st.success(f"Rating: {rating}")
        st.write("*Kategori:*", cat)
        st.write("*Keluhan:*", complaints if complaints else "Tidak ada")
        st.write("*Saran:*", solution_suggestion[rating])

# =============================
# GRAFIK
# =============================
st.subheader("Grafik Kepuasan")
fig, ax = plt.subplots()
ax.bar(st.session_state.counter.keys(), st.session_state.counter.values())
ax.set_ylabel("Jumlah")
ax.set_xlabel("Kategori")
st.pyplot(fig)
