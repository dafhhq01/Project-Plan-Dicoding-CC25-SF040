# 📌 Dokumentasi ERD & Skema Database

## 📍 1. Deskripsi Database
Database ini dirancang untuk menyimpan informasi terkait tempat wisata, kondisi cuaca di lokasi wisata, serta rekomendasi aktivitas berdasarkan cuaca.

---

## 🏗 2. Entity Relationship Diagram (ERD)
```mermaid
erDiagram
    USERS {
        int id PK
        varchar name
        varchar email UNIQUE
        text password
        timestamp created_at DEFAULT CURRENT_TIMESTAMP
    }
    
    DESTINATIONS {
        int id PK
        varchar name
        varchar location
        varchar category
        text description
    }

    WEATHER {
        int id PK
        int destination_id FK
        float temperature
        int humidity
        float wind_speed
        varchar weather_condition
        timestamp timestamp DEFAULT CURRENT_TIMESTAMP
    }

    RECOMMENDATIONS {
        int id PK
        int user_id FK
        int destination_id FK
        int weather_id FK
        text recommended_activity
    }

    USERS ||--o{ RECOMMENDATIONS : has
    DESTINATIONS ||--o{ WEATHER : has
    DESTINATIONS ||--o{ RECOMMENDATIONS : has
    WEATHER ||--o{ RECOMMENDATIONS : based_on
```

---

## 📂 3. Tabel-Tabel Utama

### 1️⃣ **Tabel `users`**
| Kolom      | Tipe Data      | Keterangan                   |
|------------|---------------|------------------------------|
| `id`       | SERIAL (PK)    | ID pengguna                  |
| `name`     | VARCHAR(100)   | Nama pengguna                |
| `email`    | VARCHAR(100)   | Email unik                   |
| `password` | TEXT           | Password terenkripsi         |
| `created_at` | TIMESTAMP   | Waktu pendaftaran           |

---

### 2️⃣ **Tabel `destinations`**
| Kolom      | Tipe Data      | Keterangan                    |
|------------|---------------|--------------------------------|
| `id`       | SERIAL (PK)    | ID tempat wisata              |
| `name`     | VARCHAR(100)   | Nama tempat wisata            |
| `location` | VARCHAR(255)   | Lokasi                        |
| `category` | VARCHAR(50)    | Kategori wisata               |
| `description` | TEXT       | Deskripsi tempat wisata       |

---

### 3️⃣ **Tabel `weather`**
| Kolom           | Tipe Data      | Keterangan                       |
|-----------------|---------------|----------------------------------|
| `id`           | SERIAL (PK)    | ID data cuaca                   |
| `destination_id` | INT (FK)     | ID tempat wisata terkait        |
| `temperature`   | FLOAT         | Suhu dalam Celsius              |
| `humidity`      | INT           | Kelembaban udara (%)            |
| `wind_speed`    | FLOAT         | Kecepatan angin (m/s)           |
| `weather_condition` | VARCHAR(100) | Kondisi cuaca (Hujan/Cerah)   |
| `timestamp`     | TIMESTAMP     | Waktu pencatatan                |

---

### 4️⃣ **Tabel `recommendations`**
| Kolom           | Tipe Data      | Keterangan                         |
|-----------------|---------------|------------------------------------|
| `id`           | SERIAL (PK)    | ID rekomendasi                     |
| `user_id`      | INT (FK)       | ID pengguna                        |
| `destination_id` | INT (FK)     | ID tempat wisata yang direkomendasikan |
| `weather_id`   | INT (FK)       | ID cuaca terkait                   |
| `recommended_activity` | TEXT  | Aktivitas yang direkomendasikan   |

---

## 🚀 4. Relasi Antar Tabel
1. **`users` → `recommendations`** (One-to-Many)  
   - Seorang pengguna bisa memiliki banyak rekomendasi wisata.

2. **`destinations` → `weather`** (One-to-Many)  
   - Satu tempat wisata memiliki banyak data cuaca yang diperbarui.

3. **`destinations` → `recommendations`** (One-to-Many)  
   - Satu tempat wisata bisa direkomendasikan ke banyak pengguna.

4. **`weather` → `recommendations`** (One-to-Many)  
   - Satu kondisi cuaca bisa memiliki banyak rekomendasi aktivitas.

---

## 🎯 5. Kesimpulan
Struktur database ini memungkinkan sistem untuk menyimpan data pengguna, tempat wisata, informasi cuaca, serta rekomendasi aktivitas berdasarkan cuaca. Relasi antar tabel dirancang untuk mempermudah pengolahan data dan memberikan pengalaman pengguna yang lebih baik.

🔥 **Siap digunakan untuk integrasi dengan Backend!** 🔥
```

📌 **Cara Pakai**:  
1. **Simpan file sebagai** `erd_documentation.md`.  
2. **Gunakan di GitHub** atau Markdown viewer untuk melihat diagram ERD.  
3. **Diagram ERD bisa digenerate langsung di**: [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor).