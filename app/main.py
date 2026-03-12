from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def root():
    return {"status": "healthy"}
