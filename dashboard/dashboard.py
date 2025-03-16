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

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
option = st.sidebar.selectbox(
    "Pilih Analisis",
    ["RFM Analysis", "Clustering", "Segmentasi Musim & Cuaca", "Analisis Jam Sibuk", "Segmentasi Hari Kerja & Libur", "Segmentasi Musim", "Segmentasi Cuaca"]
)

# Tampilkan analisis berdasarkan pilihan
if option == "RFM Analysis":
    st.header("RFM Analysis")
    
    # Hitung Recency, Frequency, dan Monetary
    hour_df['Date'] = pd.to_datetime(hour_df['Date'])
    last_date = hour_df['Date'].max()
    hour_df['Recency'] = (last_date - hour_df['Date']).dt.days
    
    frequency_df = hour_df.groupby('Date')['Total Count'].count().reset_index()
    frequency_df.columns = ['Date', 'Frequency']
    
    monetary_df = hour_df.groupby('Date')['Total Count'].sum().reset_index()
    monetary_df.columns = ['Date', 'Monetary']
    
    rfm_df = pd.merge(frequency_df, monetary_df, on='Date')
    rfm_df = pd.merge(rfm_df, hour_df[['Date', 'Recency']], on='Date')
    
    st.write("Data RFM:")
    st.dataframe(rfm_df.head())
    
    # Visualisasi RFM
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x='Recency', y='Frequency', size='Monetary', data=rfm_df, sizes=(20, 200), ax=ax)
    ax.set_title('RFM Analysis: Recency vs Frequency (Ukuran: Monetary)')
    ax.set_xlabel('Recency (Hari)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

elif option == "Clustering":
    st.header("Clustering (Manual Grouping)")
    
    # Buat kategori berdasarkan jumlah penyewaan
    hour_df['Rental Category'] = pd.cut(hour_df['Total Count'],
                                        bins=[0, 50, 150, float('inf')],
                                        labels=['Low', 'Medium', 'High'])
    
    st.write("Data dengan Kategori Penyewaan:")
    st.dataframe(hour_df[['Total Count', 'Rental Category']].head())
    
    # Visualisasi kategori penyewaan
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='Rental Category', data=hour_df, order=['Low', 'Medium', 'High'], ax=ax)
    ax.set_title('Distribusi Kategori Penyewaan')
    ax.set_xlabel('Kategori Penyewaan')
    ax.set_ylabel('Jumlah')
    st.pyplot(fig)

elif option == "Segmentasi Musim & Cuaca":
    st.header("Segmentasi Berdasarkan Musim dan Cuaca")
    
    # Segmentasi berdasarkan musim dan cuaca
    segment_df = hour_df.groupby(['Season', 'Weather Situation'])['Total Count'].mean().reset_index()
    st.write("Rata-Rata Penyewaan Berdasarkan Musim dan Cuaca:")
    st.dataframe(segment_df)
    
    # Visualisasi segmentasi musim dan cuaca
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Season', y='Total Count', hue='Weather Situation', data=segment_df, ax=ax)
    ax.set_title('Rata-Rata Penyewaan Berdasarkan Musim dan Cuaca')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Fall', 'Spring', 'Summer', 'Winter'])
    ax.legend(title='Cuaca')
    st.pyplot(fig)

elif option == "Analisis Jam Sibuk":
    st.header("Analisis Jam Sibuk")
    
    # Hitung rata-rata penyewaan per jam
    hour_analysis = hour_df.groupby('Hour')['Total Count'].mean().reset_index()
    st.write("Rata-Rata Penyewaan per Jam:")
    st.dataframe(hour_analysis)
    
    # Visualisasi jam sibuk
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='Hour', y='Total Count', data=hour_analysis, marker='o', ax=ax)
    ax.set_title('Rata-Rata Penyewaan Sepeda per Jam')
    ax.set_xlabel('Jam (0-23)')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    ax.grid()
    st.pyplot(fig)

elif option == "Segmentasi Hari Kerja & Libur":
    st.header("Segmentasi Berdasarkan Hari Kerja dan Hari Libur")
    
    # Segmentasi berdasarkan hari kerja dan hari libur
    workingday_analysis = hour_df.groupby('Working Day')['Total Count'].mean().reset_index()
    st.write("Rata-Rata Penyewaan Berdasarkan Hari Kerja dan Hari Libur:")
    st.dataframe(workingday_analysis)
    
    # Visualisasi segmentasi hari kerja vs hari libur
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Working Day', y='Total Count', data=workingday_analysis, ax=ax)
    ax.set_title('Rata-Rata Penyewaan: Hari Kerja vs Hari Libur')
    ax.set_xlabel('Hari Kerja (1: Ya, 0: Tidak)')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Hari Libur', 'Hari Kerja'])
    st.pyplot(fig)

elif option == "Segmentasi Musim":
    st.header("Segmentasi Berdasarkan Musim")
    
    # Segmentasi berdasarkan musim
    season_analysis = hour_df.groupby('Season')['Total Count'].mean().reset_index()
    st.write("Rata-Rata Penyewaan Berdasarkan Musim:")
    st.dataframe(season_analysis)
    
    # Visualisasi segmentasi musim
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Season', y='Total Count', data=season_analysis, ax=ax)
    ax.set_title('Rata-Rata Penyewaan Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Fall', 'Spring', 'Summer', 'Winter'])
    st.pyplot(fig)

elif option == "Segmentasi Cuaca":
    st.header("Segmentasi Berdasarkan Cuaca")
    
    # Segmentasi berdasarkan cuaca
    weather_analysis = hour_df.groupby('Weather Situation')['Total Count'].mean().reset_index()
    st.write("Rata-Rata Penyewaan Berdasarkan Cuaca:")
    st.dataframe(weather_analysis)
    
    # Visualisasi segmentasi cuaca
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Weather Situation', y='Total Count', data=weather_analysis, ax=ax)
    ax.set_title('Rata-Rata Penyewaan Berdasarkan Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-Rata Jumlah Penyewaan')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Cerah', 'Hujan Ringan', 'Hujan Lebat', 'Berkabut'])
    st.pyplot(fig)