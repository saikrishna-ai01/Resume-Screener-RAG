from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from backend.jd_parser import JobDescriptionParser
from backend.jd_analyzer import JobDescriptionAnalyzer

app = FastAPI(
    title="Resume Screener API",
    version="1.0.0",
    description="AI Resume Screener using RAG"
)

# Create instances
jd_parser = JobDescriptionParser()
jd_analyzer = JobDescriptionAnalyzer()


@app.get("/")
def root():
    return {
        "message": "Resume Screener API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/upload-job-description")
async def upload_job_description(
    file: UploadFile = File(...)
):
    upload_dir = Path("data/job_descriptions")
    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not file.filename:
     return {"error": "No filename provided"}

    destination = upload_dir / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    text = jd_parser.parse(str(destination))

    return jd_analyzer.analyze(text)