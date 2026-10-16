# Mini Dashboard Restoran - WAD UTS
- **Nama:** Fajar Muhammad Ramadhan
- **NIM:** 25120300023 (Ganjil - Soal A)

## Ambang Batas (Threshold) Stok
- **Stok Habis:** Stok = 0
- **Menipis:** Stok 1 - 5
- **Aman:** Stok > 5

## Cara Menjalankan

### 1. Jalankan Backend (FastAPI)

## Buka terminal pertama, lalu ketik perintah berikut:
cd C:\Users\welcome\uts_wad05\mini_project_restoran\backend
python -m uvicorn main:app --reload --port 8000

## 2. Jalankan Frontend (Python HTTP Server)

## Buka terminal kedua, lalu ketik perintah berikut:
cd C:\Users\welcome\uts_wad05\mini_project_restoran\frontend
python -m http.server 3000
