from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import random

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to Voiceflow domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
users_db = {}
submitted_shifts = []

# Sample facility names
facility_names = [
    "City Health Center", "River Hospital", "Lakeside Clinic",
    "Metro Medical Hub", "Sunrise Wellness", "Hope Care Point"
]

# Model for POST /submit-shift
class ShiftRequest(BaseModel):
    phone: str
    shift_date: str
    shift_time: str

# GET /get-facility?phone=...
@app.get("/get-facility")
def get_facility(phone: str):
    if phone not in users_db:
        # Generate new facility info
        new_facility_id = f"F{str(uuid4())[:6].upper()}"
        new_facility_name = random.choice(facility_names)
        users_db[phone] = {
            "facility_id": new_facility_id,
            "facility_name": new_facility_name
        }

    return users_db[phone]

# POST /submit-shift
@app.post("/submit-shift")
def submit_shift(data: ShiftRequest):
    if data.phone not in users_db:
        raise HTTPException(status_code=404, detail="Phone number not found. Call /get-facility first.")

    facility_info = users_db[data.phone]
    shift_data = {
        "phone": data.phone,
        "shift_date": data.shift_date,
        "shift_time": data.shift_time,
        "facility_id": facility_info["facility_id"],
        "facility_name": facility_info["facility_name"]
    }

    submitted_shifts.append(shift_data)

    return {
        "status": "success",
        "message": "Shift submitted successfully",
        "data": shift_data
    }
