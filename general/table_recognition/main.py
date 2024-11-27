import cv2
import numpy as np
from table_recognition.table_recognition import TableRecognizer

# Hàm kiểm tra file có phải là hình ảnh không
def is_image_file(file_path: str):
    valid_extensions = [".png", ".jpeg", ".jpg"]
    return any(file_path.endswith(ext) for ext in valid_extensions)

# Hàm nhận ảnh và trả về tọa độ các ô trong bảng
def process_image(file_path: str, table_list: list = None):
    try:
        # Kiểm tra định dạng tệp
        if not is_image_file(file_path):
            raise ValueError("Do not support this file format")

        # Đọc ảnh từ file
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError("Failed to read image")

        # Khởi tạo đối tượng TableRecognizer
        table_recognizer = TableRecognizer.get_unique_instance()

        # Xử lý ảnh và nhận diện các bảng
        tables = table_recognizer.process(image, table_list=table_list)

        # Tạo danh sách tọa độ các ô của tất cả các bảng
        table_coordinates = []
        for table in tables:
            # Lấy tọa độ của các ô trong bảng
            coordinates = table.get_coordinates()  # Phương thức này sẽ trả về tọa độ các ô

            # Giả sử rằng get_coordinates trả về các tọa độ theo dạng [(x1, y1, x2, y2), ...]
            for coord in coordinates:
                # Chuyển đổi tọa độ sang định dạng yêu cầu [x1, y1, x2, y2]
                table_coordinates.append(list(coord))

        return table_coordinates

    except Exception as e:
        print(f"Error: {e}")
        return None

# Ví dụ gọi hàm
if __name__ == "__main__":
    file_path = "../images/bangdiem5.jpg"  # Đường dẫn đến ảnh cần xử lý
    table_coordinates = process_image(file_path)
    
    if table_coordinates is not None:
        print("Table Coordinates: ", table_coordinates)
    else:
        print("Error processing the image")
