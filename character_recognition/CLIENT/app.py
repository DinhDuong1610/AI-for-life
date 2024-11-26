import requests

url = "http://127.0.0.1:5000/ocr/"

image_path = "image/enhanced_for_ocr.jpg"

coordinates = [
    [33,69,202,80],
    [207,72,221,80],
    [225,72,252,81],
    [270,74,288,81]
]
payload = {
    'coordinates[]': [str(coords) for coords in coordinates]
}

with open(image_path, "rb") as img_file:
    files = {"file": img_file}
    response = requests.post(url, files=files, data=payload)

if response.status_code == 200:
    results = response.json()
    for result in results:
        print(f"Coordinates: {result['coordinates']}")
        print(f"Text: {result['text']}")
        print(f"Confidence: {result['confidence']}")
else:
    print("Error:", response.status_code, response.text)
