from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import io
import json
import time
from gtts import gTTS

app = FastAPI(title="Rondee FastAPI")

# Buat folder static kalau belum ada
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load model
model = load_model("models/rondee-model-terbaru.h5")

# Load label info
with open("models/labels.json", encoding="utf-8") as f:
    labels = json.load(f)

# Urutan index ke label (pastikan sama kayak waktu training!)
class_indices = {
    'balai-adat-melayu': 0,
    'bukit-kursi-meriam': 1,
    'gedung-tabib': 2,
    'makam-engku-putri': 3,
    'makam-raja-ali-haji': 4,
    'masjid-raya-sultan-riau': 5,
    'rumah-hakim': 6
}
idx_to_label = {v: k for k, v in class_indices.items()}

# Preprocess gambar
def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = preprocess_image(image_bytes)

    preds = model.predict(img)
    class_id = int(np.argmax(preds))
    confidence = float(np.max(preds))

    predicted_label = idx_to_label[class_id]
    label_info = labels[predicted_label]

    # Text-to-speech
    text = label_info["description"]
    tts = gTTS(text=text, lang="id")
    filename = f"tts_{int(time.time())}.mp3"
    filepath = os.path.join("static", filename)
    tts.save(filepath)
    audio_url = f"/static/{filename}"

    note = (
        "⚠️ Gambar mungkin kurang dikenali. Coba ambil ulang dari sudut berbeda atau pastikan kualitas foto jelas."
        if confidence < 0.70 else
        "✅ Gambar dikenali dengan baik."
    )

    return JSONResponse({
        "label": label_info["name"],
        "confidence": f"{confidence*100:.2f}%",
        "description": label_info["description"],
        "location": label_info["location"],
        "history": label_info["history"],
        "architecture": label_info["architecture"],
        "audio_url": audio_url,
        "note": note
    })

@app.get("/")
def root():
    return {"message": "Rondee FastAPI is running!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
