from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class JobStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class JobCreate(BaseModel):
    document_url: str

class JobResponse(BaseModel):
    id: int
    document_url: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class JobUpdate(BaseModel):
    status: JobStatus 