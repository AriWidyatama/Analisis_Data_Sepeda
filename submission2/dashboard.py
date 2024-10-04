import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np

day_df = pd.read_csv("dashboard/days.csv")
hour_df = pd.read_csv("dashboard/hours.csv")

st.header('Projeck Analisis Data Sewa Sepeda :sparkles:')


# Data penyewa casual dan register berdasarkan season
with st.container():
    st.subheader('Visualisasi Dari Perbandingan Penyewa Casual dan Register Pada Setiap Season')
    customer_data = hour_df.groupby(by=["yr", "season"]).agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    customer_data['yr_season'] = customer_data['yr'].astype(str) + '-' + customer_data['season'].astype(str)

    ind = np.arange(len(customer_data)) 
    width = 0.35  # Lebar batang

    fig, ax = plt.subplots(figsize=(10, 6))

    bar1 = ax.bar(ind - width/2, customer_data['casual'], width, label='Penyewa Casual')
    bar2 = ax.bar(ind + width/2, customer_data['registered'], width, label='Penyewa Registered')

    ax.set_xlabel('Year and Season')
    ax.set_ylabel('Jumlah Penyewa')
    ax.set_title('Perbandingan penyewa Casual dan Register')

    ax.set_xticks(ind)
    ax.set_xticklabels([f'{customer_data["yr"][i]}-{customer_data["season"][i]}' for i in range(len(customer_data))])

    ax.legend()

    plt.tight_layout()

    st.pyplot(fig)

with st.expander("Kesimpulan"):
    st.write(
        """Penyewa Casual relatif lebih rendah dibandingkan penyewa Register untuk setiap musimnya.
        """
    )


# Statistik sewa setiap musim
with st.container():
    st.subheader('Visualisasi Statistik Penyewa Sepeda Dalam Setiap Season')
    season_data = day_df.groupby(by=["season"]).agg({
        "cnt": ["sum", "max", "min", "mean"]
    })

    season_data.columns = ['cnt_sum', 'cnt_max', 'cnt_min', 'cnt_mean']

    plt.figure(figsize=(10, 6))

    plt.plot(season_data.index, season_data['cnt_max'], label='Max penyewa', marker='o', color='green')
    plt.plot(season_data.index, season_data['cnt_min'], label='Min penyewa', marker='o', color='red')
    plt.plot(season_data.index, season_data['cnt_mean'], label='Mean penyewa', marker='o', color='orange')

    plt.xlabel("Season")
    plt.ylabel('Jumlah Penyewa')
    plt.title('Statistik Penyewa Setiap Musim')

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    st.pyplot(plt)

with st.expander("Kesimpulan"):
    st.write(
        """Musim 4 (musim dingin) pernah memiliki paling sedikit penyewa dalam satu hari, tapi juga memiliki paling banyak dalam satu hari.
        """
    )


# Perkembangan sewa setiap bulan
with st.container():
    st.subheader('Visualisasi Dari Grafik Perkembangan Jumlah Sewa Dalam Setiap Bulan')
    monthly_data = hour_df.groupby(by=["yr", "mnth"]).agg({"cnt": "sum"}).reset_index()

    plt.figure(figsize=(10, 6))

    plt.plot(monthly_data['mnth'] + (monthly_data['yr'] * 12), monthly_data['cnt'], marker='o', linestyle='-', color='b')

    plt.xlabel('Month (Year-Month)')
    plt.ylabel('Total Penyewa')
    plt.title('Grafik Sewa Sepeda dalam setiap Bulan')

    plt.grid(True)
    plt.xticks(ticks=range(1, 25), labels=[f'{y}-{m}' for y in range(0, 2) for m in range(1, 13)])

    plt.tight_layout()

    st.pyplot(plt)

with st.expander("Kesimpulan"):
    st.write(
        """Pada bulan desember ada penurunan jumlah sewa, yang perlahan menaik pada bulan pebruari.
        """
    )


# Mengelompokkan data berdasarkan jam sewa
with st.container():
    st.subheader('Visualisasi Jumlah Penyewa Dalam Setiap Jam')
    hourly_data = hour_df.groupby(by=["hr"]).cnt.sum().sort_values(ascending=True)

    plt.figure(figsize=(10, 6))

    hourly_data.plot(kind='barh', color='skyblue')

    plt.xlabel('Total Penyewa')
    plt.ylabel('Jam Sewa')
    plt.title('Grafik Sewa Berdasarkan Jam')

    plt.grid(axis='x')

    plt.tight_layout()

    st.pyplot(plt)

with st.expander("Kesimpulan"):
    st.write(
        """Sewa tertinggi berada di jam 17 sedangkan paling sedikit ada di jam 4.
        """
    )