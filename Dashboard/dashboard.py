import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_data = pd.read_csv('day_data.csv', parse_dates=['dteday'])
hour_data = pd.read_csv('hour_data.csv', parse_dates=['dteday'])

st.title("Dashboard Penyewaan Sepeda")

# Sidebar filter untuk memilih rentang tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Mulai Tanggal", day_data['dteday'].min())
end_date = st.sidebar.date_input("Sampai Tanggal", day_data['dteday'].max())

# Filter data berdasarkan rentang tanggal
filtered_data = day_data[(day_data['dteday'] >= pd.to_datetime(start_date)) & 
                         (day_data['dteday'] <= pd.to_datetime(end_date))]

# Rata-rata Penyewaan berdasarkan hari dalam seminggu
st.subheader('Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')

weekday_avg_cnt = filtered_data.groupby(filtered_data['dteday'].dt.weekday)['cnt'].mean()

plt.figure(figsize=(10,6))
sns.barplot(x=weekday_avg_cnt.index, y=weekday_avg_cnt, palette='coolwarm')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
plt.xlabel('Hari dalam Seminggu (0 = Minggu, 6 = Sabtu)')
plt.ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(plt)

# Pengaruh Kelembapan dan Suhu terhadap Penyewaan Sepeda
st.subheader('Pengaruh Kelembapan dan Suhu terhadap Penyewaan Sepeda')

plt.figure(figsize=(10,6))
sns.scatterplot(data=hour_data, x='hum', y='cnt', hue='weathersit', palette='coolwarm', alpha=0.6)
plt.title('Hubungan antara Kelembapan dan Penyewaan Sepeda')
plt.xlabel('Kelembapan')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.legend(title='Kondisi Cuaca', loc='upper right')
st.pyplot(plt)

plt.figure(figsize=(10,6))
sns.scatterplot(data=hour_data, x='temp', y='cnt', hue='weathersit', palette='coolwarm', alpha=0.6)
plt.title('Hubungan antara Suhu dan Penyewaan Sepeda')
plt.xlabel('Suhu')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.legend(title='Kondisi Cuaca', loc='upper right')
st.pyplot(plt)

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
