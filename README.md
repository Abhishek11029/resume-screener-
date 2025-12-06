# AI Resume Screener

A full-stack AI-powered application that automatically screens and ranks resumes against job descriptions using semantic similarity, skill matching, and experience analysis.

## 🚀 Features

- **Multi-format Resume Parsing**: Supports PDF, DOCX, and TXT files
- **Intelligent Scoring**: 
  - 40% Skill matching
  - 30% Semantic similarity (using sentence transformers)
  - 20% Experience relevance
  - 10% Education/Projects
- **Detailed Rankings**: Get ranked candidate list with score breakdowns
- **Strengths & Weaknesses**: AI-generated insights for each candidate
- **Beautiful UI**: Modern React frontend with TailwindCSS

## 📁 Project Structure

```
resume-screener/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── utils/
│   │   ├── resume_parser.py    # Resume parsing logic
│   │   └── scoring_engine.py  # Scoring and ranking logic
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── main.jsx            # React entry point
│   │   ├── index.css           # TailwindCSS styles
│   │   ├── api.js              # API client functions
│   │   └── components/
│   │       ├── UploadResumes.jsx
│   │       ├── JobDescriptionInput.jsx
│   │       └── Results.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## 🛠️ Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 📡 API Endpoints

### `POST /upload-resumes`
Upload multiple resume files (PDF, DOCX, TXT)

**Request:** Multipart form data with `files` field

**Response:**
```json
{
  "message": "Successfully uploaded 3 resume(s)",
  "resumes": [
    {
      "resume_id": "uuid",
      "filename": "resume.pdf",
      "status": "parsed"
    }
  ]
}
```

### `POST /job-description`
Submit job description for matching

**Request:**
```json
{
  "description": "Job description text here..."
}
```

**Response:**
```json
{
  "message": "Job description submitted successfully",
  "length": 1234
}
```

### `POST /rank`
Rank all uploaded resumes against the job description

**Response:**
```json
{
  "rankings": [
    {
      "resume_id": "uuid",
      "filename": "resume.pdf",
      "total_score": 85.5,
      "scores": {
        "skill_match": 90.0,
        "semantic_similarity": 82.3,
        "experience_match": 88.0,
        "education_projects": 75.0
      },
      "strengths": ["Strong match in skills: python, react, sql"],
      "weaknesses": ["Missing key skills: docker"],
      "summary": "This candidate has an Excellent match..."
    }
  ]
}
```

### `GET /report/{resume_id}`
Get detailed report for a specific resume

## 🧠 How the Algorithm Works

### 1. **Resume Parsing**
- Extracts text from PDF/DOCX/TXT files
- Identifies skills using keyword matching
- Parses experience, education, and projects sections
- Uses regex patterns to extract structured data

### 2. **Embedding Generation**
- Uses `all-MiniLM-L6-v2` sentence transformer model
- Generates vector embeddings for job description and resume text
- Enables semantic similarity comparison

### 3. **Scoring Calculation**

**Skill Match (40%):**
- Extracts skills from job description
- Compares with skills found in resume
- Calculates match percentage

**Semantic Similarity (30%):**
- Generates embeddings for resume and job description
- Calculates cosine similarity between embeddings
- Measures overall content relevance

**Experience Match (20%):**
- Extracts keywords from job description
- Matches keywords against experience entries
- Calculates relevance score

**Education/Projects (10%):**
- Analyzes education and project sections
- Matches keywords from job description
- Provides additional context score

### 4. **Ranking & Insights**
- Sorts candidates by total score
- Generates strengths based on matches
- Identifies weaknesses (missing skills, etc.)
- Creates AI-generated summary for each candidate

## 🎯 Example Usage

1. **Start Backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Use the Application:**
   - Open `http://localhost:5173` in browser
   - Upload multiple resume files
   - Paste job description
   - Click "Rank Resumes"
   - View ranked results with detailed breakdowns

## 🔧 Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Sentence Transformers**: For semantic embeddings
- **PyPDF2**: PDF parsing
- **docx2txt**: DOCX parsing
- **scikit-learn**: Cosine similarity calculations

### Frontend
- **React**: UI framework
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **Axios**: HTTP client (via fetch API)

## 📝 Notes

- The first run will download the sentence transformer model (~90MB)
- Resume parsing uses regex patterns and may need tuning for different formats
- For production, consider adding database storage instead of in-memory storage
- Add authentication and rate limiting for production use

## 🚀 Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- User authentication
- Resume storage and history
- Export rankings to PDF/Excel
- Advanced NLP for better parsing
- Docker containerization
- Deployment guides

## 📄 License

MIT License - feel free to use and modify as needed!

