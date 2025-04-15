document.addEventListener("DOMContentLoaded", () => {
    const places = [
        {
            Place_name: "Bromo",
            Category: "Gunung",
            Description: "Gunung Bromo, terletak di Jawa Timur, adalah gunung berapi aktif...",
            Image_URL: "https://image.popbela.com/content-images/post/20231225/8aa929d9b2986a7c68fc365585a28ceb.jpg?width=1600&format=webp&w=1600"
        },
        {
            Place_name: "Kawah Ijen",
            Category: "Kawah",
            Description: "Kawah Ijen, terletak di Jawa Timur, adalah kawah gunung berapi...",
            Image_URL: "https://www.yukbanyuwangi.co.id/wp-content/uploads/2023/12/DJI_0126_1200-960x636.jpg"
        },
        {
            Place_name: "Yogyakarta",
            Category: "Kota",
            Description: "Yogyakarta adalah kota budaya di Indonesia yang terkenal...",
            Image_URL: "https://raminten.com/wp-content/uploads/2024/07/tugu-jogja.jpg"
        },
        {
            Place_name: "Bandung",
            Category: "Kota",
            Description: "Bandung adalah ibu kota provinsi Jawa Barat yang terkenal...",
            Image_URL: "https://images.contentstack.io/v3/assets/blt00454ccee8f8fe6b/blt7f86b6cf7e72ffe7/61bc491f85b59c201581b414/US_Bandung_ID_Header.jpg?width=1440&quality=70&auto=webp"
        },
        {
            Place_name: "Danau Toba",
            Category: "Danau",
            Description: "Danau Toba adalah danau vulkanik terbesar di dunia...",
            Image_URL: "https://regalsprings.co.id/wp-content/uploads/2023/05/danau-toba-1536x1023.jpg"
        },
        {
            Place_name: "Bukittinggi",
            Category: "Kota",
            Description: "Bukittinggi adalah kota di Sumatera Barat yang terkenal...",
            Image_URL: "https://www.nusantaratv.com/2024/01/bukit-tinggi-1705294665-01-2024.jpg"
        },
        {
            Place_name: "Medan",
            Category: "Kota",
            Description: "Medan adalah ibu kota provinsi Sumatera Utara...",
            Image_URL: "https://www.rumah123.com/seo-cms/assets/Medan_Kota_c5625f2988/Medan_Kota_c5625f2988.webp"
        },
        {
            Place_name: "Rawa Pening",
            Category: "Danau",
            Description: "Rawa Pening adalah danau alami yang terletak di Jawa Tengah...",
            Image_URL: "https://asset.kompas.com/crops/7fxUSBj5r9NCj1jgOefVaLsKA2M=/0x0:1800x1200/1200x800/data/photo/2023/03/07/6406c3e71fd87.jpg"
        }
    ];

    const container = document.getElementById("places-container");

    places.forEach((place, index) => {
        const card = document.createElement("div");
        card.className = "place-card";
        card.innerHTML = `
            <img src="${place.Image_URL}" alt="${place.Place_name}" class="place-image" />
            <h2>${place.Place_name}</h2>
            <p><strong>Kategori:</strong> ${place.Category}</p>
            <p>${place.Description}</p>
        `;
        container.appendChild(card);
    });
});
