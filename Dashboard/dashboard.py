import pandas as pd
import streamlit as st

# Tentukan URL mentah GitHub untuk file CSV
day_data_url = 'https://raw.githubusercontent.com/asirmanjaya/Proyek-Analisis-Dataset/main/Dashboard/day_data.csv'
hour_data_url = 'https://raw.githubusercontent.com/asirmanjaya/Proyek-Analisis-Dataset/main/Dashboard/hour_data.csv'

st.title("Dashboard Penyewaan Sepeda")

# Sidebar filter untuk memilih rentang tanggal
st.sidebar.header("Filter Data")
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
selected_day = st.sidebar.selectbox("Pilih Hari untuk Analisis Penyewaan Berdasarkan Jam", day_data['dteday'].unique())
hour_filtered_data = hour_data[hour_data['dteday'] == selected_day]
hour_chart = hour_filtered_data.groupby('hr')['cnt'].sum()
st.bar_chart(hour_chart)

  
