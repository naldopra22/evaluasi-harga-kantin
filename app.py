import streamlit as st
import re
import matplotlib.pyplot as plt

# =============================
# DATA KAMUS PENILAIAN
# =============================
custom_dict = {
    "harga murah": 5,
    "murah": 5,
    "cukup murah": 4,
    "harga sedang": 3,
    "standar": 3,
    "normal": 3,
    "harga mahal": 1,
    "mahal": 1,
    "agak mahal": 2,
    "terlalu mahal": 1,
    "kemahalan": 1,
    "makanan enak": 5,
    "porsi banyak": 4,
    "porsi sedikit": 1,
    "tidak enak": 1,
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
    2: "Pertimbangkan menurunkan harga atau menambah porsi.",
    1: "Segera evaluasi harga karena banyak keluhan.",
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
    score = 0
    count = 0
    complaints = []

    text = text.lower()

    for key in sorted(custom_dict, key=len, reverse=True):
        matches = re.findall(r"\b" + re.escape(key) + r"\b", text)
        for _ in matches:
            value = custom_dict[key]
            score += value
            count += 1
            if value <= 2:
                complaints.append(key)

    if count == 0:
        return None, None

    rating = round(max(1, min(5, score / count)))
    return rating, complaints

# =============================
# TAMPILAN WEB
# =============================
st.set_page_config(
    page_title="Evaluasi Harga Kantin ITPA",
    layout="centered"
)

st.title("📊 Evaluasi Opini Mahasiswa Tentang Harga Makanan di Kantin ITPA")
st.write("Masukkan opini mahasiswa mengenai harga makanan di kantin.")

text = st.text_area("✍ Masukkan Opini")

# =============================
# PROSES OPINI
# =============================
if st.button("🔍 Proses Opini"):
    if text.strip() == "":
        st.warning("⚠ Silakan masukkan opini terlebih dahulu.")
    else:
        rating, complaints = analyze_food(text)

        if rating is None:
            st.error("❌ Kata yang berhubungan dengan harga tidak ditemukan.")
        else:
            category = rating_category[rating]
            st.session_state.counter[category] += 1

            keluhan_text = ", ".join(complaints) if complaints else "Tidak ada"

            st.success("✅ Hasil Evaluasi")
            st.write(f"*Rating :* {rating}")
            st.write(f"*Kategori :* {category}")
            st.write(f"*Keluhan :* {keluhan_text}")
            st.write(f"*Saran :* {solution_suggestion[rating]}")

# =============================
# GRAFIK (OTOMATIS MUNCUL)
# =============================
st.subheader("📈 Grafik Kepuasan Harga")

fig, ax = plt.subplots()
ax.bar(
    st.session_state.counter.keys(),
    st.session_state.counter.values()
)
ax.set_xlabel("Kategori")
ax.set_ylabel("Jumlah")
plt.xticks(rotation=20)

st.pyplot(fig)
