import streamlit as st
import pandas as pd
from datetime import datetime
import cloudinary
import cloudinary.uploader
from streamlit_gsheets import GSheetsConnection

# --- 1. SETTING CLOUDINARY ---
cloudinary.config( 
  cloud_name = "dl2u1olfq", 
  api_key = "699377441919147", 
  api_secret = "-Vsh09LWc2uxK4XaNva6rwhmNDM" 
)

URL_SHEET = "https://docs.google.com/spreadsheets/d/11_Br_wvmHVvJLaeXqySCUhK8eWCeslRKKNVSDdymryY/edit?usp=sharing"

def get_hari_indo(tanggal):
    hari_dict = {'Monday':'Senin','Tuesday':'Selasa','Wednesday':'Rabu','Thursday':'Kamis','Friday':'Jumat','Saturday':'Sabtu','Sunday':'Minggu'}
    return hari_dict[tanggal.strftime('%A')]

# --- 2. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Jurnal SMK Nasional Bandung", page_icon="📝", layout="wide")

# Custom CSS untuk tampilan Ramah Mata & Berwarna
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        background: linear-gradient(to right, #1E3A8A, #3B82F6);
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        border-radius: 10px;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    h1, h2 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Logo & Header
st.markdown("<br>", unsafe_allow_html=True)
col_l1, col_l2, col_l3 = st.columns([2, 1, 2])
with col_l2:
    try: st.image("logo.png", width=180)
    except: st.warning("logo.png tidak ditemukan.")

st.markdown("<h1 style='text-align:center; color:#1E3A8A; margin-bottom:0;'>📋 JURNAL MENGAJAR GURU</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#1E3A8A; margin-top:0;'>SMK NASIONAL BANDUNG</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.2rem; color:#D97706; background-color:#FEF3C7; padding:10px; border-radius:10px;'><b>✨ kieu bisa, kitu bisa, sagala bisa ✨</b></p>", unsafe_allow_html=True)
st.markdown("---")

conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. FORM JURNAL ---
with st.container(border=True):
    # Bagian Atas: Waktu
    st.markdown("### ⏰ Waktu & Identitas")
    c1, c2 = st.columns(2)
    with c1:
        tgl_input = st.date_input("📅 Pilih Tanggal", datetime.now())
    with c2:
        hari_input = get_hari_indo(tgl_input)
        st.info(f"Hari ini: **{hari_input}**")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👨‍🏫 Detail Pelajaran")
        nama = st.text_input("👤 Nama Lengkap Guru", placeholder="Masukkan nama Bapak/Ibu")
        mapel = st.text_input("📚 Mata Pelajaran", placeholder="Contoh: Dasar-dasar TJKT")
        jenis_pertemuan = st.radio("📑 Jenis Kegiatan", ["Teori", "Praktik", "Test Formatif", "Test Sumatif"], horizontal=True)
        
        st.markdown("<div style='background-color:#E0F2FE; padding:15px; border-radius:10px;'>", unsafe_allow_html=True)
        st.markdown("**📂 Administrasi & Modul**")
        adm_tipe = st.selectbox("Pilih Perangkat", ["Modul Ajar", "Modul Praktik/Projek"])
        status_modul = st.radio("Status Ketersediaan", ["Sudah Ada", "Belum Ada (Upload File)"], horizontal=True)
        
        file_modul = None
        if status_modul == "Belum Ada (Upload File)":
            file_modul = st.file_uploader(f"📎 Lampirkan {adm_tipe}", type=['pdf', 'jpg', 'png', 'jpeg'])
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        lokasi = st.radio("📍 Lokasi Belajar", ["Di Kelas", "Di Lab/Bengkel", "Di Lapangan"], horizontal=True)
        kelas = st.selectbox("🏫 Kelas / Rombel", [
            "X MPLB", "XI MPLB", "XII MPLB",
            "X TJKT", "XI TJKT", "XII TJKT",
            "X DKV", "XI DKV", "XII DKV",
            "--- KELAS GABUNGAN ---",
            "SEMUA KELAS X", "SEMUA KELAS XI", "SEMUA KELAS XII",
            "SELURUH SISWA (X, XI, XII)"
        ])
        jam_ke = st.text_input("⏱️ Jam Ke", placeholder="Contoh: 1 - 4")
        
    with col2:
        st.markdown("### 👥 Absensi & Materi")
        st.markdown("<div style='background-color:#FEE2E2; padding:15px; border-radius:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
        st.markdown("**Data Tidak Hadir:**")
        ca1, ca2 = st.columns([1, 3])
        with ca1: s_sakit = st.number_input("🤒 Sakit", min_value=0, step=1)
        with ca2: n_sakit = st.text_input("Nama Sakit", placeholder="Siapa yang sakit?")
        
        cb1, cb2 = st.columns([1, 3])
        with cb1: s_izin = st.number_input("✉️ Izin", min_value=0, step=1)
        with cb2: n_izin = st.text_input("Nama Izin", placeholder="Siapa yang izin?")
        
        cc1, cc2 = st.columns([1, 3])
        with cc1: s_alfa = st.number_input("🚫 Alfa", min_value=0, step=1)
        with cc2: n_alfa = st.text_input("Nama Alfa", placeholder="Siapa yang bolos?")
        st.markdown("</div>", unsafe_allow_html=True)
        
        materi = st.text_area("📖 Pokok Bahasan / Materi", placeholder="Tuliskan materi yang diajarkan hari ini...", height=100)
        kendala = st.text_area("📝 Catatan / Kendala", placeholder="Ceritakan kondisi kelas atau kendala jika ada...", height=100)
    
    st.markdown("---")
    st.markdown("### 📸 Dokumentasi Kegiatan")
    foto = st.camera_input("Klik tombol di bawah untuk ambil foto kegiatan")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.button("🚀 SIMPAN JURNAL & KIRIM LAPORAN", use_container_width=True)

    if submit:
        if nama and mapel and foto:
            if status_modul == "Belum Ada (Upload File)" and file_modul is None:
                st.error("⚠️ Pak/Bu, file modulnya jangan lupa di-upload dulu ya!")
            else:
                with st.spinner("⏳ Sedang menyimpan data ke sistem..."):
                    try:
                        res_foto = cloudinary.uploader.upload(foto)
                        url_foto = res_foto["secure_url"]
                        
                        url_modul_final = "Sudah Ada"
                        if file_modul:
                            res_m = cloudinary.uploader.upload(file_modul)
                            url_modul_final = res_m["secure_url"]
                        
                        df_lama = conn.read(spreadsheet=URL_SHEET, ttl=0)
                        data_baru = pd.DataFrame([{
                            "Hari": hari_input, "Tanggal": tgl_input.strftime("%d/%m/%Y"),
                            "Nama Guru": nama, "Mapel": mapel, "Jenis": jenis_pertemuan,
                            "Administrasi": adm_tipe, "Link Modul": url_modul_final,
                            "Lokasi": lokasi, "Kelas": kelas, "Jam Ke": jam_ke,
                            "Materi": materi, "Jml Sakit": s_sakit, "Nama Sakit": n_sakit,
                            "Jml Izin": s_izin, "Nama Izin": n_izin, "Jml Alfa": s_alfa,
                            "Nama Alfa": n_alfa, "Kendala": kendala, "Link Foto": url_foto,
                            "Timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }])
                        
                        df_akhir = pd.concat([df_lama, data_baru], ignore_index=True)
                        conn.update(spreadsheet=URL_SHEET, data=df_akhir)
                        st.success("🎉 Berhasil! Jurnal telah tersimpan. Selamat beristirahat, Pak/Bu!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Aduh, ada gangguan sistem: {e}")
        else:
            st.warning("⚠️ Mohon lengkapi Nama, Mapel, dan Foto Kegiatan ya!")

# --- 4. FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; padding: 20px; background-color: #1E3A8A; color: white; border-radius: 15px;'>Developed with ❤️ by <br><b style='font-size: 1.2rem;'>RUAS STUDIO</b><br>© 2026 - SMK Nasional Bandung</div>", unsafe_allow_html=True)