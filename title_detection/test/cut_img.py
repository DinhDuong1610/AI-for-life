from PIL import Image, ImageDraw

image_path = "title_detection/test/img_input/_test_2.png"

image = Image.open(image_path)

# Dữ liệu nhãn và tọa độ từ JSON
predictions = [
        {
            "label": "khoa",
            "confidence": 0.9243448376655579,
            "bbox": [
                109.67903900146484,
                81.0687026977539,
                369.37103271484375,
                108.43220520019531
            ]
        },
        {
            "label": "kythi",
            "confidence": 0.9243448376655579,
            "bbox": [
                34.70358657836914,
                183.4239044189453,
                245.63095092773438,
                209.6919708251953
            ]
        },
        {
            "label": "lophocphan",
            "confidence": 0.9243448376655579,
            "bbox": [
                167.64944458007812,
                209.0294952392578,
                290.1394348144531,
                234.76133728027344
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