import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Dashboard Restoran - Bahan Baku Dapur",
    description="Backend API untuk UTS WAD - NIM: 25120300023",
    version="1.0.0"
)

# Aktifkan CORS agar frontend Vue bisa panggil backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Validation Skema Pydantic
class BahanBakuBase(BaseModel):
    nama_bahan: str = Field(..., min_length=2)
    kategori: str = Field(..., min_length=2)
    stok: int = Field(..., ge=0)
    satuan: str = Field(..., min_length=1)

class BahanBakuCreate(BahanBakuBase):
    pass

class BahanBakuUpdate(BaseModel):
    nama_bahan: str | None = None
    kategori: str | None = None
    stok: int | None = Field(None, ge=0)
    satuan: str | None = None

class BahanBaku(BahanBakuBase):
    id: int

@app.get("/api/bahan-baku", response_model=list[BahanBaku])
def get_all_bahan_baku():
    return load_data()

@app.post("/api/bahan-baku", response_model=BahanBaku, status_code=201)
def create_bahan_baku(item: BahanBakuCreate):
    data = load_data()
    new_id = max([x["id"] for x in data], default=0) + 1
    new_item = {
        "id": new_id,
        "nama_bahan": item.nama_bahan,
        "kategori": item.kategori,
        "stok": item.stok,
        "satuan": item.satuan
    }
    data.append(new_item)
    save_data(data)
    return new_item

@app.put("/api/bahan-baku/{item_id}", response_model=BahanBaku)
def update_bahan_baku(item_id: int, item_update: BahanBakuUpdate):
    data = load_data()
    for index, item in enumerate(data):
        if item["id"] == item_id:
            updated_data = item.copy()
            if item_update.nama_bahan is not None:
                updated_data["nama_bahan"] = item_update.nama_bahan
            if item_update.kategori is not None:
                updated_data["kategori"] = item_update.kategori
            if item_update.stok is not None:
                updated_data["stok"] = item_update.stok
            if item_update.satuan is not None:
                updated_data["satuan"] = item_update.satuan
            
            data[index] = updated_data
            save_data(data)
            return updated_data
    raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")

@app.delete("/api/bahan-baku/{item_id}")
def delete_bahan_baku(item_id: int):
    data = load_data()
    new_data = [item for item in data if item["id"] != item_id]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")
    save_data(new_data)
    return {"message": "Bahan baku berhasil dihapus", "id": item_id}