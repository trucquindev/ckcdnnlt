from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import os


app = FastAPI(root_path="/api/db")


# Cấu hình kết nối MySQL từ biến môi trường
db_config = {
    'host': os.getenv('MYSQL_HOST', 'mysql'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', '123456'),
    'database': os.getenv('MYSQL_DATABASE', 'fahasaDB')
}


# Hàm kết nối database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None



# Pydantic model
class DoChoi(BaseModel):
    id:str
    ten: str
    giaGoc: int
    giaBan: int
    giamGia: int
    hinh: str
    doTuoiSD: str
    namSX: int
    noiSX: str
    moTa: str
    kichThuoc: str

#GET all đồ chơi
@app.get("/dochoi")
def get_all_dochoi():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DoChoi")
    results = cursor.fetchall()
    conn.close()
    return results

# GET tìm theo tên (gần đúng)
@app.get("/dochoi/search")
def search_dochoi(ten: str = Query(..., description="Tên cần tìm")):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DoChoi WHERE ten LIKE %s", ('%' + ten + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

# DELETE tất cả
@app.delete("/dochoi")
def delete_all_dochoi():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM DoChoi")
    conn.commit()
    conn.close()
    return {"message": "Đã xóa toàn bộ đồ chơi"}

# INSERT tất cả từ JSON
@app.post("/dochoi")
def insert_dochoi(ds_dochoi: List[DoChoi]):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO DoChoi 
    (id,ten, giaGoc, giaBan, giamGia, hinh, doTuoiSD, namSX, noiSX, moTa, kichThuoc)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for dc in ds_dochoi:
        cursor.execute(query, (
            dc.id, dc.ten, dc.giaGoc, dc.giaBan, dc.giamGia,
            dc.hinh, dc.doTuoiSD, dc.namSX, dc.noiSX,
            dc.moTa, dc.kichThuoc
        ))
    conn.commit()
    conn.close()
    return {"message": f"Đã thêm {len(ds_dochoi)} đồ chơi"}

# UPDATE theo id
@app.put("/dochoi/{id}")
def update_dochoi(id: str, dc: DoChoi):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE DoChoi SET
    ten=%s, giaGoc=%s, giaBan=%s, giamGia=%s, hinh=%s,
    doTuoiSD=%s, namSX=%s, noiSX=%s, moTa=%s, kichThuoc=%s
    WHERE id=%s
    """
    cursor.execute(query, (
        dc.ten, dc.giaGoc, dc.giaBan, dc.giamGia, dc.hinh,
        dc.doTuoiSD, dc.namSX, dc.noiSX, dc.moTa, dc.kichThuoc, id
    ))
    conn.commit()
    conn.close()
    return {"message": f"Đã cập nhật đồ chơi có id = {id}"}
