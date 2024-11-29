# Cách để chạy server : </br>
## B1 : tải các thư viện cần thiết như : vietocr,werkzeug.utils,flask,numpy,..
## B2 : thực hiện chạy file app.py trong thư mục general

- Để gởi yêu cầu api qua server thực hiện gởi qua endpoint : http://127.0.0.1:5000/upload
- Server cho phép gởi nhiều ảnh với key là files và sẽ trả lại api dưới dạng :
```
  {
  "annotated_images": [
  {
  "filename": "cb3d76834e8c4702b3bcc3e9045e6d83.jpg",
  "url": "/uploads/cb3d76834e8c4702b3bcc3e9045e6d83.jpg"
  },
  {
  "filename": "375a01aff4474a18850613aa3ac1d6c3.jpg",
  "url": "/uploads/375a01aff4474a18850613aa3ac1d6c3.jpg"
  },
  {
  "filename": "005d4f1dd1f74e3faf4404d33fab7def.jpg",
  "url": "/uploads/005d4f1dd1f74e3faf4404d33fab7def.jpg"
  }
  ],
  "download_url": "/download/OCR_Results_11f9ce47b43a4a7ab5c8b059c399c92c.xlsx",
  "excel_file": "OCR_Results_11f9ce47b43a4a7ab5c8b059c399c92c.xlsx",
  "message": "Image processing completed.",
  "title_results": [
  [
  {
  "confidence": 0.9325633563778617,
  "coordinates": [
  114,
  80,
  379,
  108
  ],
  "ocr_text": "KHOA KHOA HỌC MÁY TÍNH"
  },
  {
  "confidence": 0.9300756967729993,
  "coordinates": [
  188,
  206,
  481,
  234
  ],
  "ocr_text": "Đồ án chuyên ngành 3 - Hội đồng 7-SE"
  },
  {
  "confidence": 0.9268639418813918,
  "coordinates": [
  42,
  181,
  270,
  210
  ],
  "ocr_text": "Học kỳ 2, Năm học 2023-2024"
  }
  ],
  [],
  []
  ]
  }
```
- Ở đây mình gởi 4 file ảnh nên nó sẽ trả lại api như sau :
```
  {
  "annotated_images": [
  {
  "filename": "4ed6029021694664a1e2b2432dd9bc39.jpg",
  "url": "/uploads/4ed6029021694664a1e2b2432dd9bc39.jpg"
  },
  {
  "filename": "fb341e7eba9e49ff84b805995552a0f5.jpg",
  "url": "/uploads/fb341e7eba9e49ff84b805995552a0f5.jpg"
  },
  {
  "filename": "97e9b418e2ba439599aae0f4dd673ca3.jpg",
  "url": "/uploads/97e9b418e2ba439599aae0f4dd673ca3.jpg"
  },
  {
  "filename": "bf3075c4c1104f3cac1abfb303e2d50a.jpg",
  "url": "/uploads/bf3075c4c1104f3cac1abfb303e2d50a.jpg"
  }
  ],
```
- Ở trường url sẽ cho phép bạn tải ảnh đã qua xử lý table detection với thứ tự chính xác với thứ tự ảnh bạn call api
- "download_url": "/download/OCR_Results_93b58d91874546e3bd92ace7e1a08216.xlsx", đây sẽ là link dowload file excel được xuất ra khi quá trình xử lý thành công
- ở trường title_results sẽ là các label title của bảng điểm.
  Chúc thành công...
