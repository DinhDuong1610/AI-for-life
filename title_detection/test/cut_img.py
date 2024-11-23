from PIL import Image, ImageDraw

# Đường dẫn đến tấm ảnh
image_path = "title_detection/test/img_input/IMG_4010_jpg.rf.40e96249ff486a852f3ea015569d6053.jpg"

# Mở tấm ảnh
image = Image.open(image_path)

# Dữ liệu nhãn và tọa độ từ JSON
predictions = [
    {
        "label": "kythi",
        "confidence": 0.8736988306045532,
        "bbox": [
            420.3743896484375,
            87.3135986328125,
            507.7625732421875,
            97.17733764648438
        ]
    },
    {
        "label": "lophocphan",
        "confidence": 0.8736988306045532,
        "bbox": [
            217.61599731445312,
            108.519775390625,
            424.5296325683594,
            120.78341674804688
        ]
    },
    {
        "label": "khoa",
        "confidence": 0.8736988306045532,
        "bbox": [
            86.76455688476562,
            66.58000183105469,
            317.1660461425781,
            78.45295715332031
        ]
    },
    {
        "label": "mon",
        "confidence": 0.8736988306045532,
        "bbox": [
            256.57391357421875,
            97.83195495605469,
            390.724853515625,
            108.83418273925781
        ]
    }
]

# Tạo danh sách các màu sắc
colors = ["red", "blue", "green", "orange"]

# Tạo đối tượng ImageDraw để vẽ
draw = ImageDraw.Draw(image)

# Vẽ bounding box cho từng nhãn với màu khác nhau
for i, prediction in enumerate(predictions):
    label = prediction["label"]
    bbox = prediction["bbox"]
    confidence = prediction["confidence"]

    # Chọn màu từ danh sách theo thứ tự
    color = colors[i % len(colors)]

    # Vẽ hình chữ nhật
    draw.rectangle(bbox, outline=color, width=2)

    # Thêm nhãn và độ tin cậy lên trên bounding box
    text = f"{label} ({confidence:.2f})"
    draw.text((bbox[0], bbox[1] - 10), text, fill=color)  # Text phía trên bbox

# Lưu ảnh đã chỉnh sửa
output_path = "title_detection/test/img_output/image_with_boxes.jpg"
image.save(output_path)

# Hiển thị ảnh với bounding box và nhãn
image.show()

#run: python title_detection/test/cut_img.py