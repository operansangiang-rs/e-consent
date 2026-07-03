
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import datetime

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
# 2. BAGIAN PENJELASAN MEDIS (CONTOH KASUS)
# ==========================================
st.subheader("2. Penjelasan Tindakan Medis")
st.warning("📋 **Jenis Tindakan: Pencabutan Gigi Bungsu (Odontektomi)**")

# Menggunakan expander agar tampilan di HP ringkas dan rapi
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
    st.write(" ") # Ganjal jarak
    st.write(" ") 
    if st.button("Kirim OTP"):
        st.toast("Simulasi: Kode OTP '1234' berhasil dikirim ke WhatsApp!", icon="💬")

otp_input = st.text_input("Masukkan 4 Digit OTP:", max_chars=4, placeholder="Masukkan kode yang diterima")

st.write("---")

# ==========================================
# 4. BAGIAN PERNYATAAN & TANDA TANGAN DIGITAL
# ==========================================
st.subheader("4. Pernyataan Persetujuan")

setuju_1 = st.checkbox("Saya menyatakan telah membaca, mendengar, dan memahami informasi tindakan medis di atas.")
setuju_2 = st.checkbox("Saya menyetujui tindakan tersebut dilakukan secara sadar, online, dan tanpa paksaan.")

st.write(" ")
st.write("**Gunakan jari Anda (di HP) atau mouse (di laptop) untuk tanda tangan di kotak bawah ini:**")

# Komponen Canvas untuk coretan tanda tangan digital
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
# 5. TOMBOL SUBMIT & OUTPUT AKHIR
# ==========================================
if st.button("Kirim Persetujuan (Submit)", type="primary"):
    # Validasi apakah data sudah diisi lengkap
    if not nama or not nik or not no_hp:
        st.error("❌ Mohon lengkapi Data Diri Anda terlebih dahulu.")
    elif otp_input != "1234":
        st.error("❌ Kode OTP salah atau belum diisi (Gunakan kode simulasi: 1234).")
    elif not (setuju_1 and setuju_2):
        st.error("❌ Anda harus mencentang semua pernyataan persetujuan.")
    elif canvas_result.image_data is None:
        st.error("❌ Mohon bubuhkan tanda tangan Anda terlebih dahulu.")
    else:
        st.success("✅ **Electronic Informed Consent BERHASIL Disimpan!**")
        st.info("📦 **Bukti Transaksi Digital (Metadata):**")
        waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.json({
            "Status Persetujuan": "APPROVED (ONLINE)",
            "Nama Pasien": nama,
            "NIK": nik,
            "No HP/WhatsApp": no_hp,
            "Waktu Validasi": waktu_sekarang,
            "Metode Verifikasi": "Simulasi OTP WhatsApp Sukses",
            "Integritas Data": "Disimpan ke Cloud Server (Simulasi)"
        })
        st.balloons()
