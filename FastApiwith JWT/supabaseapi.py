from operator import ge, le
import os
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()
from fastapi import FastAPI

app = FastAPI()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
client = create_client(SUPABASE_URL, SUPABASE_KEY)



@app.get("/students")
def get_students():
    response = client.table("students").select("*").execute()
    return response.data

@app.get("/students/{student_id}")
def get_students_by_id(student_id: int):
    response = client.table("students").select("*").eq("id", student_id).execute()
    return response.data


@app.get("/students/age/{age}")
def filter_by_age(age: int):
    response = client.table("students").select("*").eq("age", age).execute()
    return response.data

from pydantic import BaseModel ,Field , EmailStr

class Student(BaseModel):
    name: str = Field(ge=5 , le=100)
    email : EmailStr
    age: int = Field(ge=18 , le=100)
    course: str


@app.post("/students/insert")
def insert_student(student: Student):
    response = client.table("students").insert(student.dict()).execute()
    return response.data


class studentupdate(BaseModel):
    name: str = Field(min_length=5 , max_length=100)
    email : EmailStr
    age: int = Field(ge=18 , le=100)
    course: str


@app.put("/students/update/{student_id}")
def update_student(student_id: int, student: studentupdate):
    response = client.table("students").update(student.dict()).eq("id", student_id).execute()
    return response.data


class studetnpatch(BaseModel):
    name: str | None = Field(default=None, min_length=5 , max_length=100)
    email : EmailStr | None = Field(default=None)
    age: int | None = Field(default=None, ge=18 , le=100)
    course: str | None = Field(default=None)



@app.patch("/students/patch/{student_id}")
def student_patch(student_id: int, student: studetnpatch):
    response = client.table("students").update(student.dict(exclude_unset=True)).eq("id", student_id).execute()
    return response.data



@app.delete("/students/delete/{student_id}")
def delete_student(student_id: int):
    response = client.table("students").delete().eq("id", student_id).execute()
    return response.data


from slowapi import Limiter
from fastapi import Request
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


@app.get("/studentslimit/xyz")
@limiter.limit("5/minute")
def limit_student_update(request:Request):
    response = client.table("students").select("*").execute()
    return response.data


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5004", "http://127.0.0.1:5004"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test-cors")
@limiter.limit("5/minute")
def test_cors():
    return {"message": "CORS is working"}

