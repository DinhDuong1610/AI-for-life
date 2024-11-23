from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

model = YOLO("title_detection/models/best.pt")  

@app.post("/title-detection/")
async def predict(file: UploadFile = File(...)):
    try:
        # Đọc tệp ảnh từ yêu cầu
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Chạy mô hình YOLO trên ảnh
        results = model.predict(image, save=False)

        # Trích xuất thông tin từ kết quả
        predictions = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy() 
            classes = result.boxes.cls.cpu().numpy() 
            for box, cls in zip(boxes, classes):
                predictions.append({
                    "label": model.names[int(cls)],      # Lấy tên nhãn từ model.names
                    "confidence": float(result.boxes.conf[0]),  # Độ tin cậy của dự đoán
                    "bbox": [float(x) for x in box]     # Tọa độ bbox
                })

        return JSONResponse(content={"predictions": predictions})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "YOLOv8 API is running!"}

#run: uvicorn title_detection.api:app --reload --port 1610