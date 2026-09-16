import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import FastAPI

DATABASE_URL = 'postgresql://neondb_owner:npg_L7o9JqiSyPNp@ep-tiny-violet-aes869xt-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


@app.get("/students")
def get_students():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM students"))
        students = result.fetchall()
        print(students)
        return [dict(row._mapping) for row in students]
    finally:
        session.close()
        
        
        
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM students WHERE id = :id"), {"id": student_id})
        student = result.fetchone()
        print(student)
        return dict(student._mapping) if student else None
    finally:
        session.close()
        
        
        
from pydantic import BaseModel, EmailStr, EmailStr

class Studentcreate(BaseModel):

    name: str
    email: EmailStr
    age:int | None = None
    city: str | None = None
    
    
    
@app.post("/students_create")
def create_student(student: Studentcreate):
    session = SessionLocal()
    try:
        session.execute(
            text("INSERT INTO students (name, email, age, city) VALUES (:name, :email, :age, :city)"),
            {"name": student.name, "email": student.email, "age": student.age, "city": student.city}
        )
        session.commit()
        return {"message": "Student created successfully"}
    finally:
        session.close()


@app.patch("/students/{student_id}/city")
def update_city(student_id: int, new_city: str):
    session = SessionLocal()
    try:
        session.execute(
            text("UPDATE students SET city = :city WHERE id = :id"),
            {"city": new_city, "id": student_id}
        )
        session.commit()
        return {"message": "City updated successfully"}
    finally:
        session.close()



@app.get("/course_revenue")
def course_revenue():

    session = SessionLocal()

    query = """
    SELECT
        c.id,
        c.title,
        c.price,
        COUNT(e.id) AS total_students,
        c.price * COUNT(e.id) AS revenue
    FROM courses c
    LEFT JOIN enrollments e
        ON c.id = e.course_id
    WHERE e.status = 'active'
    GROUP BY
        c.id,
        c.title,
        c.price
    ORDER BY revenue DESC;
    """

    result = session.execute(text(query))
    rows = result.fetchall()
    session.close()

    result = []

    for row in rows:
        result.append({
            "course_id": row[0],
            "course_name": row[1],
            "price": float(row[2]),
            "total_students": row[3],
            "revenue": float(row[4])
        })

    return result