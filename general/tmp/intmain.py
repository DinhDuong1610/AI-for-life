from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import cv2
import numpy as np
import torch
from character_recognition.imageprocessing import enhance_text_image

# Load config OCR
config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'

detector = Predictor(config)

def process_image_with_coordinates(image_path, coordinates_list):
    try:
        # Đọc ảnh từ file
        img = Image.open(image_path).convert("RGB")
        original_img = np.array(img)  # Ảnh gốc để vẽ
        enhanced_img = enhance_text_image(original_img)
        enhanced_img_pil = Image.fromarray(enhanced_img)
    except Exception as e:
        print(f"Error loading or processing the image: {str(e)}")
        return [], None

    results = []  # Danh sách kết quả nhận diện

    # Tạo bản sao của ảnh để tô màu
    annotated_img = original_img.copy()

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
        if prob < 0.5 or text.lower() == "contraction":
            text = ""

        # Lưu kết quả OCR
        results.append({
            "coordinates": coords,
            "text": text,
            "confidence": prob
        })

        # Tô màu vùng trên ảnh nếu text nhận diện được
        color = (0, 0, 255) if prob < 0.5 else (0, 255, 0)  # Màu đỏ nếu tin cậy thấp, màu xanh nếu cao
        cv2.rectangle(annotated_img, (min_x, min_y), (max_x, max_y), color, 2)  # Viền hình chữ nhật
        cv2.putText(annotated_img, text, (min_x, min_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    # Ghi ảnh kết quả
    output_path = "annotated_image.jpg"
    cv2.imwrite(output_path, cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))

    return results, output_path
