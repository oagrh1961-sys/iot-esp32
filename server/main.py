from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
import os

DATABASE_URL = "sqlite:///./iot_datos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

CSV_FILE = "iot_datos.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "temperatura", "humedad", "dispositivo", "timestamp"])

class DatoSensor(Base):
    __tablename__ = "datos"
    id          = Column(Integer, primary_key=True, index=True)
    temperatura = Column(Float)
    humedad     = Column(Float)
    dispositivo = Column(String)
    timestamp   = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class SensorData(BaseModel):
    temperatura: float
    humedad: float
    dispositivo: str = "ESP32"

@app.get("/")
def root():
    return {"status": "Servidor IoT activo", "hora": str(datetime.now())}

@app.get("/dashboard")
def dashboard():
    return FileResponse("templates/index.html")

@app.post("/datos")
def recibir_datos(data: SensorData):
    db = SessionLocal()
    registro = DatoSensor(
        temperatura = data.temperatura,
        humedad     = data.humedad,
        dispositivo = data.dispositivo
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([registro.id, registro.temperatura, registro.humedad, registro.dispositivo, str(registro.timestamp)])
    db.close()
    return {"mensaje": "Dato guardado en DB y CSV", "id": registro.id}

@app.get("/datos")
def ver_datos():
    db = SessionLocal()
    datos = db.query(DatoSensor).all()
    db.close()
    return {
        "total": len(datos),
        "datos": [{"id": d.id, "temperatura": d.temperatura, "humedad": d.humedad, "dispositivo": d.dispositivo, "timestamp": str(d.timestamp)} for d in datos]
    }

@app.get("/datos/ultimo")
def ultimo_dato():
    db = SessionLocal()
    dato = db.query(DatoSensor).order_by(DatoSensor.id.desc()).first()
    db.close()
    if dato is None:
        return {"mensaje": "No hay datos aún"}
    return {"id": dato.id, "temperatura": dato.temperatura, "humedad": dato.humedad, "dispositivo": dato.dispositivo, "timestamp": str(dato.timestamp)}

@app.get("/csv")
def ver_csv():
    datos = []
    with open(CSV_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            datos.append(row)
    return {"total": len(datos), "datos": datos}
