import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style seaborn
sns.set(style='dark')

def total_rentals_per_hour(hour_df):
    total_rentals = hour_df.groupby('hours').agg({'count': 'sum'}).reset_index()
    return total_rentals

def count_by_weather_situation(day_df):
    weather_situation_count = day_df.groupby('weather_situation').agg({'count': 'mean'}).reset_index()
    return weather_situation_count

def total_rentals(day_df):
    total_rentals = day_df.groupby('date').agg({'count': 'sum'}).reset_index()
    return total_rentals

def avg_rentals_per_month(day_df):
    monthly_rentals = day_df.groupby('month')['count'].sum().reset_index()
    average_rentals_per_mounth = monthly_rentals['count'].mean()
    return average_rentals_per_mounth

# Load dataset day_df dan hour_df
day_df = pd.read_csv("day_clean.csv")
hour_df = pd.read_csv("hour_clean.csv")

# Mengonversi kolom tanggal
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Dashboard header
st.header('Dashboard Bike Sharing')

# Filter berdasarkan rentang tanggal
st.sidebar.header('Filter Rentang Waktu')
min_date = day_df['date'].min()
max_date = day_df['date'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://miro.medium.com/v2/resize:fit:2000/0*TZ0bsPAR7gGvOoEu")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["date"] >= str(start_date)) & 
                (day_df["date"] <= str(end_date))]

total_rental_per_hour = total_rentals_per_hour(hour_df)
count_weather_situation = count_by_weather_situation(main_df)
total_rental = total_rentals(main_df) 
avg_rentals = avg_rentals_per_month(main_df)

st.subheader('Total Penyewaan Sepeda per Hari')
col1, col2 = st.columns(2)
with col1:
    total_rentals = main_df['count'].sum()
    st.metric("Total Penyewaan Sepeda", value=total_rentals)

with col2:
    main_df['month'] = main_df['date'].dt.to_period('M').apply(lambda r: r.start_time)
    st.metric("Rata - Rata Sewa Per Bulan", value=f"{avg_rentals:.2f}")

# Visualisasi 1: Total Penyewaan per Hari

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='date', y='count', data=main_df, marker='o', ax=ax)
ax.set_title('Total Penyewaan Sepeda per Hari')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 2: Penyewaan Sepeda Berdasarkan Jam
st.subheader('Penyewaan Sepeda Berdasarkan Jam')


fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='hours', y='count', data=total_rental_per_hour, ax=ax, palette='Blues_d')
ax.set_title('Total Penyewaan Sepeda Berdasarkan Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 3: Pengaruh Cuaca terhadap Penyewaan
st.subheader('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weather_situation', y='count', data=count_weather_situation, ax=ax, palette='coolwarm')
ax.set_title('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)




