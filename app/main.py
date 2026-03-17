from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session 
from typing import List
from app.models import Base, Job
from app.database import engine, SessionLocal
from app.schemas import JobCreate, JobResponse, JobUpdate, JobStatus


app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Get Requests
@app.get("/")
def check_run():
    return {"message": "API is running"}

@app.get("/health")
def health_status():
    return {"status": "healthy"}

@app.get("/jobs", response_model=List[JobResponse])
def get_all_jobs(
    status: JobStatus | None = None,
    db: Session = Depends(get_db)
    ):
        if status is not None:
            jobs = db.query(Job).filter(Job.status == status).all()
            return jobs
        
        all_jobs = db.query(Job).all()
        return all_jobs


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job
    

#Post Requests
@app.post("/jobs", response_model=JobResponse)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    
    job = Job(
        document_url = job_data.document_url,
        status = JobStatus.pending
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job

#Patches
@app.patch("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_data: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    
    job.status = job_data.status
    
    db.commit()
    db.refresh(job)
    
    return job

#Delete 
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job Deleted Successfully"}