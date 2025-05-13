from fastapi import FastAPI, File, UploadFile, BackgroundTasks
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

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load model dan label saat startup
model = None
labels = {}
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

@app.on_event("startup")
def load_model_and_labels():
    global model, labels
    print("🔄 Loading model dan label...")
    model = load_model("models/rondee-model-terbaru.h5")
    with open("models/labels.json", encoding="utf-8") as f:
        labels = json.load(f)

# TTS sebagai background task
def generate_audio(text, filename):
    try:
        tts = gTTS(text=text, lang="id")
        filepath = os.path.join("static", filename)
        tts.save(filepath)
        print(f"✅ Audio disimpan di {filepath}")
    except Exception as e:
        print(f"❌ Gagal generate TTS: {e}")

# Preprocessing gambar
def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.post("/predict")
async def predict(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    start = time.time()
    image_bytes = await file.read()
    img = preprocess_image(image_bytes)

    preds = model.predict(img)
    class_id = int(np.argmax(preds))
    confidence = float(np.max(preds))
    predicted_label = idx_to_label[class_id]
    label_info = labels[predicted_label]

    # Buat nama audio berdasarkan ID label
    filename = f"tts_{predicted_label}_{int(time.time())}.mp3"
    filepath = os.path.join("static", filename)

    # Buat audio di background
    if not os.path.exists(filepath):
        background_tasks.add_task(generate_audio, label_info["description"], filename)

    note = (
        "⚠️ Gambar mungkin kurang dikenali. Coba ambil ulang dari sudut berbeda atau pastikan kualitas foto jelas."
        if confidence < 0.70 else
        "✅ Gambar dikenali dengan baik."
    )

    print(f"✅ Prediction done in {time.time() - start:.2f}s")

    return JSONResponse({
        "label": label_info["name"],
        "confidence": f"{confidence * 100:.2f}%",
        "description": label_info["description"],
        "location": label_info["location"],
        "history": label_info["history"],
        "architecture": label_info["architecture"],
        "audio_url": f"/static/{filename}",
        "note": note
    })

@app.get("/")
def root():
    return {"message": "Rondee FastAPI is running!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000)
