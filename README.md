# Rondee FastAPI


## 🇮🇩 Rondee FastAPI - API Pengenalan Objek Budaya Pulau Penyengat

**Rondee FastAPI** adalah backend API berbasis FastAPI untuk mengenali objek budaya di Pulau Penyengat dari gambar yang diunggah. Menggunakan deep learning (CNN dengan MobileNetV2), API ini memberikan hasil klasifikasi gambar, informasi budaya, dan audio deskripsi secara otomatis.

🔗 **Demo API**: [https://ronde-pakai-emping.onrender.com](https://ronde-pakai-emping.onrender.com)

---

### 🎯 Kegunaan

Digunakan oleh aplikasi mobile/web untuk:

* Mengenali landmark budaya dari gambar.
* Memberikan informasi deskriptif: sejarah, lokasi, arsitektur.
* Menyediakan audio deskripsi otomatis (TTS).

---

### 📦 Endpoint API

* `POST /predict` → Kirim gambar dan terima informasi lengkap tentang landmark.
* `GET /` → Healthcheck (cek status API).

Contoh response JSON:

```json
{
  "label": "Masjid Raya Sultan Riau",
  "confidence": "98.76%",
  "description": "...",
  "location": "...",
  "history": "...",
  "architecture": "...",
  "audio_url": "/static/tts_XXXXX.mp3",
  "note": "✅ Gambar dikenali dengan baik."
}
```

---

### 🛠 Cara Pakai

1. **Jalankan Lokal** (butuh Python, pip, dan model):

```bash
uvicorn app:app --reload
```

2. **Upload Gambar** melalui:

   * Swagger UI: `http://localhost:5000/docs`
   * Atau gunakan `curl`:

```bash
curl -X POST "https://ronde-pakai-emping.onrender.com/predict" \
 -H "accept: application/json" \
 -H "Content-Type: multipart/form-data" \
 -F "file=@namafile.jpg;type=image/jpeg"
```

3. **Mainkan Audio** dari field `audio_url` yang diberikan dalam response.

---

### ⚙️ Struktur Proyek & Model

```
📁 models/
 ├── rondee-model-terbaru.h5      # Trained model
 └── labels.json                   # Metadata info setiap kelas

📁 static/                         # Folder hasil audio TTS (otomatis dibuat)
📄 app.py                          # Source code utama FastAPI
📄 Dockerfile                      # Konfigurasi container Docker
📄 requirements.txt                # Daftar dependency Python
```

---

### 🧪 Testing

* Swagger Docs: buka `/docs`
* Gunakan Postman untuk `POST /predict`
* Minimal gambar ukuran 224x224 JPG/PNG.

---

### 🐳 Jalankan dengan Docker

```bash
docker build -t rondee-fastapi .
docker run -p 5000:5000 rondee-fastapi
```

---

### ⚠️ Kendala Diketahui

* `gTTS` tidak selalu bekerja di hosting gratis seperti Render (karena pembatasan akses internet / codec).
* Model akan sulit mengenali gambar buram, gelap, atau dari sudut yang ekstrem.

---

## 🌍 Rondee FastAPI (English)

**Rondee FastAPI** is a lightweight API service that performs cultural landmark recognition from image uploads, using a CNN-based deep learning model trained on real cultural data from Pulau Penyengat.

🔗 **Demo**: [https://ronde-pakai-emping.onrender.com](https://ronde-pakai-emping.onrender.com)

---

### 🎯 Purpose

This API is useful for:

* Detecting cultural heritage objects via uploaded images.
* Delivering detailed metadata: description, location, history, architecture.
* Serving automatic spoken description via TTS (Text-to-Speech).

---

### 📦 API Endpoints

* `POST /predict` → Submit image, receive label + info + audio.
* `GET /` → Status check.

Example response:

```json
{
  "label": "Masjid Raya Sultan Riau",
  "confidence": "98.76%",
  "description": "...",
  "location": "...",
  "history": "...",
  "architecture": "...",
  "audio_url": "/static/tts_XXXXX.mp3",
  "note": "✅ Image recognized with high confidence."
}
```

---

### 🛠 How to Use

1. **Run locally**:

```bash
uvicorn app:app --reload
```

2. **Test API** via:

   * Swagger UI: `/docs`
   * cURL:

```bash
curl -X POST "https://ronde-pakai-emping.onrender.com/predict" \
 -H "accept: application/json" \
 -H "Content-Type: multipart/form-data" \
 -F "file=@yourimage.jpg;type=image/jpeg"
```

3. **Play audio** from `audio_url` field.

---

### ⚙️ Project Structure

```
📁 models/        → trained .h5 model and labels.json
📁 static/        → generated MP3 audio files
📄 app.py         → FastAPI backend code
📄 Dockerfile     → container config
📄 requirements.txt → pip dependencies
```

---

### 🐳 Docker Support

```bash
docker build -t rondee-fastapi .
docker run -p 5000:5000 rondee-fastapi
```

---

### ⚠️ Known Issues

* gTTS audio may fail on serverless platforms without outbound internet access.
* Model accuracy drops significantly on blurry or poorly lit photos.

---

### 👩‍💻 Developed by

**Vinsen**, **Aichan**, and **Nuswapada** 💜
