from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from backend.parser import ResumeParser
from backend.jd_parser import JDParser
from backend.temp_upload import TempFileHandler
from backend.chunker import ResumeChunker
from backend.embeddings import EmbeddingService
from backend.vector_store import VectorStore
from backend.rag import RAGPipeline

from backend.ats.skill_extractor import SkillExtractor
from backend.ats.matcher import SkillMatcher
from backend.ats.ats_score import ATSScorer
from backend.ats.report import ATSReport
from backend.ats.ai_recommendation import AIRecommendation


app = FastAPI()
uploaded_resume = ""
uploaded_jd = ""

parser = ResumeParser()
jd_parser = JDParser()
chunker = ResumeChunker()
embedding_service = EmbeddingService()
vector_store = VectorStore()
rag = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Resume Screener API is running"}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    temp_path = TempFileHandler.save_temp_file(file)

    try:
        # Parse Resume
        result = parser.parse(temp_path)
        global uploaded_resume
        uploaded_resume = result["text"]

        # Clear previous resume embeddings
        vector_store.clear()

        # Create Chunks
        chunks = chunker.create_chunks(
            filename=file.filename or "uploaded_resume", 
            document_type="resume",
            text=result["text"]
        )

        # Generate Embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_service.embed_documents(texts)

        # Store in ChromaDB
        vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings
        )

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "total_documents": vector_store.count(),
            "data": result
        }

    finally:
        TempFileHandler.delete_temp_file(temp_path)

# ======================================
# Upload Job Description
# ======================================

@app.post("/upload-jd")
async def upload_job_description(file: UploadFile = File(...)):

    global uploaded_jd

    temp_path = TempFileHandler.save_temp_file(file)

    try:
        result = jd_parser.parse(temp_path)

        uploaded_jd = result["text"]

        return {
            "status": "success",
            "message": "Job Description uploaded successfully.",
            "characters": len(uploaded_jd),
            "data": {
                "text": uploaded_jd
            }
        }
    finally:
        TempFileHandler.delete_temp_file(temp_path)

@app.post("/ask")
def ask_question(request: QuestionRequest):
    return rag.ask(request.question)

@app.post("/ats-score")
def ats_score():

    global uploaded_resume
    global uploaded_jd

    if not uploaded_resume:
        return {
            "status": "error",
            "message": "Please upload a resume first."
        }

    if not uploaded_jd:
        return {
            "status": "error",
            "message": "Please upload a Job Description first."
        }

    # Extract skills
    resume_skills = SkillExtractor.extract(uploaded_resume)
    jd_skills = SkillExtractor.extract(uploaded_jd)

    # Compare skills
    comparison = SkillMatcher.compare(
        resume_skills,
        jd_skills
    )

    # Calculate ATS score
    score = ATSScorer.calculate(comparison)

    # Generate ATS report
    report = ATSReport.generate(
        comparison,
        score
    )

    # AI Recommendation
    try:
       ai = AIRecommendation()
       ai_review = ai.generate(report)

    except Exception as e:
        print(f"AI Recommendation Error: {e}")

        ai_review = {
            "status": "unavailable",
            "message": "AI Review is temporarily unavailable because the Gemini API quota has been exceeded."
        }

    return {
        **report,
        "ai_review": ai_review
    }