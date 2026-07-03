# ==========================================
# FUNGSI UNTUK MEMBUAT PDF + CETAK TANDA TANGAN (TITIK DUA RAPI)
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
    
    # --- PROSES CETAK TITIK DUA SEJAJAR ---
    # Baris Nama Lengkap
    pdf.cell(35, 10, "Nama Lengkap")
    pdf.cell(5, 10, ":")
    pdf.cell(0, 10, f"{nama_p}", ln=True)
    
    # Baris NIK
    pdf.cell(35, 10, "NIK")
    pdf.cell(5, 10, ":")
    pdf.cell(0, 10, f"{nik_p}", ln=True)
    
    # Baris Tanggal Lahir
    pdf.cell(35, 10, "Tanggal Lahir")
    pdf.cell(5, 10, ":")
    pdf.cell(0, 10, f"{tgl_p}", ln=True)
    
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
        img = Image.fromarray(ttd_image_data.astype('uint8'), 'RGBA')
        bg = Image.new("RGBA", img.size, (255, 255, 255))
        alpha_composite = Image.alpha_composite(bg, img).convert("RGB")
        
        current_y = pdf.get_y()
        pdf.image(alpha_composite, x=15, y=current_y, w=60, h=30)
        pdf.ln(35) 
    except Exception as e:
        pdf.cell(0, 10, "[Gagal memuat gambar tanda tangan]", ln=True)
        pdf.ln(5)

    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Status Dokumen: APPROVED & VERIFIED (DIGITAL SIGNATURE)", ln=True)
    
    return bytes(pdf.output())
