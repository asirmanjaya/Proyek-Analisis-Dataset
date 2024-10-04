import os
import streamlit as st

day_file_path = 'day_data.csv'
hour_file_path = 'hour_data.csv'

st.write(f"Path saat ini: {os.getcwd()}")
st.write(f"Cek apakah day_data.csv ada: {os.path.exists(day_file_path)}")
st.write(f"Cek apakah hour_data.csv ada: {os.path.exists(hour_file_path)}")
