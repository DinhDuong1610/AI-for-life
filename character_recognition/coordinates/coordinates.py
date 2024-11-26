from pytesseract import pytesseract, Output
from PIL import Image

# Đường dẫn tới ảnh
image_path = "./test4.png"

# Cấu hình đường dẫn tới Tesseract nếu cần (thay đổi tùy theo hệ thống)
# pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Mở ảnh
img = Image.open(image_path)

# Sử dụng Tesseract để lấy dữ liệu kèm tọa độ
data = pytesseract.image_to_data(img, lang='vie', output_type=Output.DICT)

# Tìm từ "phím"
found = False
for i, word in enumerate(data['text']):
    if word.lower() == "phím":  # So khớp từ
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        print(f"Từ 'phím' được tìm thấy tại tọa độ: ({x}, {y}), kích thước: ({w}x{h})")
        found = True
        break

if not found:
    print("Không tìm thấy từ 'phím' trong ảnh.")
