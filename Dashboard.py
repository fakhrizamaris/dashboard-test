import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style seaborn
sns.set(style='dark')

# Load dataset day_df dan hour_df
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Mengonversi kolom tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Dashboard header
st.header('Dashboard Bike Sharing')

# Filter berdasarkan rentang tanggal
st.sidebar.header('Filter Rentang Waktu')
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

start_date, end_date = st.sidebar.date_input('Pilih Rentang Tanggal', [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data berdasarkan tanggal
filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]


st.subheader('Total Penyewaan Sepeda per Hari')
col1, col2 = st.columns(2)
with col1:
    total_rentals = filtered_day_df['cnt'].sum()
    st.metric("Total Penyewaan Sepeda", value=total_rentals)

with col2:
    filtered_day_df['month'] = filtered_day_df['dteday'].dt.to_period('M').apply(lambda r: r.start_time)
    monthly_rentals = filtered_day_df.groupby('month')['cnt'].sum().reset_index()
    average_rentals_per_mounth = monthly_rentals['cnt'].mean()
    st.metric("Rata - Rata Sewa Per Bulan", value=f"{average_rentals_per_mounth:.2f}")

# Visualisasi 1: Total Penyewaan per Hari

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='dteday', y='cnt', data=filtered_day_df, marker='o', ax=ax)
ax.set_title('Total Penyewaan Sepeda per Hari')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 2: Penyewaan Sepeda Berdasarkan Jam
st.subheader('Penyewaan Sepeda Berdasarkan Jam')

total_rentals_per_hour = hour_df.groupby('hr').agg({'cnt': 'sum'}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='hr', y='cnt', data=total_rentals_per_hour, ax=ax, palette='Blues_d')
ax.set_title('Total Penyewaan Sepeda Berdasarkan Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 3: Perbandingan Pengguna Casual dan Registered
st.subheader('Perbandingan Penyewaan Pengguna Casual vs Registered')

total_casual = day_df['casual'].sum()
total_registered = day_df['registered'].sum()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(['Casual', 'Registered'], [total_casual, total_registered], color=['#1f77b4', '#ff7f0e'])
ax.set_title('Total Penyewaan: Casual vs Registered')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 4: Pengaruh Cuaca terhadap Penyewaan
st.subheader('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')

weather_grouped = day_df.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_grouped, ax=ax, palette='coolwarm')
ax.set_title('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')
ax.set_xlabel('Kondisi Cuaca (1.Cerah 2.Berawan 3.Mendung)')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)




