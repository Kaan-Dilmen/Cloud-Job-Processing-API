from fastapi import FastAPI
from typing import List
from app.models import Base, Job
from app.database import engine, SessionLocal
from app.schemas import JobCreate, JobResponse


app = FastAPI()

Base.metadata.create_all(bind=engine)

#Get Requests
@app.get("/")
def check_run():
    return {"message": "API is running"}

@app.get("/health")
def health_status():
    return {"status": "healthy"}

@app.get("/jobs", response_model=List[JobResponse])
def return_all_jobs():
    db = SessionLocal()
    all_jobs = db.query(Job).all()
    return all_jobs


@app.get("/jobs/{job_id}", response_model=JobResponse)
def return_jobs_by_id(job_id: int):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    return job
    

#Post Requests
@app.post("/jobs", response_model=JobResponse)
def create_job(job_data: JobCreate):
    db = SessionLocal()

    job = Job(
        document_url = job_data.document_url,
        status = "pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job