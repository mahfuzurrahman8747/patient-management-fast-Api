from fastapi import FastAPI , Path , HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal,Optional
import json

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(...,description="The unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(...,description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(...,description="The city where the patient resides", example="New York")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal["Male", "Female"], Field(...,description="The gender of the patient", example="Male")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in meters", example=1.75)]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms", example=70.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def health_status(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None, description="The name of the patient", example="John Doe")]
    city: Annotated[Optional[str], Field(default=None, description="The city where the patient resides", example="New York")]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Optional[Literal["Male", "Female"]], Field(default=None, description="The gender of the patient", example="Male")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="The height of the patient in meters", example=1.75)]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="The weight of the patient in kilograms", example=70.5)]


def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {"message": "Patient Management system api is running successfully!"}

@app.get("/about")
def about():
    return {"message": "A full functional API to manage your patient records."}


@app.get("/views")
def views():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patient(sort_by: str = Query(...,description='Sort on the basic on height, weight or bmi '),
                  order: str = Query('asc',description='Sort in asc or desc order')):

    value_field = ['height','weight','bmi']

    if sort_by not in value_field:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {value_field}')
    
    if order not in ['asc','desc']:
        return HTTPException(status_code=400,detail=f'In valid order select between asc or desc')
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0),reverse=sort_order)

    return sorted_data

@app.post("/patient")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump(exclude=['id'])

    with open('patient.json', 'w') as f:
        json.dump(data, f, indent=4)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient = data[patient_id]

    updated_patient = patient_update.model_dump(exclude_unset=True)

    existing_patient.update(updated_patient)

    existing_patient['bmi'] = round(existing_patient['weight'] / (existing_patient['height'] ** 2), 2)

    existing_patient['health_status'] = (
        "Underweight" if existing_patient['bmi'] < 18.5 else
        "Normal weight" if 18.5 <= existing_patient['bmi'] < 25 else
        "Overweight" if 25 <= existing_patient['bmi'] < 30 else
        "Obese"
    )

    data[patient_id] = existing_patient

    with open('patient.json', 'w') as f:
        json.dump(data, f, indent=4)

    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]

    with open('patient.json', 'w') as f:
        json.dump(data, f, indent=4)

    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)