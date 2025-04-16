from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User
import os
from flask_mail import Mail, Message
import pandas as pd
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import tensorflow.keras.losses
import numpy as np
import requests
from geopy.distance import geodesic 
from random import randint

#Inisialisasi Flask
app = Flask(
    __name__,
    template_folder="../frontend/capstone",
    static_folder="../frontend/capstone"
)
app.secret_key = "supersecretkey"

#Konfigurasi Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'xdzakyz@gmail.com'
app.config['MAIL_PASSWORD'] = 'dvzo wzct hxyc sjtg'
app.config['MAIL_DEFAULT_SENDER'] = 'xdzakyz@gmail.com'

mail = Mail(app)

#Konfigurasi API
KUNCI_API_CUACA = "9744e26280dda6530d2628c24167fbe7"
KUNCI_API_JARAK = "a45c7bf1-a037-453b-a7d2-2a4f46a8c5e2"

#Muat model dan data
model = load_model("model.h5", custom_objects={"mse": tensorflow.keras.losses.mse})
data_rating = pd.read_csv("ratings.csv")
data_tempat = pd.read_csv("places.csv")

data_rating = data_rating.rename(columns={'Place_Id': 'Place_id'})
data_tempat = data_tempat.rename(columns={'Place_name': 'Nama_Tempat'})

#Mapping aktivitas berdasarkan cuaca
AKTIVITAS_BERDASARKAN_CUACA = {
    "gunung": {
        "cerah": ["Mendaki ke puncak", "Foto sunrise", "Berkemah", "Bird watching"],
        "mendung": ["Trekking ringan", "Mengunjungi kawah", "Mengamati flora"],
        "hujan": ["Mengunjungi museum gunung", "Istirahat di penginapan", "Mencoba kuliner lokal"]
    },
    "kawah": {
        "cerah": ["Melihat biru kawah", "Foto panorama", "Trekking mengelilingi kawah"],
        "mendung": ["Mengamati aktivitas vulkanik", "Kunjungi museum geologi"],
        "hujan": ["Istirahat di penginapan", "Mencoba sauna alam"]
    },
    "kota": {
        "cerah": ["City tour", "Kulineran", "Belanja oleh-oleh", "Mengunjungi museum"],
        "mendung": ["Mengunjungi galeri seni", "Nongkrong di kafe", "Wisata kuliner"],
        "hujan": ["Nonton bioskop", "Mengunjungi mall", "Mencoba spa"]
    },
    "danau": {
        "cerah": ["Memancing", "Berperahu", "Foto panorama", "Berjemur"],
        "mendung": ["Jogging sekitar danau", "Mengamati burung"],
        "hujan": ["Mencoba kuliner ikan", "Istirahat di penginapan"]
    },
    "pantai": {
        "cerah": ["Berenang", "Snorkeling", "Sunbathing", "Voli pantai"],
        "mendung": ["Jalan-jalan di pantai", "Mengumpulkan kerang"],
        "hujan": ["Mencoba seafood", "Pijat pantai", "Istirahat di resort"]
    },
    "pulau": {
        "cerah": ["Island hopping", "Diving", "Snorkeling", "Foto bawah air"],
        "mendung": ["Jelajah pulau", "Mengunjungi desa nelayan"],
        "hujan": ["Istirahat di resort", "Mencoba kuliner laut"]
    },
    "taman nasional": {
        "cerah": ["Safari", "Foto satwa", "Trekking", "Camping"],
        "mendung": ["Mengamati satwa", "Kunjungi pusat informasi"],
        "hujan": ["Mengunjungi museum", "Istirahat di penginapan"]
    }
}

