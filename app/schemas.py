from pydantic import BaseModel, ConfigDict

class JobCreate(BaseModel):
    document_url: str

class JobResponse(BaseModel):
    id: int
    document_url: str
    status: str

    model_config = ConfigDict(from_attributes=True)
    
class JobUpdate(BaseModel):
    status: str    