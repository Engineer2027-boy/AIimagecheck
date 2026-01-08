from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from PIL import Image
import io

app = FastAPI()
# Allow React to communicate with this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load the AI detection model (this may take a moment on the first run)
# We use a model specifically trained to distinguish between real photos and AI
detector = pipeline("image-classification", model="umm-maybe/AI-image-detector")
@app.post("/detect")
async def detect_ai(file: UploadFile = File(...)):
    try:
        # 1. Read the uploaded bytes and convert to a PIL Image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # 2. Run the image through the AI model
        # The model returns a list like: [{'label': 'fake', 'score': 0.98}, ...]
        predictions = detector(image)
        
        # 3. Format the result
        top_prediction = predictions[0]
        label = "AI Generated" if top_prediction['label'] == 'fake' else "Human Created"
        confidence = top_prediction['score'] * 100

        return {
            "message": f"Result: {label} ({confidence:.2f}% confidence)",
            "status": "success"
        }
    except Exception as e:
        return {"message": f"Error: {str(e)}", "status": "error"}
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)