@app.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    if request.method == "POST":
        #Ambil kode yang dimasukkan oleh pengguna
        entered_code = ''.join(request.form.getlist('code'))  # Mengambil kode dari form input
        
        if entered_code == str(session.get('verification_code')):
            #Kode benar, arahkan ke halaman ubah password
            return redirect("/change_password")
        else:
            flash("Kode verifikasi salah.")
            return redirect("/verify_code")
    return render_template("verify_code.html")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        # Ambil password baru dari form
        new_password = request.form["new_password"]
        email = session.get("email")  # Ambil email dari session
        
        # Cek apakah email ada di database
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password  # Update password
            db.session.commit()
            flash("Kata sandi berhasil diperbarui.")
            return redirect("/login")  # Arahkan pengguna ke halaman login
        else:
            flash("Pengguna tidak ditemukan.")
            return redirect("/change_password")

    return render_template("change_password.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]

        user_exist = User.query.filter_by(email=email).first()
        if user_exist:
            #Generate verification code (4 digits for example)
            verification_code = randint(1000, 9999)

            #Send email with verification code
            message = Message(
                subject="Verifikasi Kode Reset Password",
                recipients=[email],
                body=f"Kode verifikasi Anda adalah {verification_code}. Gunakan kode ini untuk mereset kata sandi Anda."
            )
            try:
                mail.send(message)
                #Store the verification code and email in session
                session['verification_code'] = verification_code
                session['email'] = email  #Simpan email untuk penggunaan selanjutnya
                return redirect("/verify_code")
            except Exception as e:
                flash(f"Terjadi kesalahan saat mengirim email: {e}")
                return redirect("/reset_password")
        
        flash("Email tidak terdaftar")
        return redirect("/reset_password")
    return render_template("resetpw.html")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

print("Model terdaftar:", db.metadata.tables.keys())

with app.app_context():
    print("Model terdaftar:", db.metadata.tables.keys())  
    db.create_all()
    if os.path.exists("instance/users.db"):
        print("✅ File database ditemukan!")
    else:
        print("❌ File database belum dibuat")

def get_user(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user.id if user else None

@app.route("/")
def home():
    return render_template("index.html")

users = {}

@app.route("/signup", methods=["GET", "POST"])
def signup(): 
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

     
        user_exist = User.query.filter_by(email=email).first()
        if user_exist:
            flash("Email sudah terdaftar")
            return redirect("/signup")

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Signup berhasil! Silakan login.")
        return redirect("/signup")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            
            session["email"] = user.email
            session["user"] = user.name
            session["user_id"] = user.id  

            return redirect(url_for("wireframe1"))

        flash("Login gagal! Email atau password salah.")
        return redirect("/login")

    return render_template("login.html")

@app.route("/wireframe1", methods=["GET", "POST"])
def wireframe1():
    return render_template("wireframe1.html")

@app.route("/wireframe2", methods=["GET","POST"])
def wireframe2():
    return render_template("wireframe2.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/save_location", methods=["POST"])
def save_location():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    
    email = session.get("email") 
    user = User.query.filter_by(email=email).first()

    print("Latitude:", latitude)
    print("Longitude:", longitude)

    if user:
        user.latitude = latitude
        user.longitude = longitude
        db.session.commit()
        flash("Lokasi disimpan")
        return redirect(url_for("wireframe1"))
    else:
        flash("User tidak ditemukan")
        return redirect(url_for("wireframe1"))

def dapatkan_aktivitas(kategori, kondisi_cuaca):
    kategori = kategori.lower()
    for key in AKTIVITAS_BERDASARKAN_CUACA:
        if key in kategori:
            return AKTIVITAS_BERDASARKAN_CUACA[key].get(kondisi_cuaca, ["Aktivitas umum"])
    return ["Aktivitas umum"]

def dapatkan_cuaca(lat, lon):
    """Ambil data cuaca dari OpenWeatherMap"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={KUNCI_API_CUACA}&units=metric&lang=id"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            cuaca = data["weather"][0]["description"].lower()
            if "cerah" in cuaca:
                kondisi = "cerah"
            elif "mendung" in cuaca or "berawan" in cuaca:
                kondisi = "mendung"
            elif "hujan" in cuaca:
                kondisi = "hujan"
            else:
                kondisi = "tidak diketahui"
            
            return {
                "suhu": data["main"]["temp"],
                "kondisi": kondisi,
                "deskripsi": data["weather"][0]["description"].capitalize(),
                "ikon": data["weather"][0]["icon"]
            }
    except Exception as e:
        print(f"Error mengambil data cuaca: {e}")
    return None

def hitung_jarak(asal, tujuan):
    """Hitung jarak menggunakan API atau fallback ke geodesic"""
    try:
        url = f"https://graphhopper.com/api/1/route?point={asal[0]},{asal[1]}&point={tujuan[0]},{tujuan[1]}&vehicle=car&key={KUNCI_API_JARAK}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if "paths" in data:
            return data["paths"][0]["distance"] / 1000  # dalam km
    except Exception as e:
        print(f"Error API jarak: {e}")
    
    return geodesic(asal, tujuan).km

def rekomendasi_dasar(user_id, jumlah=5):
    """Rekomendasi berdasarkan model prediktif saja"""
    semua_tempat = set(data_rating["Place_id"].unique())
    tempat_di_rating = set(data_rating[data_rating["User_Id"] == user_id]["Place_id"])
    tempat_belum_di_rating = list(semua_tempat - tempat_di_rating)
    
    if not tempat_belum_di_rating:
        return []
    
    prediksi = model.predict([
        np.array([user_id] * len(tempat_belum_di_rating)),
        np.array(tempat_belum_di_rating)
    ])
    
    return sorted(zip(tempat_belum_di_rating, prediksi.flatten()), 
                 key=lambda x: x[1], reverse=True)[:jumlah]

def rekomendasi_cerdas(user_id, lokasi_user, jumlah=8):
    """Gabungkan rekomendasi berdasarkan rating, jarak, dan cuaca"""
    
    rekomendasi_awal = rekomendasi_dasar(user_id, jumlah*3)
    
    df = pd.DataFrame(rekomendasi_awal, columns=["Place_id", "Prediksi_Rating"])
    df = df.merge(data_tempat, on="Place_id", how="left")
    
    df['cuaca'] = df.apply(lambda x: dapatkan_cuaca(x['Latitude'], x['Longitude']), axis=1)
    df['jarak'] = df.apply(lambda x: hitung_jarak(lokasi_user, (x['Latitude'], x['Longitude'])), axis=1)
    
    df = df[df['cuaca'].apply(lambda x: x['kondisi'] if x else '') != 'hujan']
    
    df['skor'] = df.apply(lambda x: (
        0.6 * x['Prediksi_Rating'] + 
        0.2 * (1 / (1 + x['jarak'])) + 
        0.2 * (1 if x['cuaca'] and x['cuaca']['kondisi'] == 'cerah' else 0.5) 
    ), axis=1)
    
    return df.sort_values('skor', ascending=False).head(jumlah)

@app.route("/recommend", methods=["POST"])
def rekomendasi():
    try:
        user_id = session.get("user_id")
        
        user = User.query.filter_by(id=user_id).first()
        if not user or not user.latitude or not user.longitude:
            return jsonify({"error": "Lokasi pengguna tidak ditemukan"}), 404
        
        lokasi_user = (user.latitude, user.longitude) 

        rekomendasi = rekomendasi_cerdas(user_id, lokasi_user)
        
        if rekomendasi.empty:
            return jsonify({"error": "Tidak ada rekomendasi yang tersedia"}), 404
            
        hasil = []
        for _, row in rekomendasi.iterrows():
            kondisi_cuaca = row['cuaca']['kondisi'] if row['cuaca'] else 'tidak diketahui'
            aktivitas = dapatkan_aktivitas(row['Category'], kondisi_cuaca)
            
            hasil.append({
                "Place_id": row['Place_id'],
                "Place_Name": row['Nama_Tempat'],
                "Category": row['Category'],
                "Predicted_Rating": round(row['Prediksi_Rating'], 2),
                "Distance_km": round(row['jarak'], 1),
                "Weather": row['cuaca']['deskripsi'] if row['cuaca'] else "Tidak diketahui",
                "Temperature": row['cuaca']['suhu'] if row['cuaca'] else None,
                "Weather_Condition": kondisi_cuaca,
                "Activities": aktivitas,
                "Score": round(row['skor'], 3),
                "Latitude": row['Latitude'],
                "Longitude": row['Longitude'],
                "Image_URL": row['Image_URL']
            })
        
        return jsonify(hasil)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_destinasi_detail', methods=['GET'])
def get_destinasi_detail():
    #Ambil nama destinasi dari parameter query
    destinasi_name = request.args.get('name')

    #Baca data dari wisata-indonesia.csv
    wisata_df = pd.read_csv('places.csv')

    #Cari data berdasarkan nama destinasi
    destinasi = wisata_df[wisata_df['Place_name'] == destinasi_name].to_dict(orient='records')

    #Jika data ditemukan, tambahkan cuaca dan aktivitas
    if destinasi:
        destinasi = destinasi[0]  # Ambil data pertama (karena hasilnya list)

        #Ambil data cuaca berdasarkan koordinat
        cuaca = dapatkan_cuaca(destinasi['Latitude'], destinasi['Longitude'])
        destinasi['Weather'] = cuaca['deskripsi'] if cuaca else "Tidak diketahui"
        destinasi['Temperature'] = cuaca['suhu'] if cuaca else None

        #Ambil aktivitas berdasarkan kategori dan kondisi cuaca
        kondisi_cuaca = cuaca['kondisi'] if cuaca else "tidak diketahui"
        aktivitas = dapatkan_aktivitas(destinasi['Category'], kondisi_cuaca)
        destinasi['Activities'] = aktivitas

        return jsonify(destinasi)
    else:
        return jsonify({"error": "Destinasi tidak ditemukan"}), 404

@app.route("/users")
def list_users():
    users = User.query.all()  
    return render_template("users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
