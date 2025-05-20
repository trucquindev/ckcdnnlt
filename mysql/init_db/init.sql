CREATE DATABASE fahasaDB;
USE fahasaDB;
CREATE TABLE DoChoi (
    id VARCHAR(6) PRIMARY KEY ,
    ten TEXT,
    giaGoc INT,
    giaBan INT,
    giamGia INT,
    hinh TEXT,
    doTuoiSD VARCHAR(300),
    namSX INT,
    noiSX VARCHAR(200),
    moTa TEXT,
    kichThuoc VARCHAR(300)
);

INSERT INTO DoChoi 
(id, ten, giaGoc, giaBan, giamGia, hinh, doTuoiSD, namSX, noiSX, moTa, kichThuoc) 
VALUES 
('100001','Xe ô tô đồ chơi điều khiển', 250000, 199000, 20, 'oto_dieu_khien.jpg', '3+', 2023, 'Việt Nam', 'Ô tô điều khiển từ xa cho trẻ em, màu sắc bắt mắt.', '30x15x10cm'),
('100002','Bộ xếp hình Lego siêu anh hùng', 500000, 450000, 10, 'lego_sieu_anh_hung.jpg', '6+', 2024, 'Đan Mạch', 'Bộ đồ chơi xếp hình giúp phát triển tư duy logic.', '25x20x5cm');


