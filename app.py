import streamlit as st
import google.generativeai as genai
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Bantu.AI - Logistik Pintar", layout="wide")

# Konfigurasi API Gemini
API_KEY = "AIzaSyCPcIw2STmbQWN6mafPgbxAAqL761fmpu8"
genai.configure(api_key=API_KEY)

available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
model = genai.GenerativeModel(available_models[0]) if available_models else None

# Koneksi Google Sheets
@st.cache_resource
def get_google_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_info = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Bantu.AI - Logistik").sheet1
        return sheet
    except Exception as e:
        return None

# Style CSS
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #ffffff; }
    .stMetric { background-color: #1E1E1E; padding: 15px; border-radius: 10px; color: #ffffff; border-left: 5px solid #FF4B4B; }
    .stButton>button { 
        width: 100%; border-radius: 20px; background: linear-gradient(to right, #FF4B4B, #FF8E53); 
        color: white; font-weight: bold; padding: 12px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2555/2555001.png", width=100)
    st.title("Bantu.AI")
    st.caption("Inovasi Digital untuk Logistik Bencana")
    st.divider()
    st.write("Status: Posko Pusat")
    st.write("Petugas: Relawan")
    if st.button("Refresh Data"):
        st.rerun()

# Header
st.title("Sistem Manajemen Logistik Darurat")
st.caption("Pencatatan Bantuan Berbasis Computer Vision & Cloud Sync")
st.divider()

# Ambil data
sheet = get_google_sheet()
data_df = pd.DataFrame()

if sheet:
    raw_data = sheet.get_all_values()
    if len(raw_data) > 1:
        data_df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
        data_df.columns = data_df.columns.str.strip()
        data_df = data_df.dropna()

# Tabs menu
tab1, tab2, tab3 = st.tabs(["Scan Barang Masuk", "Dashboard Real-Time", "Asisten Siaga"])

with tab1:
    col_cam, col_res = st.columns([0.6, 0.4])
    with col_cam:
        st.markdown("### Kamera Pemindai")
        img_file = st.camera_input("")
    
    with col_res:
        st.markdown("### Hasil Analisis")
        if img_file:
            img = Image.open(img_file)
            st.image(img, use_container_width=True)
            
            if st.button("VERIFIKASI & SIMPAN KE CLOUD"):
                with st.spinner("Menganalisis..."):
                    try:
                        prompt = "Analisis gambar ini. Jika barang logistik bencana (makanan, minuman, obat, tenda, selimut, baju), jawab: [Nama Barang], [Jumlah], [Kategori]. Jika bukan, jawab: Bukan Barang Logistik."
                        
                        response = model.generate_content([prompt, img])
                        ai_result = response.text
                        waktu = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        
                        if "Bukan Barang Logistik" in ai_result:
                            sheet.append_row([waktu, "Objek Ditolak", "Invalid", ai_result])
                            st.warning("Objek tidak valid dicatat.")
                        else:
                            if "," in ai_result:
                                sheet.append_row([waktu, ai_result, "Valid", "Verified by AI"])
                                st.success("Berhasil disimpan ke Google Sheets!")
                                st.balloons()
                            else:
                                sheet.append_row([waktu, ai_result, "Valid", "Verified by AI"])
                                st.success("Tersimpan!")
                    except Exception as e:
                        st.error(f"Error: {e}")

with tab2:
    st.subheader("Dashboard Inventaris Terpusat")
    if not data_df.empty:
        # Metrics
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Total Scan", len(data_df))
        with c2: 
            valid_count = len(data_df[data_df['Status'] == 'Valid'])
            st.metric("Barang Valid", valid_count)
        with c3: 
            st.write("Database", "Google Sheets")
            st.link_button("Lihat di Sheets", "https://docs.google.com/spreadsheets/d/1qpg3WA3mWNTc_izKcx9bDrmAHuQhGPc_Zc3WCTD3o-k/edit?usp=sharing")
        
        st.divider()
        
        # Table & Chart
        col_t, col_c = st.columns([0.6, 0.4])
        with col_t:
            st.dataframe(data_df.tail(10), use_container_width=True)
        
        with col_c:
            df_valid = data_df[data_df['Status'] == 'Valid'].copy()
            if not df_valid.empty:
                df_valid['Singkat'] = df_valid['Nama Barang'].apply(lambda x: x[:20] + '...')
                chart_data = df_valid['Singkat'].value_counts().reset_index()
                
                chart_data.columns = ['Barang', 'Jumlah']
                
                fig = px.bar(chart_data, 
                             x='Barang', 
                             y='Jumlah', 
                             color='Barang', 
                             template="plotly_dark",
                             labels={'Barang': 'Nama Logistik', 'Jumlah': 'Total Scan'})
                
                fig.update_layout(
                    showlegend=False, 
                    height=300,
                    xaxis_title="Jenis Bantuan",
                    yaxis_title="Frekuensi Masuk"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Belum ada data valid.")
    else:
        st.warning("Data kosong.")

with tab3:
    st.subheader("Asisten Siaga")
    tanya = st.text_input("Tanya prosedur:")
    if tanya:
        res = model.generate_content(f"Jawab singkat prosedur logistik bencana: {tanya}")
        st.chat_message("assistant").write(res.text)