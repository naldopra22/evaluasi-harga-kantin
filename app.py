import streamlit as st
import re
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from io import BytesIO

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Evaluasi Harga Kantin ITPA",
    layout="centered"
)

st.title("📊 Evaluasi Opini Mahasiswa Tentang Harga Makanan di Kantin ITPA")

# =========================
# DATA & DICTIONARY
# =========================
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

# =========================
# SESSION STATE
# =========================
if "sentiment_counter" not in st.session_state:
    st.session_state.sentiment_counter = {v: 0 for v in rating_category.values()}

last_result_text = ""

# =========================
# FUNGSI ANALISIS
# =========================
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

# =========================
# INPUT OPINI
# =========================
opini = st.text_area("✍ Masukkan Opini Mahasiswa", height=120)

if st.button("🔍 Proses Opini"):
    if not opini.strip():
        st.warning("Masukkan opini terlebih dahulu.")
    else:
        rating, complaints = analyze_food(opini)

        if rating is None:
            st.error("⚠ Kata harga tidak ditemukan.")
        else:
            kategori = rating_category[rating]
            st.session_state.sentiment_counter[kategori] += 1

            last_result_text = (
                f"HASIL EVALUASI OPINI HARGA MAKANAN DI KANTIN ITPA\n\n"
                f"Rating   : {rating}\n"
                f"Kategori : {kategori}\n"
                f"Keluhan  : {complaints if complaints else 'Tidak ada'}\n"
                f"Saran    : {solution_suggestion[rating]}"
            )

            st.success("✅ Analisis berhasil")
            st.text(last_result_text)

            # =========================
            # DOWNLOAD PDF
            # =========================
            buffer = BytesIO()
            c = pdf_canvas.Canvas(buffer, pagesize=A4)
            text_obj = c.beginText(40, 800)

            for line in last_result_text.split("\n"):
                text_obj.textLine(line)

            c.drawText(text_obj)
            c.save()
            buffer.seek(0)

            st.download_button(
                label="⬇ Download PDF",
                data=buffer,
                file_name="evaluasi_harga_kantin_ITPA.pdf",
                mime="application/pdf"
            )

# =========================
# GRAFIK
# =========================
st.subheader("📈 Grafik Kepuasan Harga")

fig, ax = plt.subplots()
kategori = list(st.session_state.sentiment_counter.keys())
nilai = list(st.session_state.sentiment_counter.values())

ax.bar(kategori, nilai)
ax.set_title("Grafik Kepuasan Harga Makanan di Kantin ITPA")
ax.set_ylabel("Jumlah Opini")
ax.tick_params(axis="x", rotation=20)

st.pyplot(fig)
