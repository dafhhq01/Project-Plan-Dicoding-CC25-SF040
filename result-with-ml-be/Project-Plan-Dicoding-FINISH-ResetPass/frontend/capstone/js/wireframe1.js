function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            showPosition,
            showError,
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert("Geolocation tidak didukung oleh browser ini.");
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    fetch("/save_location", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude
        })
    })
    .then(res => res.json())
    .then(data => console.log("Lokasi disimpan:", data))
    .catch(err => console.error("Gagal simpan lokasi:", err));
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("Akses lokasi ditolak.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Informasi lokasi tidak tersedia.");
            break;
        case error.TIMEOUT:
            alert("Permintaan lokasi timeout.");
            break;
        case error.UNKNOWN_ERROR:
            alert("Terjadi kesalahan lokasi.");
            break;
    }
}

function redirectToSearchPage() {
    
    window.location.href = "/wireframe2";
}

// Trigger getLocation ketika halaman selesai dimuat
window.onload = getLocation;



document.addEventListener("DOMContentLoaded", function () {
    const loadingPopup = document.getElementById("loading-popup");
    loadingPopup.style.display = "flex"; // Tampilkan pop-up loading

    fetch("/recommend", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        loadingPopup.style.display = "none"; // Sembunyikan pop-up loading

        const resultDiv = document.getElementById("result");

        // Buat kontainer utama untuk title, rekomendasi, dan tombol
        const recommendationWrapper = document.createElement("div");
        recommendationWrapper.classList.add("recommendation-wrapper");

        // Tambahkan title ke dalam recommendationWrapper
        const title = document.createElement("h2");
        title.textContent = "Rekomendasi Wisata untuk Anda";
        title.classList.add("recommendation-title");
        recommendationWrapper.prepend(title);

        // Tambahkan kontainer rekomendasi wisata
        const recommendationContainer = document.createElement("div");
        recommendationContainer.classList.add("recommendation-container");
        recommendationWrapper.appendChild(recommendationContainer);

        // Tangani jika ada error dari server
        if (data.error) {
            recommendationContainer.innerHTML = `<p class="error">${data.error}</p>`;
            resultDiv.appendChild(recommendationWrapper);
            return;
        }

        // Tambahkan rekomendasi wisata
        data.forEach(item => {
            recommendationContainer.innerHTML += `
                <div class="recommendation-item">
                    <img src="${item.Image_URL}" alt="${item.Place_Name}" class="destination-image" data-id="${item.Place_id}">
                    <p>${item.Place_Name}</p>
                </div>
            `;
        });

        // Tambahkan tombol "Cari Wisata" secara dinamis
        const searchButtonContainer = document.createElement("div");
        searchButtonContainer.classList.add("search-button-container");
        searchButtonContainer.innerHTML = `
            <a href="/wireframe2">
                <button class="search-button">Cari Wisata</button>
            </a>
        `;

        // Tambahkan tombol ke dalam recommendationWrapper
        recommendationWrapper.appendChild(searchButtonContainer);

        // Tambahkan recommendationWrapper ke dalam resultDiv
        resultDiv.appendChild(recommendationWrapper);

        document.querySelectorAll(".destination-image").forEach(image => {
            image.addEventListener("click", function () {
                const placeName = this.getAttribute("alt"); // Gunakan nama destinasi dari atribut alt
        
                // Tampilkan loading saat mengambil data
                const popupContainer = document.getElementById("popup-container");
                const popupDetails = document.getElementById("popup-details");
                popupDetails.innerHTML = "<p>Memuat detail destinasi...</p>";
                popupContainer.style.display = "flex";
        
                // Ambil data detail dari endpoint /get_destinasi_detail
                fetch(`/get_destinasi_detail?name=${encodeURIComponent(placeName)}`)
                    .then(response => response.json())
                    .then(destination => {
                        if (destination.error) {
                            popupDetails.innerHTML = `<p>${destination.error}</p>`;
                        } else {
                            // Tampilkan rincian wisata di dalam pop-up
                            popupDetails.innerHTML = `
                                <h3>Deskripsi</h3>
                                <p>${destination.Description || "Deskripsi tidak tersedia"}</p>
                                
                                <h3>Lokasi</h3>
                                <p>${destination.Address || "Alamat tidak tersedia"}</p>
                                
                                <h3>Koordinat</h3>
                                <p>Latitude: ${destination.Latitude}, Longitude: ${destination.Longitude}</p>
                                
                                <h3>Kategori</h3>
                                <p>${destination.Category}</p>
                                
                                <h3>Cuaca Saat Ini</h3>
                                <p>${destination.Weather || "Tidak diketahui"} (${destination.Temperature || "N/A"}°C)</p>
                                
                                <h3>Aktivitas yang Direkomendasikan</h3>
                                <ul>
                                    ${destination.Activities.map(activity => `<li>${activity}</li>`).join('')}
                                </ul>
                            `;
                        }
                    })
                    .catch(error => {
                        popupDetails.innerHTML = `<p>Terjadi kesalahan: ${error.message}</p>`;
                    });
            });
        });

        // Tambahkan event listener untuk tombol tutup pop-up
        const closePopupButton = document.getElementById("close-popup");
        closePopupButton.addEventListener("click", function () {
            const popupContainer = document.getElementById("popup-container");
            popupContainer.style.display = "none"; // Sembunyikan pop-up
        });
    })
    .catch(error => {
        document.getElementById("result").innerHTML = 
            `<p class="error">Terjadi kesalahan: ${error.message}</p>`;
    });
});