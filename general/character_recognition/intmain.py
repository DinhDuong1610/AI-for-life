from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import torch
import numpy as np
from character_recognition.imageprocessing import enhance_text_image

# Load config OCR
config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'

detector = Predictor(config)

def process_image_with_coordinates(image_path, coordinates_list):
    try:
        # Đọc ảnh từ file
        img = Image.open(image_path).convert("RGB")
        enhanced_img = enhance_text_image(np.array(img))
        enhanced_img_pil = Image.fromarray(enhanced_img)
    except Exception as e:
        print(f"Error loading or processing the image: {str(e)}")
        return []

    results = []  # Danh sách kết quả nhận diện

    # Duyệt qua từng tọa độ và thực hiện OCR
    for coords in coordinates_list:
        if len(coords) != 4:
            print(f"Invalid coordinates format: {coords}")
            continue

        min_x, min_y, max_x, max_y = coords

        # Cắt phần ảnh theo tọa độ
        cropped_img = enhanced_img_pil.crop((min_x, min_y, max_x, max_y))

        # Dự đoán văn bản trong vùng đã cắt
        text, prob = detector.predict(cropped_img, return_prob=True)

        # Nếu độ tin cậy thấp hoặc văn bản không hợp lệ, gán text = ""
        if prob < 0.5 or text.lower() == "contraction" or text.lower() == "CONTRACTION":
            text = ""

        results.append({
            "coordinates": coords,
            "text": text,
            "confidence": prob
        })

    for result in results:
        print(f"Coordinates: {result['coordinates']}, Text: {result['text']}, Confidence: {result['confidence']}")
    return results
