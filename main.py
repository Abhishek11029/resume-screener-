from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import uuid
from models.schemas import JobDescription, RankingResponse, ResumeReport
from utils.resume_parser import ResumeParser
from utils.scoring_engine import ScoringEngine

app = FastAPI(title="AI Resume Screener API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
resumes_storage = {}
job_description_storage = {}

# Initialize parser and scoring engine
resume_parser = ResumeParser()
scoring_engine = ScoringEngine()


@app.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Upload multiple resume files (PDF, DOCX, TXT)
    """
    uploaded_resumes = []
    
    for file in files:
        # Validate file type
        if not file.filename:
            continue
            
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.pdf', '.docx', '.doc', '.txt']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported: PDF, DOCX, DOC, TXT"
            )
        
        # Generate unique ID for resume
        resume_id = str(uuid.uuid4())
        
        # Save file temporarily
        file_path = f"temp_{resume_id}{file_ext}"
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Parse resume
            parsed_data = resume_parser.parse(file_path)
            parsed_data['filename'] = file.filename
            parsed_data['resume_id'] = resume_id
            
            # Store parsed data
            resumes_storage[resume_id] = parsed_data
            
            uploaded_resumes.append({
                'resume_id': resume_id,
                'filename': file.filename,
                'status': 'parsed'
            })
            
            # Clean up temp file
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            # Clean up on error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=500,
                detail=f"Error processing {file.filename}: {str(e)}"
            )
    
    return {
        'message': f'Successfully uploaded {len(uploaded_resumes)} resume(s)',
        'resumes': uploaded_resumes
    }


@app.post("/job-description")
async def submit_job_description(job_desc: JobDescription):
    """
    Submit job description for matching
    """
    if not job_desc.description or not job_desc.description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
    
    job_description_storage['description'] = job_desc.description
    job_description_storage['embedding'] = scoring_engine.generate_embedding(job_desc.description)
    
    return {
        'message': 'Job description submitted successfully',
        'length': len(job_desc.description)
    }


@app.post("/rank", response_model=RankingResponse)
async def rank_resumes():
    """
    Rank all uploaded resumes against the job description
    """
    if not resumes_storage:
        raise HTTPException(status_code=400, detail="No resumes uploaded")
    
    if 'description' not in job_description_storage:
        raise HTTPException(status_code=400, detail="Job description not submitted")
    
    # Get job description and embedding
    job_description = job_description_storage['description']
    job_embedding = job_description_storage['embedding']
    
    # Score each resume
    rankings = []
    for resume_id, resume_data in resumes_storage.items():
        scores = scoring_engine.calculate_scores(
            resume_data,
            job_description,
            job_embedding
        )
        
        # Generate strengths and weaknesses
        strengths = scoring_engine.get_strengths(resume_data, job_description)
        weaknesses = scoring_engine.get_weaknesses(resume_data, job_description)
        
        # Generate summary
        summary = scoring_engine.generate_summary(resume_data, scores)
        
        rankings.append({
            'resume_id': resume_id,
            'filename': resume_data.get('filename', 'Unknown'),
            'total_score': scores['total_score'],
            'scores': {
                'skill_match': scores['skill_match'],
                'semantic_similarity': scores['semantic_similarity'],
                'experience_match': scores['experience_match'],
                'education_projects': scores['education_projects']
            },
            'strengths': strengths,
            'weaknesses': weaknesses,
            'summary': summary
        })
    
    # Sort by total score (descending)
    rankings.sort(key=lambda x: x['total_score'], reverse=True)
    
    return RankingResponse(rankings=rankings)


@app.get("/report/{resume_id}", response_model=ResumeReport)
async def get_report(resume_id: str):
    """
    Get detailed report for a specific resume
    """
    if resume_id not in resumes_storage:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_data = resumes_storage[resume_id]
    
    if 'description' not in job_description_storage:
        raise HTTPException(status_code=400, detail="Job description not submitted")
    
    job_description = job_description_storage['description']
    job_embedding = job_description_storage['embedding']
    
    scores = scoring_engine.calculate_scores(
        resume_data,
        job_description,
        job_embedding
    )
    
    strengths = scoring_engine.get_strengths(resume_data, job_description)
    weaknesses = scoring_engine.get_weaknesses(resume_data, job_description)
    summary = scoring_engine.generate_summary(resume_data, scores)
    
    return ResumeReport(
        resume_id=resume_id,
        filename=resume_data.get('filename', 'Unknown'),
        parsed_data=resume_data,
        scores=scores,
        strengths=strengths,
        weaknesses=weaknesses,
        summary=summary
    )


@app.get("/")
async def root():
    return {
        "message": "AI Resume Screener API",
        "version": "1.0.0",
        "endpoints": {
            "upload_resumes": "POST /upload-resumes",
            "job_description": "POST /job-description",
            "rank": "POST /rank",
            "report": "GET /report/{resume_id}"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

