from flask import Flask, request, jsonify
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import torch
from io import BytesIO

app = Flask(__name__)

config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'

detector = Predictor(config)

@app.route("/ocr/", methods=["POST"])
def ocr():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        img = Image.open(BytesIO(file.read()))
        img = img.convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Invalid image file: {str(e)}"}), 400

    try:
        coords_list = request.form.getlist('coordinates[]')
        if not coords_list:
            return jsonify({"error": "No coordinates provided"}), 400

        result = []
        for coords_str in coords_list:
            coords_str = coords_str.strip()
            coords_str = coords_str.strip('[]')

            coords = list(map(int, coords_str.split(',')))

            if len(coords) != 4:
                return jsonify({"error": f"Invalid coordinates format: {coords_str}"}), 400

            min_x, min_y = coords[0], coords[1]
            max_x, max_y = coords[2], coords[3]

            cropped_img = img.crop((min_x, min_y, max_x, max_y))

            text, prob = detector.predict(cropped_img, return_prob=True)

            result.append({
                "coordinates": coords,
                "text": text,
                "confidence": prob
            })
    except Exception as e:
        return jsonify({"error": f"Error processing coordinates: {str(e)}"}), 400

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
