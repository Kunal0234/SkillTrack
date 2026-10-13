
from fastapi import FastAPI

app = FastAPI(title="SkillTrack LMS")


@app.get("/")
def home():
    return {"message": "Welcome to SkillTrack LMS!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
