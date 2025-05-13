# 🇮🇩 Rondee FastAPI

**Rondee FastAPI** adalah REST API berbasis Python FastAPI yang dapat mengenali objek budaya dari Pulau Penyengat melalui gambar yang diunggah oleh pengguna, lalu memberikan deskripsi dan audio (TTS) otomatis.

🔗 Demo API: `https://ronde-pakai-emping.onrender.com`

---

## 🌟 Fitur

* 🔍 **Klasifikasi gambar landmark budaya** dari Pulau Penyengat
* 📜 Menampilkan **deskripsi, lokasi, sejarah, dan arsitektur**
* 🔊 Menyediakan **audio deskripsi** menggunakan TTS (`gTTS`)
* 🧠 Menggunakan **model deep learning (.h5, MobileNet)**

---

## 📦 Struktur Folder

```
RONDEE-ANGET/
├── app.py                   # FastAPI backend
├── models/                  # Trained model & label metadata
│   ├── rondee-model-terbaru.h5
│   └── labels.json
├── static/                  # Audio hasil TTS (auto-generated)
├── requirements.txt         # Dependency Python
├── Dockerfile               # Deploy config (Render-ready)
└── README.md                # Dokumentasi ini
```

---

## 🚀 Cara Menjalankan Lokal

### 1. Install dependensi

```bash
pip install -r requirements.txt
```

### 2. Jalankan server

```bash
uvicorn app:app --reload
```

Buka [http://localhost:8000/docs](http://localhost:8000/docs) untuk Swagger UI.

---

## 📬 API Documentation

### ♻️ `GET /`

Cek apakah API sedang aktif.

#### Contoh Response:

```json
{
  "message": "Rondee FastAPI is running!"
}
```

---

### 🖼️ `POST /predict`

Upload gambar dan dapatkan hasil klasifikasi.

#### 📥 Request

* **Method:** `POST`
* **Content-Type:** `multipart/form-data`
* **Body:** 1 file gambar (`file`)

#### ✅ Contoh cURL

```bash
curl -X POST "https://ronde-pakai-emping.onrender.com/predict" \
 -H "accept: application/json" \
 -H "Content-Type: multipart/form-data" \
 -F "file=@masjid.jpg;type=image/jpeg"
```

#### 📤 Response JSON:

```json
{
  "label": "Masjid Raya Sultan Riau",
  "confidence": "97.12%",
  "description": "Masjid yang dibangun oleh Sultan Riau...",
  "location": "Pulau Penyengat, Riau",
  "history": "...",
  "architecture": "...",
  "audio_url": "/static/tts_masjid-raya-sultan-riau_1715677890.mp3",
  "note": "✅ Gambar dikenali dengan baik."
}
```

---

## ⚙️ Teknologi yang Digunakan

* FastAPI
* TensorFlow / Keras
* Pillow
* NumPy
* gTTS
* Uvicorn
* Docker (untuk deploy ke Render)

---

## 📦 Deployment ke Render (Opsional)

1. Buat akun di [https://render.com](https://render.com)
2. Buat Web Service baru dari repo GitHub kamu
3. Pastikan file berikut ada:

   * `app.py`
   * `requirements.txt`
   * `Dockerfile`

---

## 👨‍💼 Developer

> Developed by Vinsen, Aichan, dan Nuswapada
> Untuk project AI Cultural Landmark Recognition – Pulau Penyengat, Batam 2025

---

## 🧠 Catatan

* Model hanya mengenali landmark budaya dari 7 kelas yang sudah dilatih.
* Audio TTS dihasilkan secara realtime (background task) dan otomatis disimpan di folder `/static`.
* Model `.h5` sebaiknya dioptimasi jika ingin digunakan di hosting production dengan resource terbatas.

---

## 📸 Contoh Gambar yang Didukung

* Masjid Raya Sultan Riau
* Balai Adat Melayu
* Gedung Tabib
* Bukit Kursi Meriam
* Rumah Hakim Raja Ali Haji
* Makam Engku Putri
* Makam Raja Ali Haji
