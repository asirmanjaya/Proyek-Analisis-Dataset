import os
import streamlit as st

day_file_path = 'day_data.csv'
hour_file_path = 'hour_data.csv'

day_accessible = os.access(day_file_path, os.R_OK)
hour_accessible = os.access(hour_file_path, os.R_OK)

if day_accessible and hour_accessible:
    st.write("File day_data.csv dan hour_data.csv dapat diakses.")
else:
    st.write("Izin file bermasalah. Periksa izin akses file.")
