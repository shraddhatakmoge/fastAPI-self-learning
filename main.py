from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel
import json

app = FastAPI()


class User(BaseModel):
    PatientID:int
    name: str
    age: int
    weight:float


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message":"Patient Information Management API"}

@app.get("/about")
def user():
    return({"message":"It manages patient records digitally !!"})

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/view_patient/{patient_id}")
def view_patient(patient_id : str=Path(...,description="ID of the patient in the DB",example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patiet not found')

@app.get("/sort")
def sort_functions(sort_by:str = Query(...,description="sort on the basis of height , weight or bmi"),order:str=Query('asc',description="sort in ascending or descending order")):
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Invalid field , select from {valid_fields}")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f"select from {['asc','desc']}")
    
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(),key=lambda x :x.get(sort_by,0),reverse=sort_order)

    return sorted_data




@app.get("/patient/{patient_id}/female/{gender_key}")
def get_emp(patient_id:str,gender_key:str):
    data = load_data()
    if patient_id in data.keys() and gender_key in ['female']:
        return data[patient_id]['gender']
    raise HTTPException(status_code=400,detail=f"Enter correct id from {data.keys()}")
