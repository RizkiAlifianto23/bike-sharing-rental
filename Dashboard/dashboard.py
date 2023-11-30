import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')   


#Menyiapkan dataset
day_df  = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

#Menghapus kolom yang tidak diperlukan

#data_df
drop_col = ['instant','windspeed','temp', 'atemp','hum']

for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)

#hour_df
drop_col = ['instant','windspeed','temp', 'atemp','hum']

for i in hour_df.columns:
  if i in drop_col:
    hour_df.drop(labels=i, axis=1, inplace=True)

#merubah nama beberapa kolom
day_df.rename(columns={
    'dteday': 'ket_tanggal',
    'season' : 'musim',
    'holiday' : 'hari_libur',
    'weekday' : 'hari_biasa',
    'workingday' : 'hari_kerja',
    'weathersit' : 'cuaca',
    'yr': 'tahun',
    'mnth': 'bulan',
    'cnt': 'jumlah'
}, inplace=True)

hour_df.rename(columns={
    'dteday': 'ket_tanggal',
    'season' : 'musim',
    'holiday' : 'hari_libur',
    'weekday' : 'hari_biasa',
    'workingday' : 'hari_kerja',
    'weathersit' : 'cuaca',
    'yr': 'tahun',
    'mnth': 'bulan',
    'cnt': 'jumlah',
    'hr' : 'jam'
}, inplace=True)

#Mengubah value pada beberapa kolom menjadi keterangan informatif
#day_df
day_df['bulan'] = day_df['bulan'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
    7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
})
day_df['musim'] = day_df['musim'].map({
    1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'
})
day_df['hari_biasa'] = day_df['hari_biasa'].map({
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
})
day_df['cuaca'] = day_df['cuaca'].map({
    1: 'Cerah/Sebagian Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju Tipis/Hujan',
    4: 'Cuaca Buruk'
})

day_df['musim'] = day_df.musim.astype('category')
day_df['tahun'] = day_df.tahun.astype('category')
day_df['bulan'] = day_df.bulan.astype('category')
day_df['hari_libur'] = day_df.hari_libur.astype('category')
day_df['hari_biasa'] = day_df.hari_biasa.astype('category')
day_df['hari_kerja'] = day_df.hari_kerja.astype('category')
day_df['cuaca'] = day_df.cuaca.astype('category')

hour_df['bulan'] = hour_df['bulan'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
    7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
})
hour_df['musim'] = hour_df['musim'].map({
    1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'
})
hour_df['hari_biasa'] = hour_df['hari_biasa'].map({
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
})
hour_df['cuaca'] = hour_df['cuaca'].map({
    1: 'Cerah/Sebagian Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju Tipis/Hujan',
    4: 'Cuaca Buruk'
})
hour_df['musim'] = hour_df.musim.astype('category')
hour_df['tahun'] = hour_df.tahun.astype('category')
hour_df['bulan'] = hour_df.bulan.astype('category')
hour_df['hari_libur'] = hour_df.hari_libur.astype('category')
hour_df['hari_biasa'] = hour_df.hari_biasa.astype('category')
hour_df['hari_kerja'] = hour_df.hari_kerja.astype('category')
hour_df['cuaca'] = hour_df.cuaca.astype('category')

#membuat fungsi daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='ket_tanggal').agg({
        'jumlah': 'sum'
    }).reset_index()
    return daily_rent_df

#membuat fungsi hour_rent_df
def create_hour_rent_df(df):
  hour_rent_df = df.groupby(by='jam').agg({
    'jumlah' : 'sum'
  })
  return hour_rent_df

#membuat fungsi season_rent_df 
def create_season_rent_df(df):
  season_rent_df = df.groupby(by='musim').agg({
    'jumlah' : 'mean'
  })
  return season_rent_df

#membuat fungsi weather_rent_df
def create_weather_rent_df(df):
  weather_rent_df = df.groupby(by='cuaca').agg({
    'jumlah' : 'mean'
  })
  return weather_rent_df

