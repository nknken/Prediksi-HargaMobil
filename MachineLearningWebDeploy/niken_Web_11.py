import pickle
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os


# Load model prediksi harga mobil
file_path = os.path.join(os.getcwd(), 'model_prediksi_harga_mobil.sav')
model = pickle.load(open(file_path, 'rb'))

# Sidebar untuk navigasi aplikasi
st.sidebar.title("Navigasi Aplikasi")
app_mode = st.sidebar.selectbox(
    "Pilih Mode", ["Home", "Prediksi Harga Mobil", "Dataset & Visualisasi", "Tentang Aplikasi"]
)

if app_mode == "Home":
    st.title('Selamat Datang di Aplikasi Prediksi Harga Mobil')
    st.write("""
        Aplikasi ini memungkinkan Anda untuk:
        - Memprediksi harga mobil berdasarkan variabel tertentu seperti `Highway-mpg`, `Curbweight`, dan `Horsepower`.
        - Melihat dataset mobil lengkap dengan visualisasi interaktif.

        Gunakan menu di sebelah kiri untuk mulai menjelajahi fitur aplikasi ini. Selamat mencoba!
    """)
    st.image("car.jpg")

elif app_mode == "Prediksi Harga Mobil":
    st.title('Prediksi Harga Mobil')

    # Input nilai dari variabel independent
    st.write("Masukkan Nilai Variabel Independent untuk Prediksi Harga Mobil")
    highwaympg = st.number_input('Highway-mpg', min_value=0)
    curbweight = st.number_input('Curbweight', min_value=0)
    horsepower = st.number_input('Horsepower', min_value=0)

    # Tombol prediksi
    if st.button('Prediksi!'):
        try:
            # Prediksi variabel yang telah dimasukkan
            car_prediction = model.predict([[highwaympg, curbweight, horsepower]])

            # Convert ke string
            harga_mobil_str = np.array(car_prediction)
            harga_mobil_float = float(harga_mobil_str[0])

            # Tampilkan hasil prediksi
            harga_mobil_formatted = "Rp {:,.0f}".format(harga_mobil_float)
            st.success(f"**Prediksi Harga Mobil: {harga_mobil_formatted}**")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")

elif app_mode == "Dataset & Visualisasi":
    st.title('Dataset Mobil dan Visualisasi')

    try:
        # Baca file CSV
        df1 = pd.read_csv('CarPrice.csv')

        # Tampilkan dataset dalam bentuk tabel
        st.subheader("Tabel Dataset")
        st.dataframe(df1)

        # Tampilkan statistik deskriptif
        st.subheader("Statistik Deskriptif Dataset")
        st.write(df1.describe())

        # Grafik Highway-mpg vs Harga Mobil
        st.subheader("Grafik Highway-mpg vs Harga Mobil")
        chart_highwaympg = alt.Chart(df1).mark_line().encode(
            x=alt.X('highwaympg', title='Highway-mpg'),
            y=alt.Y('price', title='Harga Mobil'),
            tooltip=['highwaympg', 'price']
        ).properties(title='Highway-mpg vs Harga Mobil')
        st.altair_chart(chart_highwaympg, use_container_width=True)

        # Grafik Curbweight vs Harga Mobil
        st.subheader("Grafik Curbweight vs Harga Mobil")
        chart_curweight = alt.Chart(df1).mark_line().encode(
            x=alt.X('curbweight', title='Curbweight'),
            y=alt.Y('price', title='Harga Mobil'),
            tooltip=['curbweight', 'price']
        ).properties(title='Curbweight vs Harga Mobil')
        st.altair_chart(chart_curweight, use_container_width=True)

        # Grafik Horsepower vs Harga Mobil
        st.subheader("Grafik Horsepower vs Harga Mobil")
        chart_horsepower = alt.Chart(df1).mark_line().encode(
            x=alt.X('horsepower', title='Horsepower'),
            y=alt.Y('price', title='Harga Mobil'),
            tooltip=['horsepower', 'price']
        ).properties(title='Horsepower vs Harga Mobil')
        st.altair_chart(chart_horsepower, use_container_width=True)

    except FileNotFoundError:
        st.error("File dataset `CarPrice.csv` tidak ditemukan. Pastikan file sudah diunggah ke direktori yang sesuai.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses dataset: {e}")

elif app_mode == "Tentang Aplikasi":
    st.title("Tentang Aplikasi")
    st.markdown("""
    **Aplikasi Prediksi Harga Mobil** adalah aplikasi berbasis web yang memanfaatkan machine learning untuk memperkirakan harga mobil
    berdasarkan beberapa parameter seperti:
    - Highway-mpg
    - Curbweight
    - Horsepower

    ### Fitur Utama:
    - Prediksi harga mobil secara real-time
    - Visualisasi data dalam bentuk grafik interaktif
    - Tabel dan statistik deskriptif dataset

    Dikembangkan menggunakan:
    - **Python**: Bahasa pemrograman utama
    - **Streamlit**: Framework untuk aplikasi web
    - **Altair**: Visualisasi data

    Harap pastikan bahwa file `model_prediksi_harga_mobil.sav` dan `CarPrice.csv` sudah diunggah ke dalam folder proyek.
    """)
    
    st.info("Untuk bantuan lebih lanjut, silakan hubungi pengembang aplikasi.")
    st.write("Dikembangkan oleh: Niken Setyo N")

