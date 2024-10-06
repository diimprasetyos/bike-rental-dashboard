import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for Seaborn
sns.set(style='dark')

# Fungsi untuk memproses data harian
def create_daily_rentals_df(df):
    daily_rentals_df = df.groupby('dteday').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return daily_rentals_df

# Fungsi untuk memproses data jam-jam tertentu
def create_hourly_rentals_df(df):
    hourly_rentals_df = df.groupby('hr').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return hourly_rentals_df

# Load the datasets
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Mengubah kolom 'dteday' menjadi tipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Membuat dropdown untuk pilihan tahun
with st.sidebar:
    st.image("https://link-logo-perusahaan.com/logo.png")
    selected_year = st.selectbox(
        'Pilih Tahun',
        options=[2011, 2012],
        index=0
    )

# Filter data berdasarkan tahun yang dipilih
filtered_day_df = day_df[day_df['dteday'].dt.year == selected_year]
filtered_hour_df = hour_df[hour_df['dteday'].dt.year == selected_year]

# Membuat dataframe harian
daily_rentals_df = create_daily_rentals_df(filtered_day_df)

# Tampilan metrik di dashboard
st.header('Dashboard Penyewaan Sepeda :bicyclist:')
st.subheader(f'Penyewaan Harian Tahun {selected_year}')

col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_rentals_df['cnt'].sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    avg_daily_rentals = daily_rentals_df['cnt'].mean()
    st.metric("Rata-rata Penyewaan Harian", value=round(avg_daily_rentals, 2))

# Plot tren penyewaan harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(pd.to_datetime(daily_rentals_df['dteday']), daily_rentals_df['cnt'], marker='o', color='#90CAF9')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title(f'Tren Penyewaan Sepeda Harian Tahun {selected_year}')
st.pyplot(fig)

# perbandingan tipe pengguna
st.subheader(f"Rata-rata Penyewaan Berdasarkan Tipe Pengguna Tahun {selected_year}")

user_type_rentals = filtered_hour_df.groupby('hr').agg({'casual': 'mean', 'registered': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
user_type_rentals.plot(x='hr', y=['casual', 'registered'], kind='line', ax=ax)
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title(f'Rata-rata Penyewaan Berdasarkan Tipe Pengguna Tahun {selected_year}')
st.pyplot(fig)

# Monthly rental based on the selected year
st.subheader(f"Rata-rata Penyewaan Bulanan Tahun {selected_year}")
monthly_rental = filtered_day_df.groupby('mnth').agg({'cnt': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='mnth', y='cnt', data=monthly_rental, palette='Greens', ax=ax)
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title(f'Rata-rata Penyewaan Bulanan Tahun {selected_year}')
st.pyplot(fig)

# perbandingan weekday dan holiday
st.subheader("Rata-rata Penyewaan Berdasarkan Libur")
weekday_holiday = day_df.groupby('holiday').agg({'cnt': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='holiday', y='cnt', data=weekday_holiday, palette='Oranges', ax=ax)
ax.set_xlabel('Libur (0: Tidak, 1: Ya)')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title('Rata-rata Penyewaan Berdasarkan Libur')
st.pyplot(fig)

# pengaruh cuaca pada rental
st.subheader("Rata-rata Penyewaan Berdasarkan Cuaca")
weather_factor = day_df.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='weathersit', y='cnt', data=weather_factor, palette='Reds', ax=ax)
ax.set_xlabel('Kondisi Cuaca (1: Baik, 2: Sedang, 3: Buruk)')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title('Rata-rata Penyewaan Berdasarkan Cuaca')
st.pyplot(fig)

# pengaruh cuaca tiap jam
st.subheader("Pengaruh Cuaca pada Penyewaan Berdasarkan Jam")
weather_effect = hour_df.groupby(['hr', 'weathersit']).agg({'cnt': 'mean'}).unstack()

fig, ax = plt.subplots(figsize=(16, 8))
weather_effect.plot(kind='line', ax=ax)
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title('Pengaruh Cuaca pada Penyewaan Berdasarkan Jam')
st.pyplot(fig)

# Performa penyewaan berdasarkan jam
st.subheader("Penyewaan Berdasarkan Jam")
hourly_rentals_df = create_hourly_rentals_df(hour_df)

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='hr', y='cnt', data=hourly_rentals_df, palette='Blues', ax=ax)
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Jumlah Penyewaan Berdasarkan Jam')
st.pyplot(fig)
