import os
import pandas as pd
import streamlit as st

# Tentukan URL mentah GitHub untuk file CSV
day_data_url = 'https://raw.githubusercontent.com/asirmanjaya/Proyek-Analisis-Dataset/main/Dashboard/day_data.csv'
hour_data_url = 'https://raw.githubusercontent.com/asirmanjaya/Proyek-Analisis-Dataset/main/Dashboard/hour_data.csv'

# Coba untuk memuat file dari file lokal terlebih dahulu
day_file_path = 'day_data.csv'
hour_file_path = 'hour_data.csv'

day_data = None
hour_data = None

try:
    # Periksa akses file lokal
    day_accessible = os.access(day_file_path, os.R_OK)
    hour_accessible = os.access(hour_file_path, os.R_OK)

    if day_accessible and hour_accessible:
        day_data = pd.read_csv(day_file_path, parse_dates=['dteday'])
        hour_data = pd.read_csv(hour_file_path, parse_dates=['dteday'])
        st.write("File day_data.csv dan hour_data.csv dapat diakses dari lokal.")
    else:
        st.write("Izin file bermasalah. Memuat dari URL GitHub...")
        # Memuat file dari URL jika file lokal tidak dapat diakses
        day_data = pd.read_csv(day_data_url, parse_dates=['dteday'])
        hour_data = pd.read_csv(hour_data_url, parse_dates=['dteday'])
        st.write("File berhasil dimuat dari URL GitHub.")
except Exception as e:
    st.write("Terjadi kesalahan saat memuat file:", str(e))

# Cek apakah data berhasil dimuat
if day_data is not None and hour_data is not None:
    st.write("Data berhasil dimuat.")

    # Tampilkan beberapa baris pertama dari data untuk verifikasi
    st.subheader("Data Hari")
    st.write(day_data.head())

    st.subheader("Data Jam")
    st.write(hour_data.head())

    # Judul Dashboard
    st.title("Dashboard Penyewaan Sepeda")

    # Sidebar filter untuk memilih rentang tanggal
    st.sidebar.header("Filter Data")
    if 'dteday' in day_data.columns:
        start_date = st.sidebar.date_input("Mulai Tanggal", day_data['dteday'].min())
        end_date = st.sidebar.date_input("Sampai Tanggal", day_data['dteday'].max())

        filtered_data = day_data[(day_data['dteday'] >= pd.to_datetime(start_date)) & 
                                 (day_data['dteday'] <= pd.to_datetime(end_date))]

        # Jumlah Penyewaan Sepeda per Hari
        st.subheader("Jumlah Penyewaan Sepeda per Hari")
        st.line_chart(filtered_data[['dteday', 'cnt']].set_index('dteday'))

        # Penyewaan Berdasarkan Musim
        st.subheader("Penyewaan Berdasarkan Musim")
        season_chart = filtered_data.groupby('season')['cnt'].sum()
        st.bar_chart(season_chart)

        # Penyewaan Berdasarkan Hari Kerja atau Libur
        st.subheader("Penyewaan Berdasarkan Hari Kerja atau Libur")
        holiday_workday_chart = filtered_data.groupby(['holiday', 'workingday'])['cnt'].sum().unstack()
        st.bar_chart(holiday_workday_chart)

        # Penyewaan Berdasarkan Kondisi Cuaca
        st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")
        weather_chart = filtered_data.groupby('weathersit')['cnt'].sum()
        st.bar_chart(weather_chart)

        # Penyewaan Berdasarkan Jam
        st.subheader("Penyewaan Berdasarkan Jam")
        selected_day = st.sidebar.selectbox("Pilih Hari untuk Analisis Penyewaan Berdasarkan Jam", day_data['dteday'].dt.date.unique())
        hour_filtered_data = hour_data[hour_data['dteday'] == selected_day]
        hour_chart = hour_filtered_data.groupby('hr')['cnt'].sum()
        st.bar_chart(hour_chart)
    else:
        st.write("Kolom 'dteday' tidak ditemukan dalam data.")
else:
    st.write("Data tidak dapat dimuat. Periksa file CSV Anda.")
