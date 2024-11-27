from flask import Flask, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from process_ocr import process_multiple_images_to_excel  
from title_detection.api import predict_from_image  

app = Flask(__name__)

# Định nghĩa các cài đặt
UPLOAD_FOLDER = './image_color'
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

    file_paths = []
    # Không cần prediction_results nữa vì không trả về dự đoán

    # Lưu từng file ảnh và xử lý
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_paths.append(file_path)

    # Gộp tất cả ảnh vào một file Excel duy nhất
    try:
        # Không lưu ảnh vào thư mục nữa, tránh việc lưu ảnh thêm lần nữa
        excel_file, random_filename, out_paths, title_results = process_multiple_images_to_excel(file_paths)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Trả về kết quả JSON
    return jsonify({
        "message": "Image processing completed.",
        "excel_file": random_filename,
        "annotated_images": [{"filename": os.path.basename(out_path), "url": f"/uploads/{os.path.basename(out_path)}"} for out_path in out_paths],
        "download_url": f"/download/{random_filename}",
        "title_results": title_results  # Thêm title_results vào phản hồi
    })



@app.route('/uploads/<filename>', methods=['GET'])
def serve_uploaded_file(filename):
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404

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
