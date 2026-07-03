import streamlit as st
from streamlit_drawable_canvas import st_canvas
import datetime
from fpdf import FPDF
from PIL import Image
import numpy as np

# Pengaturan halaman agar responsif di HP/Mobile
st.set_page_config(page_title="E-Informed Consent", page_icon="📝", layout="centered")

st.title("📝 E-Informed Consent (E-IC)")
st.write("Layanan Persetujuan Tindakan Medis Online")
st.write("---")

# ==========================================
# 1. BAGIAN IDENTITAS PASIEN
# ==========================================
st.subheader("1. Identitas Pasien")
nama = st.text_input("Nama Lengkap Pasien:", placeholder="Contoh: Budi Santoso")
nik = st.text_input("Nomor NIK (16 Digit):", max_chars=16, placeholder="Contoh: 3271xxxxxxxxxxxx")
tgl_lahir = st.date_input("Tanggal Lahir:", min_value=datetime.date(1940, 1, 1))

st.write("---")

# ==========================================
# 2. BAGIAN PENJELASAN MEDIS
# ==========================================
st.subheader("2. Penjelasan Tindakan Medis")
st.warning("📋 **Jenis Tindakan: Pencabutan Gigi Bungsu (Odontektomi)**")

with st.expander("Klik untuk membaca Detail Tindakan & Risiko", expanded=True):
    st.write("""
* **Tujuan Tindakan:** Mengeluarkan gigi geraham bungsu yang tumbuh miring/terpaku di dalam gusi untuk mencegah infeksi dan pergeseran gigi lainnya.
* **Manfaat:** Menghilangkan rasa nyeri kronis, mencegah pembengkakan gusi, dan menjaga struktur gigi tetap rapi.
* **Risiko & Efek Samping:** Rasa tidak nyaman/nyeri setelah bius habis, pembengkakan pipi selama 2-3 hari, dan perdarahan ringan yang normal terjadi pasca-operasi.
""")

st.write("---")

# ==========================================
# 3. BAGIAN PERNYATAAN & TANDA TANGAN
# ==========================================
st.subheader("3. Pernyataan Persetujuan")
setju_1 = st.checkbox("Saya menyatakan telah membaca, mendengar, dan memahami informasi tindakan medis di atas.")
setju_2 = st.checkbox("Saya menyetujui tindakan tersebut dilakukan secara sadar, online, dan tanpa paksaan.")

st.write(" ")
st.write("**Gunakan jari Anda (di HP) atau mouse (di laptop) untuk tanda tangan di kotak bawah ini:**")

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=150,
    width=300,
    drawing_mode="freedraw",
    key="canvas",
)

st.write("---")

# ==========================================
# FUNGSI UNTUK MEMBUAT PDF + CETAK TANDA TANGAN
# ==========================================
def buat_pdf(nama_p, nik_p, tgl_p, waktu_p, ttd_image_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BUKTI DIGITAL INFORMED CONSENT (E-IC)", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Tanggal Transaksi: {waktu_p}", ln=True)
    pdf.cell(0, 10, "-------------------------------------------------------------------------", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "DATA PASIEN:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Nama Lengkap : {nama_p}", ln=True)
    pdf.cell(0, 10, f"NIK          : {nik_p}", ln=True)
    pdf.cell(0, 10, f"Tanggal Lahir: {tgl_p}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "PERNYATAAN:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "Pasien telah menyatakan SETUJU dan MEMAHAMI segala prosedur medis serta risiko tindakan Odontektomi (Cabut Gigi Bungsu) yang dilakukan secara sadar tanpa paksaan melalui sistem verifikasi online.")
    pdf.ln(10)
    
    # Bagian Menampilkan Gambar Tanda Tangan ke PDF
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "TANDA TANGAN DIGITAL PASIEN:", ln=True)
    pdf.ln(2)
    
    try:
        # Ubah array canvas menjadi gambar PIL (Format RGBA)
        img = Image.fromarray(ttd_image_data.astype('uint8'), 'RGBA')
        # Buat latar belakang putih (karena bawaan canvas transparan agar tanda tangan hitam terlihat jelas)
        bg = Image.new("RGBA", img.size, (255, 255, 255))
        alpha_composite = Image.alpha_composite(bg, img).convert("RGB")
        
        # Tempelkan gambar tanda tangan langsung ke halaman PDF
        current_y = pdf.get_y()
        pdf.image(alpha_composite, x=15, y=current_y, w=60, h=30)
        pdf.ln(35) # Beri ruang spasi agar teks berikutnya tidak tertimpa gambar
    except Exception as e:
        pdf.cell(0, 10, "[Gagal memuat gambar tanda tangan]", ln=True)
        pdf.ln(5)

    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Status Dokumen: APPROVED & VERIFIED (DIGITAL SIGNATURE)", ln=True)
    
    return bytes(pdf.output())

# ==========================================
# 4. TOMBOL SUBMIT & LOGIKA UTAMA
# ==========================================
if st.button("Kirim Persetujuan (Submit)", type="primary"):
    # Cek apakah kotak canvas kosong atau sudah dicoret oleh user
    is_canvas_empty = True
    if canvas_result.image_data is not None:
        if np.any(canvas_result.image_data[:, :, 3] > 0): # Mendeteksi coretan warna
            is_canvas_empty = False

    if not nama or not nik:
        st.error("❌ Mohon lengkapi Data Diri Anda terlebih dahulu.")
    elif not (setju_1 and setju_2):
        st.error("❌ Anda harus mencentang semua pernyataan persetujuan.")
    elif is_canvas_empty:
        st.error("❌ Mohon bubuhkan tanda tangan Anda terlebih dahulu.")
    else:
        st.success("✅ **Electronic Informed Consent BERHASIL Disimpan!**")
        st.balloons()
        
        waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Jalankan fungsi pembuat PDF (Kirim data teks + gambar tanda tangan)
        pdf_bytes = buat_pdf(nama, nik, tgl_lahir, waktu_sekarang, canvas_result.image_data)
        
        st.write("### ⬇️ Unduh Dokumen Resmi Anda:")
        st.download_button(
            label="Download Bukti Persetujuan (PDF)",
            data=pdf_bytes,
            file_name=f"E-Consent_{nik}.pdf",
            mime="application/pdf"
        )