#membuat fungsi weekday
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='hari_biasa').agg({
        'jumlah': 'sum'
    })
    ordered_weekdays = [
        'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu','Minggu'
        
    ]
    weekday_rent_df = weekday_rent_df.reindex(ordered_weekdays, fill_value=0)
    return weekday_rent_df

#membuat fungsi workingday
def create_workingday_rent_df(df):
  workingday_rent_df = df.groupby(by='hari_kerja').agg({
    'jumlah' : 'mean'
  })
  return workingday_rent_df

#membuat fungsi holiday
def create_holiday_rent_df(df):
  holiday_rent_df = df.groupby(by='hari_libur').agg({
    'jumlah' : 'mean'
  })
  return holiday_rent_df

#membuat month_rent_df
def create_month_rent_df(df):
    month_rent_df = df.groupby(by='bulan').agg({
        'jumlah': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
        'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'
    ]
    month_rent_df = month_rent_df.reindex(ordered_months, fill_value=0)
    return month_rent_df

#Membuat komponen filter
min_date = pd.to_datetime(day_df['ket_tanggal']).dt.date.min()
max_date = pd.to_datetime(day_df['ket_tanggal']).dt.date.max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df1 = day_df[(day_df['ket_tanggal'] >= str(start_date)) & 
                (day_df['ket_tanggal'] <= str(end_date))]

df2 = hour_df[(hour_df['ket_tanggal'] >= str(start_date)) & 
                (hour_df['ket_tanggal'] <= str(end_date))]

#menyiapkan beberapa dataframe
daily_rent_df = create_daily_rent_df(df1)
hour_rent_df = create_hour_rent_df(df2)
season_rent_df = create_season_rent_df(df1)
weather_rent_df = create_weather_rent_df(df1)
season_rent_df = create_season_rent_df(df1)
weekday_rent_df = create_weekday_rent_df(df1)
workingday_rent_df = create_workingday_rent_df(df1)
holiday_rent_df = create_holiday_rent_df(df1)
month_rent_df = create_month_rent_df(df1)

#membuat judul
st.header('Bike Rental Dashboard :sparkles:')

#membuat jumlah sewa harian
st.subheader('Daily Rentals Bike')
total_rental = daily_rent_df['jumlah'].sum()
st.metric('Total Rental', value=total_rental)

#berdasarkan cuaca
st.subheader('Weatherly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x='cuaca',
    y='jumlah',
    data=weather_rent_df,
    palette=colors,
    ax=ax
)
ax.set_title("Berdasarkan Cuaca", loc="center", fontsize=30)
ax.set_xlabel('Cuaca',fontsize=20)
ax.set_ylabel('Rata-rata Pengguna Sepeda',fontsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

#berdasarkan musim
st.subheader('Seasonly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))



sns.barplot(
    x='musim',
    y='jumlah',
    data=season_rent_df,
    palette=colors,
    ax=ax
)
ax.set_title("Berdasarkan Musim", loc="center", fontsize=30)
ax.set_xlabel('Musim',fontsize=30)
ax.set_ylabel('Rata-rata Pengguna Sepeda',fontsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

#Berdasarkan Bulan
st.subheader('Monthly Rentals')

fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    month_rent_df.index,
    month_rent_df['jumlah'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(month_rent_df['jumlah']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)



#berdasarkan workingday, weekday, holiday
st.subheader("Workingday, Weekday, Holiday Rentals")
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="jumlah", 
        x="hari_kerja",
        data=workingday_rent_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Based on Workingday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    
 
    sns.barplot(
        y="jumlah", 
        x="hari_libur",
        data=holiday_rent_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Based on Holiday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
sns.barplot(
    x="hari_biasa", 
    y="jumlah",
    data=weekday_rent_df,
    palette=colors,
    ax=ax
)
for index, row in enumerate(weekday_rent_df['jumlah']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
ax.set_title("Based on Weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


#berdasarkan jam
st.subheader('Hourly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))



sns.barplot(
    x='jam',
    y='jumlah',
    data=hour_rent_df,
    ax=ax
)
ax.set_title("Berdasarkan Jam", loc="center", fontsize=30)
ax.set_xlabel('Jam',fontsize=20)
ax.set_ylabel('Jumlah Pengguna Sepeda',fontsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)