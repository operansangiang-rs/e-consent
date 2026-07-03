import streamlit as st
from streamlit_drawable_canvas import st_canvas
import datetime
from fpdf import FPDF

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
# 3. BAGIAN VERIFIKASI ONLINE (SIMULASI OTP)
# ==========================================
st.subheader("3. Verifikasi Keamanan")
col1, col2 = st.columns([2, 1])
with col1:
    no_hp = st.text_input("Masukkan Nomor WhatsApp Aktif:", placeholder="Contoh: 0812xxxx")
with col2:
    st.write(" ") 
    st.write(" ") 
    if st.button("Kirim OTP"):
        st.toast("Simulasi: Kode OTP '1234' berhasil dikirim ke WhatsApp!", icon="💬")

otp_input = st.text_input("Masukkan 4 Digit OTP:", max_chars=4, placeholder="Masukkan kode yang diterima")

st.write("---")

# ==========================================
# 4. BAGIAN PERNYATAAN & TANDA TANGAN
# ==========================================
st.subheader("4. Pernyataan Persetujuan")
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
# FUNGSI UNTUK MEMBUAT PDF SECARA DIGITAL
# ==========================================
def buat_pdf(nama_p, nik_p, tgl_p, hp_p, waktu_p):
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
    pdf.cell(0, 10, f"No HP        : {hp_p}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "PERNYATAAN:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "Pasien telah menyatakan SETUJU dan MEMAHAMI segala prosedur medis serta risiko tindakan Odontektomi (Cabut Gigi Bungsu) yang dilakukan secara sadar tanpa paksaan melalui sistem verifikasi online.")
    pdf.ln(10)
    
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Status Dokumen: APPROVED & VERIFIED (DIGITAL SIGNATURE)", ln=True)
    return pdf.output(dest='S') # Mengembalikan file berupa bytes data

# ==========================================
# 5. TOMBOL SUBMIT & LOGIKA DOWNLOAD PDF
# ==========================================
if st.button("Kirim Persetujuan (Submit)", type="primary"):
    if not nama or not nik or not no_hp:
        st.error("❌ Mohon lengkapi Data Diri Anda terlebih dahulu.")
    elif otp_input != "1234":
        st.error("❌ Kode OTP salah atau belum diisi (Gunakan kode simulasi: 1234).")
    elif not (setju_1 and setju_2):
        st.error("❌ Anda harus mencentang semua pernyataan persetujuan.")
    elif canvas_result.image_data is None:
        st.error("❌ Mohon bubuhkan tanda tangan Anda terlebih dahulu.")
    else:
        st.success("✅ **Electronic Informed Consent BERHASIL Disimpan!**")
        st.balloons()
        
        waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Bikin file PDF di latar belakang backend
        pdf_bytes = buat_pdf(nama, nik, tgl_lahir, no_hp, waktu_sekarang)
        
        # Tombol Download PDF otomatis muncul setelah klik submit sukses
        st.write("### ⬇️ Unduh Dokumen Resmi Anda:")
        st.download_button(
            label="Download Bukti Persetujuan (PDF)",
            data=pdf_bytes,
            file_name=f"E-Consent_{nik}.pdf",
            mime="application/pdf"
        )
