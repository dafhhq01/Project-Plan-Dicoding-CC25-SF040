-- Buat database (jalankan hanya jika belum ada)
CREATE DATABASE wisata_cuaca;

-- Gunakan database wisata_cuaca
\c wisata_cuaca;

-- Tabel Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Destinations (Tempat Wisata)
CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    description TEXT
);

-- Tabel Weather (Data Cuaca)
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    destination_id INT REFERENCES destinations(id) ON DELETE CASCADE,
    temperature FLOAT NOT NULL,
    humidity INT NOT NULL,
    wind_speed FLOAT NOT NULL,
    weather_condition VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Recommendations (Rekomendasi Wisata)
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    destination_id INT REFERENCES destinations(id) ON DELETE CASCADE,
    weather_id INT REFERENCES weather(id) ON DELETE CASCADE,
    recommended_activity TEXT NOT NULL
);

-- Index untuk mempercepat pencarian
CREATE INDEX idx_weather_destination ON weather(destination_id);
CREATE INDEX idx_recommendations_user ON recommendations(user_id);
CREATE INDEX idx_recommendations_destination ON recommendations(destination_id);
