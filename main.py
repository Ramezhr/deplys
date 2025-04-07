from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = FastAPI()

# Load model
model = load_model("pneumonia_xception_model.keras")

# Preprocessing function
def preprocess_image(image_data):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    image = image.resize((224, 224))  # Adjust to your model's expected size
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = preprocess_image(contents)
        prediction = model.predict(img)[0][0]  # Adjust based on model output shape

        result = "penomena" if prediction > 0.5 else "normal"
        return JSONResponse(content={"result": result, "confidence": float(prediction)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
