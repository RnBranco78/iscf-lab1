from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modelo de dados
class SensorData(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    temp: Optional[float] = None
    timestamp: float

# Armazena os dados recebidos
data_store: List[SensorData] = []

@app.get("/")
def read_root():
    return {"message": "API de coleta de dados do CoppeliaSim"}

@app.post("/data/")
def receive_data(data: SensorData):
    """Recebe dados do sensor e os armazena."""
    data_store.append(data)
    print(f"📌 Dados armazenados: {data_store}")  # <-- Adicionado para debug
    return {"message": "Dados recebidos", "data": data}

@app.get("/data/")
def get_all_data():
    """Retorna todos os dados coletados."""
    return data_store

@app.get("/data/latest/")
def get_latest_data():
    """Retorna o último dado registrado."""
    if data_store:
        return data_store[-1]
    return {"message": "Nenhum dado registrado ainda"}
