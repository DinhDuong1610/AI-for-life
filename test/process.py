import easyocr

# Khởi tạo trình đọc
reader = easyocr.Reader(['en'], gpu=False)  # Thêm mã ngôn ngữ bạn cần (vd: 'vi' cho tiếng Việt)

# Đọc chữ từ ảnh
results = reader.readtext('./image/chu.png')

# Hiển thị kết quả
for bbox, text, prob in results:
    print(f"Detected text: {text} (Confidence: {prob})")
