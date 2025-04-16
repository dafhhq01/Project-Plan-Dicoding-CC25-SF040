# API yang Akan Digunakan
Setelah melakukan riset dan pertimbangan, kita akan menggunakan BMKG API atau OpenWeatherMap API untuk mengambil data cuaca secara real-time.

## Alasan Pemilihan API
- **BMKG API** → Data resmi dari pemerintah Indonesia, lebih akurat untuk wilayah lokal.
- **OpenWeatherMap API** → Lebih fleksibel, gratis untuk penggunaan dasar, serta memiliki banyak fitur tambahan.

---

## Endpoint API & Cara Penggunaannya

### BMKG API
- **Endpoint:**  
  `https://data.bmkg.go.id/prakiraan-cuaca`

- **Request:**  
  ```json
  {
    "kota": "Jakarta"
  }
  ```

- **Response:**  
  ```json
  {
    "cuaca": "Cerah",
    "suhu": "30°C",
    "kelembaban": "70%"
  }
  ```

### OpenWeatherMap API
- **Endpoint:**  
  `https://api.openweathermap.org/data/2.5/weather?q=Jakarta&appid=API_KEY`

- **Response:**  
  ```json
  {
    "weather": [{"description": "clear sky"}],
    "main": {
      "temp": 303.15,
      "humidity": 70
    }
  }
  ```

---

## Perbandingan BMKG API vs OpenWeatherMap API

| Fitur                 | BMKG API          | OpenWeatherMap API |
|----------------------|------------------|--------------------|
| **Akurasi Lokal**     | ✅ Sangat Akurat | ⚠️ Cukup Akurat    |
| **Data Real-time**    | ✅ Ya            | ✅ Ya              |
| **Gratis?**          | ✅ Ya            | ✅ Tapi ada batasan |
| **Dokumentasi Lengkap** | ⚠️ Terbatas    | ✅ Lengkap         |
| **Kemudahan Integrasi** | ⚠️ Agak Ribet  | ✅ Mudah           |

---

## Kesimpulan & Langkah Selanjutnya
- **API Pilihan:**  
  - **BMKG API** untuk keakuratan tinggi.  
  - **OpenWeatherMap API** jika membutuhkan fleksibilitas lebih.

- **Tugas Berikutnya:**  
  ✅ Implementasi request API di `weatherService.js`.  
  ✅ Uji coba API dan cek format data agar mudah diproses di backend.

