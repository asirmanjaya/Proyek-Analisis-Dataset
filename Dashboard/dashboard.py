import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the provided URLs
day_data = pd.read_csv('https://raw.githubusercontent.com/asirmanjaya/Proyek-Analisis-Dataset/main/Dashboard/day_data.csv')
hour_data = pd.read_csv('https://raw.githubusercontent.com/asirmanjaya/Proyek-Analisis-Dataset/main/Dashboard/hour_data.csv')

# Set page layout and title
st.set_page_config(layout="wide", initial_sidebar_state='expanded')
st.title('🚴‍♀️ Analisis Penyewaan Sepeda 🚴‍♂️')

# Sidebar for filters
st.sidebar.title("Filter Data")
selected_season = st.sidebar.selectbox('Pilih Musim:', options=[1, 2, 3, 4], format_func=lambda x: 'Musim Semi' if x == 1 else 'Musim Panas' if x == 2 else 'Musim Gugur' if x == 3 else 'Musim Dingin')
st.sidebar.markdown('---')

# Bagian 1: Pertanyaan Bisnis

# Pertanyaan 1: Pengaruh hari dalam seminggu terhadap jumlah sepeda yang disewa
st.subheader('📅 Pengaruh Hari dalam Seminggu terhadap Jumlah Sepeda yang Disewa')
weekday_avg_cnt = day_data.pivot_table(values='cnt', index='weekday', aggfunc='mean')

with st.container():
    plt.figure(figsize=(10,6))
    sns.barplot(x=weekday_avg_cnt.index, y=weekday_avg_cnt, palette='Blues')
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu', fontsize=14)
    plt.xlabel('Hari dalam Seminggu (0 = Minggu, 6 = Sabtu)', fontsize=12)
    plt.ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("📝 **Insight**: Penyewaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan hari libur.")
    st.markdown("<br>", unsafe_allow_html=True)

# Pertanyaan 2: Hubungan antara kondisi cuaca (kelembapan dan suhu) dengan jumlah sepeda yang disewa
st.subheader('🌦️ Hubungan Antara Kelembapan dan Suhu terhadap Jumlah Sepeda yang Disewa')

with st.container():
    # Scatterplot untuk Kelembapan
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=hour_data, x='hum', y='cnt', hue='weathersit', palette='Spectral', alpha=0.6)
    plt.title('Hubungan antara Kelembapan dan Penyewaan Sepeda', fontsize=14)
    plt.xlabel('Kelembapan', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)

    # Scatterplot untuk Suhu
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=hour_data, x='temp', y='cnt', hue='weathersit', palette='Spectral', alpha=0.6)
    plt.title('Hubungan antara Suhu dan Penyewaan Sepeda', fontsize=14)
    plt.xlabel('Suhu', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("📝 **Insight**: Kondisi cuaca yang cerah memiliki pengaruh signifikan pada jumlah penyewaan sepeda, terutama saat suhu lebih sejuk.")
    st.markdown("<br>", unsafe_allow_html=True)

# Bagian 2: Visualisasi (Exploratory Data Analysis)

# 1. Visualisasi jumlah penyewaan harian
st.subheader('📊 Visualisasi Jumlah Penyewaan Harian')
daily_rentals = day_data.groupby('dteday')['cnt'].sum()

with st.container():
    plt.figure(figsize=(10,6))
    plt.plot(daily_rentals.index, daily_rentals.values, color='blue', linestyle='--', marker='o')
    plt.title('Jumlah Penyewaan Sepeda Harian', fontsize=14)
    plt.xlabel('Tanggal', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)

# 2. Visualisasi penyewaan berdasarkan musim
st.subheader('☀️ Visualisasi Penyewaan Berdasarkan Musim')
seasonal_rentals = day_data[day_data['season'] == selected_season].groupby('season')['cnt'].sum()

with st.container():
    plt.figure(figsize=(10,6))
    sns.barplot(x=seasonal_rentals.index, y=seasonal_rentals.values, palette='Blues')
    plt.title('Penyewaan Berdasarkan Musim', fontsize=14)
    plt.xlabel('Musim', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)

# 3. Visualisasi penyewaan berdasarkan hari kerja vs hari libur
st.subheader('🏢 Visualisasi Penyewaan Berdasarkan Hari Kerja vs Hari Libur')
workday_rentals = day_data.groupby('workingday')['cnt'].sum()

with st.container():
    plt.figure(figsize=(10,6))
    sns.barplot(x=workday_rentals.index, y=workday_rentals.values, palette='Blues')
    plt.title('Penyewaan Berdasarkan Hari Kerja dan Hari Libur', fontsize=14)
    plt.xlabel('Hari (0 = Hari Libur, 1 = Hari Kerja)', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)

# 4. Visualisasi penyewaan berdasarkan kondisi cuaca
st.subheader('⛅ Visualisasi Penyewaan Berdasarkan Kondisi Cuaca')
day_data['is_rainy'] = day_data['weathersit'].apply(lambda x: 'Hujan' if x == 1 else 'Cerah')
rainy_rentals = day_data.groupby('is_rainy')['cnt'].sum()

with st.container():
    plt.figure(figsize=(10,6))
    sns.barplot(x=rainy_rentals.index, y=rainy_rentals.values, palette='Blues')
    plt.title('Penyewaan Berdasarkan Kondisi Cuaca', fontsize=14)
    plt.xlabel('Kondisi Cuaca', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)

# 5. Visualisasi penyewaan bulanan
st.subheader('📅 Visualisasi Penyewaan Bulanan')
monthly_rentals = day_data.groupby('mnth')['cnt'].sum()

with st.container():
    plt.figure(figsize=(10,6))
    sns.barplot(x=monthly_rentals.index, y=monthly_rentals.values, palette='Blues')
    plt.title('Penyewaan Bulanan', fontsize=14)
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)

# 6. Visualisasi penyewaan berdasarkan jam
st.subheader('⏰ Visualisasi Penyewaan Berdasarkan Jam')
hourly_rentals = hour_data.groupby('hr')['cnt'].sum()

with st.container():
    plt.figure(figsize=(10,6))
    plt.plot(hourly_rentals.index, hourly_rentals.values, color='green', linestyle='-', marker='o')
    plt.title('Penyewaan Berdasarkan Jam', fontsize=14)
    plt.xlabel('Jam', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)

# 7. Visualisasi rata-rata penyewaan per jam
st.subheader('📈 Visualisasi Rata-rata Penyewaan Per Jam')
hourly_avg_cnt = hour_data.pivot_table(values='cnt', index='hr', aggfunc='mean')

with st.container():
    plt.figure(figsize=(10,6))
    sns.lineplot(x=hourly_avg_cnt.index, y=hourly_avg_cnt['cnt'], palette='Blues')
    plt.title('Rata-rata Penyewaan Per Jam', fontsize=14)
    plt.xlabel('Jam', fontsize=12)
    plt.ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
    st.pyplot(plt)
    st.markdown("<br>", unsafe_allow_html=True)
