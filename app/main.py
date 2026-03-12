from fastapi import FastAPI
from app.models import Base
from app.models import Job
from app.database import engine
from app.database import SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)

#Get Requests
@app.get("/")
def check_run():
    return {"message": "API is running"}

@app.get("/health")
def health_status():
    return {"status": "healthy"}

@app.get("/jobs")
def return_all_jobs():
    db = SessionLocal()
    all_jobs = db.query(Job).all()
    return all_jobs


@app.get("/jobs/{job_id}")
def return_jobs_by_id(job_id: int):
    db = SessionLocal()
    jobs = db.query(Job).filter(Job.id == job_id).first()
    return jobs
    

#Post Requests
@app.post("/jobs")
def create_job(document_url: str):
    db = SessionLocal()

    job = Job(
        document_url = document_url,
        status = "pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job