from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from PIL import Image
import io
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
detector = pipeline("image-classification", model="prithivMLmods/Deep-Fake-Detector-Model")
@app.post("/detect")
async def detect_ai(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        predictions = detector(image)
        print(f"DEBUG: Model Output: {predictions}")
        top_pred = predictions[0]
        top_label = top_pred['label'].lower()
        top_score = top_pred['score'] * 100
        is_human_label = top_label in ['real', 'human', 'label_0'] 
        if is_human_label and top_score < 70:
            label = "AI Generated"
            confidence = 100 - top_score 
        elif is_human_label:
            label = "Human Created"
            confidence = top_score
        else:
            label = "AI Generated"
            confidence = top_score
        return {
            "message": f"Result: {label} ({confidence:.2f}% confidence)",
            "status": "success"
        }
    except Exception as e:
        print(f"ERROR: {e}") # This prints to your VS Code terminal
        return {"message": f"Error: {str(e)}", "status": "error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
