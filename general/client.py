import requests

# Địa chỉ API Flask
url = 'http://localhost:5000/upload'

# Đường dẫn tới các ảnh cần gửi
files = [
    ('files', open('./images/bangdiem5.jpg', 'rb')),
    ('files', open('./images/bangcuadinh.jpg', 'rb')),
    ('files', open('./images/ketthuchocphan.png', 'rb'))
]

# Gửi yêu cầu POST với các tệp ảnh
response = requests.post(url, files=files)

# Đóng tệp ảnh sau khi gửi
for _, file in files:
    file.close()

# In kết quả từ server
if response.status_code == 200:
    print("Tệp đã được gửi thành công!")
    print("Kết quả trả về:", response.json())
else:
    print(f"Lỗi khi gửi yêu cầu: {response.status_code}")
    print(response.text)
