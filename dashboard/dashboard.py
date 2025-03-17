import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Analisis Penyewaan Sepeda")
st.write("Dashboard ini menampilkan hasil analisis dataset rental sepeda.")

# Muat dataset
@st.cache_data  # Cache data untuk meningkatkan performa
def load_data():
    # Ganti dengan URL dataset baru
    day_df = pd.read_csv("dashboard/data/day_clean.csv")
    hour_df = pd.read_csv("dashboard/data/hour_clean.csv")
    
    # Rename kolom
    day_df.rename(columns={
        'dteday': 'Date', 'season': 'Season', 'yr': 'Year', 'mnth': 'Month', 'holiday': 'Holiday',
        'weekday': 'Weekday', 'workingday': 'Working Day', 'weathersit': 'Weather Situation',
        'temp': 'Temperature', 'atemp': 'Apparent Temperature', 'hum': 'Humidity',
        'windspeed': 'Wind Speed', 'casual': 'Casual User', 'registered': 'Registered User', 'cnt': 'Total Count'
    }, inplace=True)
    
    hour_df.rename(columns={
        'dteday': 'Date', 'season': 'Season', 'yr': 'Year', 'mnth': 'Month', 'hr': 'Hour',
        'holiday': 'Holiday', 'weekday': 'Weekday', 'weathersit': 'Weather Situation',
        'temp': 'Temperature', 'atemp': 'Apparent Temperature', 'hum': 'Humidity',
        'windspeed': 'Wind Speed', 'casual': 'Casual User', 'registered': 'Registered User', 'cnt': 'Total Count'
    }, inplace=True)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar untuk filtering
st.sidebar.title("Filter Data")
min_date = pd.to_datetime(hour_df['Date']).min()
max_date = pd.to_datetime(hour_df['Date']).max()
start_date = st.sidebar.date_input("Tanggal Mulai", min_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date)

# Filter tambahan
selected_season = st.sidebar.selectbox("Pilih Musim", ["Semua"] + list(hour_df['Season'].unique()))
selected_weather = st.sidebar.selectbox("Pilih Cuaca", ["Semua"] + list(hour_df['Weather Situation'].unique()))
selected_workingday = st.sidebar.selectbox("Pilih Hari Kerja/Libur", ["Semua", "Hari Kerja", "Hari Libur"])

# Terapkan filtering
filtered_hour_df = hour_df[
    (pd.to_datetime(hour_df['Date']) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(hour_df['Date']) <= pd.to_datetime(end_date))
]

if selected_season != "Semua":
    filtered_hour_df = filtered_hour_df[filtered_hour_df['Season'] == selected_season]

if selected_weather != "Semua":
    filtered_hour_df = filtered_hour_df[filtered_hour_df['Weather Situation'] == selected_weather]

if selected_workingday != "Semua":
    if selected_workingday == "Hari Kerja":
        filtered_hour_df = filtered_hour_df[filtered_hour_df['Working Day'] == 1]
    else:
        filtered_hour_df = filtered_hour_df[filtered_hour_df['Working Day'] == 0]

# Tampilkan data yang difilter
st.subheader("Data yang Difilter")
st.write(filtered_hour_df.head())

# Visualisasi Interaktif
st.header("Visualisasi Interaktif")

# Pilih jenis visualisasi
visualization_option = st.selectbox(
    "Pilih Jenis Visualisasi",
    ["Distribusi Penyewaan per Jam", "Rata-Rata Penyewaan per Musim", "Rata-Rata Penyewaan per Cuaca"]
)

if visualization_option == "Distribusi Penyewaan per Jam":
    st.subheader("Distribusi Penyewaan per Jam")
    
    # Slider untuk memilih rentang jam
    hour_range = st.slider("Pilih Rentang Jam", 0, 23, (8, 17))
    
    # Filter data berdasarkan rentang jam
    filtered_by_hour = filtered_hour_df[
        (filtered_hour_df['Hour'] >= hour_range[0]) & (filtered_hour_df['Hour'] <= hour_range[1])
    ]
    
    # Hitung rata-rata penyewaan per jam
    hour_analysis = filtered_by_hour.groupby('Hour')['Total Count'].mean().reset_index()
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Hour', y='Total Count', data=hour_analysis, ax=ax)
    ax.set_title(f'Rata-Rata Penyewaan per Jam ({hour_range[0]}:00 - {hour_range[1]}:00)')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    st.pyplot(fig)

elif visualization_option == "Rata-Rata Penyewaan per Musim":
    st.subheader("Rata-Rata Penyewaan per Musim")
    
    # Pilih musim untuk perbandingan
    selected_seasons = st.multiselect(
        "Pilih Musim untuk Dibandingkan",
        options=filtered_hour_df['Season'].unique(),
        default=filtered_hour_df['Season'].unique()
    )
    
    # Filter data berdasarkan musim yang dipilih
    season_analysis = filtered_hour_df[filtered_hour_df['Season'].isin(selected_seasons)]
    season_analysis = season_analysis.groupby('Season')['Total Count'].mean().reset_index()
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Season', y='Total Count', data=season_analysis, ax=ax)
    ax.set_title('Rata-Rata Penyewaan per Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Fall', 'Spring', 'Summer', 'Winter'])
    st.pyplot(fig)

elif visualization_option == "Rata-Rata Penyewaan per Cuaca":
    st.subheader("Rata-Rata Penyewaan per Cuaca")
    
    # Pilih cuaca untuk perbandingan
    selected_weathers = st.multiselect(
        "Pilih Cuaca untuk Dibandingkan",
        options=filtered_hour_df['Weather Situation'].unique(),
        default=filtered_hour_df['Weather Situation'].unique()
    )
    
    # Filter data berdasarkan cuaca yang dipilih
    weather_analysis = filtered_hour_df[filtered_hour_df['Weather Situation'].isin(selected_weathers)]
    weather_analysis = weather_analysis.groupby('Weather Situation')['Total Count'].mean().reset_index()
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Weather Situation', y='Total Count', data=weather_analysis, ax=ax)
    ax.set_title('Rata-Rata Penyewaan per Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Cerah', 'Hujan Ringan', 'Hujan Lebat', 'Berkabut'])
    st.pyplot(fig)