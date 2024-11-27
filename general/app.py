from flask import Flask, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from process_ocr import process_image_and_create_excel  # Xử lý OCR và tạo file Excel
from title_detection.api import predict_from_image  # Hàm xử lý từ api.py

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Định nghĩa các cài đặt
UPLOAD_FOLDER = './uploads'
RESULTS_FOLDER = './results_excel'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

# Kiểm tra định dạng tệp
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files selected"}), 400

    results = []
    
    # Lưu và xử lý từng ảnh
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Xử lý bằng process_image_and_create_excel
            try:
                excel_file, random_filename = process_image_and_create_excel(file_path)
                excel_path = os.path.join(app.config['RESULTS_FOLDER'], excel_file)
            except Exception as e:
                excel_file = None
                excel_path = None
                random_filename = None

            # Xử lý bằng predict_from_image
            try:
                with open(file_path, 'rb') as f:
                    image_bytes = f.read()
                prediction_result = predict_from_image(image_bytes)
            except Exception as e:
                prediction_result = {"error": str(e)}

            # Tổng hợp kết quả
            results.append({
                "filename": filename,
                "predictions": prediction_result.get("predictions", []),
                "random_filename": random_filename,  
                "error": prediction_result.get("error", None)
            })

    # Trả về kết quả JSON
    return jsonify({
        "message": "Image processing completed.",
        "results": results
    })

# API để tải xuống file Excel đã tạo
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['RESULTS_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Tạo thư mục nếu chưa có
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    
    # Chạy Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
