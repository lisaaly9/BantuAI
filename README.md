# Dokumentasi Proyek: Bantu.AI

## Deskripsi Sistem
Bantu.AI adalah sistem manajemen inventaris logistik darurat yang mengintegrasikan teknologi Computer Vision dan Sinkronisasi Cloud. Sistem ini dikembangkan untuk mengotomatisasi proses pencatatan bantuan logistik di posko bencana, meminimalisir kesalahan input manual, dan menyediakan data yang akurat secara real-time bagi pengambil keputusan.

## Fitur Utama
- **Otomatisasi Pencatatan (AI Vision)**: Menggunakan model Gemini 1.5 Flash untuk mengidentifikasi jenis barang, estimasi jumlah, dan kategori logistik melalui input kamera.
- **Dashboard Inventaris Real-time**: Visualisasi data stok barang masuk menggunakan library Plotly Express untuk memantau pergerakan logistik secara instan.
- **Integrasi Google Sheets**: Seluruh data tersimpan secara terpusat di Google Sheets API, memungkinkan akses data yang ringan dan kolaboratif.
- **Asisten Prosedur Bencana**: Fitur chatbot berbasis AI yang memberikan informasi cepat mengenai prosedur penanganan logistik darurat.
- **Ekspor Data**: Dukungan pengunduhan laporan inventaris dalam format CSV untuk keperluan administrasi dan pelaporan lanjut.

## Spesifikasi Teknologi
- **Bahasa Pemrograman**: Python 3.10 ke atas
- **Framework Interface**: Streamlit
- **Model Kecerdasan Buatan**: Google Generative AI (Gemini API)
- **Penyimpanan Data**: Google Sheets API
- **Analisis Data**: Pandas & Plotly Express

## Instruksi Instalasi

### Persiapan Lingkungan
Pastikan Python sudah terinstal, kemudian lakukan clone pada repositori ini.

```bash
git clone https://github.com/username/bantu-ai.git
cd bantu-ai
```

### Instalasi Dependensi
Instal pustaka yang diperlukan menggunakan pip:

```bash
pip install -r requirements.txt
```

### Konfigurasi Kredensial
- Tempatkan file `credentials.json` (Service Account Google Cloud) di folder utama.
- Pastikan API Key dari Google AI Studio telah dikonfigurasi pada variabel lingkungan atau langsung di dalam kode utama.

## Menjalankan Aplikasi
Gunakan perintah berikut untuk menjalankan server lokal:

```bash
streamlit run app.py
```

## Struktur Data
Sistem ini menyimpan data dengan struktur kolom sebagai berikut pada Google Sheets:

- **Waktu**: Timestamp pencatatan.
- **Nama Barang**: Hasil identifikasi nama dan kuantitas oleh AI.
- **Status**: Indikator validasi barang (Valid/Invalid).
- **Keterangan**: Catatan tambahan atau log error dari sistem.