from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from sessions import session as session_
import models as models_
from sqlalchemy import DateTime
from datetime import datetime, date
from fastapi import Query

app = FastAPI()

@app.post("/add_student", tags=["student"])
async def add_student(name_srn_: str, gpa_: int, age_: int,
                      entry_year_: int, gender_: str = ""):
    obj = models_.Book(Name_Surname=name_srn_, gpa=gpa_, age=age_,
                       entry_year=entry_year_, gender=gender_)
    session_.add(obj)
    session_.commit()
    return f"Student Added: {obj.id} - {obj.Name_Surname}."

@app.get("/get_student/{student_id}", tags=["student"])
async def get_student(student_id: int):
    student = session_.query(models_.Student).filter(models_.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to get student by ID: Student not found.")
    return student

@app.get("/get_all_students", tags=["student"])
async def get_all_students(skip: int = 0, limit: int = 100):
    students_query = session_.query(models_.Student).offset(skip).limit(limit)
    return students_query.all()

@app.put("/update/{student_id}", tags=["student"])
async def update_studnet(student_id_: int, new_name_srn_: str, new_gpa_: int, new_age_: int, new_entry_year: int, gender_: str = ""):
    if (obj := session_.query(models_.Student).filter(models_.Student.id == student_id_).first()) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to update student: No student with such ID.")
    if new_name_srn_:
        obj.title = new_name_srn_
    if new_gpa_:
        obj.category = new_gpa_
    if new_age_:
        obj.publisher = new_age_
    if new_entry_year:
        obj.author_name = new_entry_year
    if gender_:
        obj.author_surname = gender_
    session_.add(obj)
    session_.commit()
    return f"Successfully updated student with ID:{obj.id}."

@app.delete("/delete/{student_id}", tags=["student"])
async def delete_student(student_id_: int):
    if (obj := session_.query(models_.Student).filter(models_.Student.id == student_id_).first()) is not None:
        session_.delete(obj)
        session_.commit()
        return f"Student deleted: {obj.id} - {obj.Name_Surname}."
