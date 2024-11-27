from PIL import Image, ImageDraw

image_path = "title_detection/test/img_input/_test_2.png"

image = Image.open(image_path)

# Dữ liệu nhãn và tọa độ từ JSON
predictions = [
        {
            "label": "khoa",
            "confidence": 0.9150521755218506,
            "bbox": [
                110.6839370727539,
                81.52554321289062,
                374.21929931640625,
                108.27452087402344
            ]
        },
        {
            "label": "lophocphan",
            "confidence": 0.9150521755218506,
            "bbox": [
                166.55087280273438,
                209.5313262939453,
                291.1209716796875,
                234.06207275390625
            ]
        },
        {
            "label": "kythi",
            "confidence": 0.9150521755218506,
            "bbox": [
                34.42105484008789,
                183.1666259765625,
                246.61619567871094,
                210.39170837402344
            ]
        }
    ]

colors = ["red", "blue", "green"]

draw = ImageDraw.Draw(image)

for i, prediction in enumerate(predictions):
    label = prediction["label"]
    bbox = prediction["bbox"]
    confidence = prediction["confidence"]

    color = colors[i % len(colors)]

    draw.rectangle(bbox, outline=color, width=2)

    text = f"{label} ({confidence:.2f})"
    draw.text((bbox[0], bbox[1] - 10), text, fill=color)


if image.mode == 'RGBA':
    image = image.convert('RGB')

output_path = "title_detection/test/img_output/image_with_boxes.jpg"
image.save(output_path)

image.show()

#run: python title_detection/test/cut_img.py