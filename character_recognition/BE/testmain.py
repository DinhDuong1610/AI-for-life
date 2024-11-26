from flask import Flask, request, jsonify
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import torch
from io import BytesIO
import numpy as np
import re
from imageprocessing import enhance_text_image

app = Flask(__name__)

# Load config OCR
config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
config['weights'] = './config/transformerocr_last.pth'
detector = Predictor(config)


import re

def sanitize_number(text):
    allowed_characters = r'[^0-9\.\,\:\;\-]' 
    cleaned_text = re.sub(allowed_characters, '', text)

    replacements = {
        ':': '.',
        ';': '.',
        ',': '.',
        '-': '.',
        'h': '.',
    }
    for old, new in replacements.items():
        cleaned_text = cleaned_text.replace(old, new)

    parts = cleaned_text.split('.')
    if len(parts) > 2:
        cleaned_text = f"{parts[0]}.{''.join(parts[1:])}"

    try:
        result = float(cleaned_text)
        if result.is_integer():
            return int(result)  
        return result
    except ValueError:
        return text


@app.route("/ocr/", methods=["POST"])
def ocr():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        img = Image.open(BytesIO(file.read())).convert("RGB")
        enhanced_img = enhance_text_image(np.array(img))
        enhanced_img_pil = Image.fromarray(enhanced_img)
    except Exception as e:
        return jsonify({"error": f"Invalid image file: {str(e)}"}), 400

    try:
        coords_list = request.form.getlist('coordinates[]')
        if not coords_list:
            return jsonify({"error": "No coordinates provided"}), 400

        result = []
        for coords_str in coords_list:
            coords_str = coords_str.strip('[]')
            coords = list(map(int, coords_str.split(',')))

            if len(coords) != 4:
                return jsonify({"error": f"Invalid coordinates format: {coords_str}"}), 400

            min_x, min_y, max_x, max_y = coords

            cropped_img = enhanced_img_pil.crop((min_x, min_y, max_x, max_y))

            text, prob = detector.predict(cropped_img, return_prob=True)

            processed_text = sanitize_number(text)

            result.append({
                "coordinates": coords,
                "text": processed_text,
                "confidence": prob
            })
    except Exception as e:
        return jsonify({"error": f"Error processing coordinates: {str(e)}"}), 400

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
