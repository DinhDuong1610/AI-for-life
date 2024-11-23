from PIL import Image, ImageDraw

# Đường dẫn đến tấm ảnh
image_path = "title_detection/test/img_input/IMG_4010_jpg.rf.40e96249ff486a852f3ea015569d6053.jpg"

# Mở tấm ảnh
image = Image.open(image_path)

# Dữ liệu nhãn và tọa độ từ JSON
predictions = [
        {
            "label": "lophocphan",
            "confidence": 0.8814340829849243,
            "bbox": [
                221.84268188476562,
                109.16252136230469,
                427.4497985839844,
                120.34019470214844
            ]
        },
        {
            "label": "khoa",
            "confidence": 0.8814340829849243,
            "bbox": [
                89.54107666015625,
                66.64794921875,
                316.498046875,
                78.38552856445312
            ]
        },
        {
            "label": "kythi",
            "confidence": 0.8814340829849243,
            "bbox": [
                421.32763671875,
                87.78986358642578,
                508.921142578125,
                96.57080841064453
            ]
        },
        {
            "label": "mon",
            "confidence": 0.8814340829849243,
            "bbox": [
                256.84686279296875,
                98.76914978027344,
                391.34808349609375,
                109.21495056152344
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