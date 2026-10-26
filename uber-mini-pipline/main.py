from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import time

app = FastAPI(title="Uber API - Complete")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/uber_db")

# Connexion à la DB avec attente (pour Docker)
engine = None
while engine is None:
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
    except Exception:
        print("⏳ Attente de PostgreSQL...", flush=True)
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# MODÈLES DE BASE DE DONNÉES
# ==========================================

class PassengerDB(Base):
    __tablename__ = "passengers"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    payment_type = Column(String)
    payment_last4 = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class DriverDB(Base):
    __tablename__ = "drivers"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    vehicle_make = Column(String)
    vehicle_model = Column(String)
    license_plate = Column(String)
    capacity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class RideDB(Base):
    __tablename__ = "rides"
    id = Column(String, primary_key=True, index=True)
    passenger_id = Column(String, ForeignKey("passengers.id"))
    driver_id = Column(String, ForeignKey("drivers.id"), nullable=True)
    status = Column(String, default="REQUESTED")
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    dropoff_lat = Column(Float)
    dropoff_lng = Column(Float)
    fare_estimate = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ==========================================
# SCHÉMAS PYDANTIC
# ==========================================

class Location(BaseModel):
    lat: float
    lng: float

class PassengerInput(BaseModel):
    name: str
    email: str
    phone: str
    payment_type: str
    payment_last4: str

class PassengerResponse(PassengerInput):
    id: UUID
    class Config: from_attributes = True

class DriverInput(BaseModel):
    name: str
    email: str
    phone: str
    vehicle_make: str
    vehicle_model: str
    license_plate: str
    capacity: int

class DriverResponse(DriverInput):
    id: UUID
    class Config: from_attributes = True

class RideInput(BaseModel):
    passenger_id: UUID
    driver_id: Optional[UUID] = None
    pickup: Location
    dropoff: Location
    fare_estimate: float

class RideAcceptInput(BaseModel):
    driver_id: UUID

class RideResponse(BaseModel):
    id: UUID
    passenger_id: UUID
    driver_id: Optional[UUID]
    status: str
    fare_estimate: float
    created_at: datetime
    class Config: from_attributes = True

# ==========================================
# ENDPOINTS : PASSAGERS
# ==========================================

@app.post("/passengers", response_model=PassengerResponse, status_code=201)
def create_passenger(passenger: PassengerInput):
    db = SessionLocal()
    new_p = PassengerDB(id=str(uuid4()), **passenger.dict())
    db.add(new_p)
    db.commit()
    db.refresh(new_p)
    db.close()
    return new_p

@app.get("/passengers", response_model=List[PassengerResponse])
def list_passengers():
    db = SessionLocal()
    passengers = db.query(PassengerDB).all()
    db.close()
    return passengers

# ==========================================
# ENDPOINTS : CONDUCTEURS
# ==========================================

@app.post("/drivers", response_model=DriverResponse, status_code=201)
def create_driver(driver: DriverInput):
    db = SessionLocal()
    new_d = DriverDB(id=str(uuid4()), **driver.dict())
    db.add(new_d)
    db.commit()
    db.refresh(new_d)
    db.close()
    return new_d

@app.get("/drivers", response_model=List[DriverResponse])
def list_drivers():
    db = SessionLocal()
    drivers = db.query(DriverDB).all()
    db.close()
    return drivers

# ==========================================
# ENDPOINTS : COURSES (RIDES)
# ==========================================

@app.post("/rides", response_model=RideResponse, status_code=201)
def create_ride(ride: RideInput):
    db = SessionLocal()
    new_ride = RideDB(
        id=str(uuid4()), 
        passenger_id=str(ride.passenger_id),
        driver_id=str(ride.driver_id) if ride.driver_id else None,
        status="ACCEPTED" if ride.driver_id else "REQUESTED",
        pickup_lat=ride.pickup.lat, pickup_lng=ride.pickup.lng,
        dropoff_lat=ride.dropoff.lat, dropoff_lng=ride.dropoff.lng,
        fare_estimate=ride.fare_estimate
    )
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    db.close()
    return new_ride

@app.get("/rides", response_model=List[RideResponse])
def list_rides():
    db = SessionLocal()
    rides = db.query(RideDB).all()
    db.close()
    return rides

@app.post("/rides/{id}/accept", response_model=RideResponse)
def accept_ride(id: str, action: RideAcceptInput):
    db = SessionLocal()
    ride = db.query(RideDB).filter(RideDB.id == id).first()
    if not ride:
        db.close()
        raise HTTPException(status_code=404, detail="Ride not found")
    ride.status = "ACCEPTED"
    ride.driver_id = str(action.driver_id)
    db.commit()
    db.refresh(ride)
    db.close()
    return ride

@app.delete("/rides/{id}")
def delete_ride(id: str):
    db = SessionLocal()
    ride = db.query(RideDB).filter(RideDB.id == id).first()
    if not ride:
        db.close()
        raise HTTPException(status_code=404, detail="Ride not found")
    db.delete(ride)
    db.commit()
    db.close()
    return {"message": "Ride deleted"}

# ==========================================
# ENDPOINTS : MISE À JOUR DU STATUT
# ==========================================

class RideStatusUpdate(BaseModel):
    status: str

@app.patch("/rides/{id}/status", response_model=RideResponse)
def update_ride_status(id: str, action: RideStatusUpdate):
    db = SessionLocal()
    ride = db.query(RideDB).filter(RideDB.id == id).first()
    
    if not ride:
        db.close()
        raise HTTPException(status_code=404, detail="Ride not found")
        
    ride.status = action.status
    db.commit()
    db.refresh(ride)
    db.close()
    return ride