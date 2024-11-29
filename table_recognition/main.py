from http import HTTPStatus

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from table_detection.table_recognition import TableRecognizer, Table, Cell  # Import your TableRecognizer class


app = FastAPI()


@app.get("/health/live", response_model=None)
def get_health_live() -> bool:
    return True


def is_image_file(file: UploadFile = File(...)):
    """
    Check if the uploaded file is a valid image type (PNG, JPEG, JPG).
    """
    return file.content_type in ["image/png", "image/jpeg", "image/jpg"]

def add_borders_to_table(image: np.ndarray, table: Table) -> np.ndarray:
    """
    Vẽ 4 đường kẻ cho bảng theo tọa độ của bảng (xmin, xmax, ymin, ymax).
    """
    # Vẽ cạnh trái (dọc)
    cv2.line(image, (table.xmin, table.ymin), (table.xmin, table.ymax), (0, 0, 0), 2)

    # Vẽ cạnh phải (dọc)
    cv2.line(image, (table.xmax, table.ymin), (table.xmax, table.ymax), (0, 0, 0), 2)

    # Vẽ cạnh trên (ngang)
    cv2.line(image, (table.xmin, table.ymin), (table.xmax, table.ymin), (0, 0, 0), 2)

    # Vẽ cạnh dưới (ngang)
    cv2.line(image, (table.xmin, table.ymax), (table.xmax, table.ymax), (0, 0, 0), 2)

    return image

# Pydantic model for API response format
class TableResponse(BaseModel):
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    cells: list[dict]  # Each cell will be a dictionary with its bounding box (xmin, xmax, ymin, ymax)

    class Config:
        orm_mode = True


@app.post("/table_recognition", response_model=list[TableResponse])
async def process(file: UploadFile = File(...)):
    try:
        image = None

        # Kiểm tra nếu file là ảnh
        if is_image_file(file):
            image = await file.read()
            image = np.frombuffer(image, np.uint8)  # Dùng frombuffer thay vì fromstring
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            await file.close()
        else:
            raise HTTPException(
                status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value,
                detail="Do not support this file format",
            )
        
        assert image is not None

        # Khởi tạo TableRecognizer
        table_recognizer: TableRecognizer = TableRecognizer.get_unique_instance()

        # Xử lý để nhận diện bảng và ô trong bảng
        tables: list[Table] = table_recognizer.process(image, table_list=None)

        # Chỉnh sửa ảnh nếu bảng bị thiếu cạnh
        for table in tables:
            image = add_borders_to_table(image, table)

        # Tiến hành nhận diện lại sau khi sửa ảnh
        tables: list[Table] = table_recognizer.process(image, table_list=None)

        # Chuẩn bị dữ liệu trả về
        response = []
        for table in tables:
            table_dict = {
                "xmin": table.xmin,
                "xmax": table.xmax,
                "ymin": table.ymin,
                "ymax": table.ymax,
                "cells": []
            }
            for cell in table.cells:
                table_dict["cells"].append({
                    "xmin": cell.xmin,
                    "xmax": cell.xmax,
                    "ymin": cell.ymin,
                    "ymax": cell.ymax
                })
            response.append(table_dict)

        return response

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(e)
        )