import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List
import re


class ScoringEngine:
    """
    Scoring engine that calculates resume scores based on:
    - Skill matching (40%)
    - Semantic similarity (30%)
    - Experience relevance (20%)
    - Education/Projects (10%)
    """
    
    def __init__(self):
        # Load sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Loaded sentence transformer model")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        return self.model.encode(text, convert_to_numpy=True)
    
    def calculate_scores(self, resume_data: Dict, job_description: str, job_embedding: np.ndarray) -> Dict:
        """
        Calculate all scores for a resume
        """
        # 1. Skill Match (40%)
        skill_score = self._calculate_skill_match(resume_data, job_description)
        
        # 2. Semantic Similarity (30%)
        semantic_score = self._calculate_semantic_similarity(resume_data, job_embedding)
        
        # 3. Experience Match (20%)
        experience_score = self._calculate_experience_match(resume_data, job_description)
        
        # 4. Education/Projects (10%)
        education_score = self._calculate_education_projects_score(resume_data, job_description)
        
        # Calculate weighted total score
        total_score = (
            skill_score * 0.40 +
            semantic_score * 0.30 +
            experience_score * 0.20 +
            education_score * 0.10
        )
        
        return {
            'skill_match': round(skill_score, 2),
            'semantic_similarity': round(semantic_score, 2),
            'experience_match': round(experience_score, 2),
            'education_projects': round(education_score, 2),
            'total_score': round(total_score, 2)
        }
    
    def _calculate_skill_match(self, resume_data: Dict, job_description: str) -> float:
        """Calculate skill matching score (0-100)"""
        resume_skills = set([s.lower() for s in resume_data.get('skills', [])])
        
        # Extract skills from job description
        job_skills = self._extract_skills_from_job_description(job_description)
        
        if not job_skills:
            return 0.0
        
        # Calculate match percentage
        matched_skills = resume_skills.intersection(job_skills)
        match_ratio = len(matched_skills) / len(job_skills) if job_skills else 0
        
        # Scale to 0-100, but cap at 100
        score = min(match_ratio * 100, 100)
        
        return score
    
    def _extract_skills_from_job_description(self, job_description: str) -> set:
        """Extract skills mentioned in job description"""
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
            'postgresql', 'aws', 'docker', 'kubernetes', 'git', 'linux', 'agile',
            'scrum', 'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch',
            'html', 'css', 'typescript', 'angular', 'vue', 'django', 'flask', 'fastapi',
            'rest api', 'graphql', 'microservices', 'ci/cd', 'jenkins', 'terraform',
            'cloud computing', 'azure', 'gcp', 'redis', 'elasticsearch', 'kafka'
        ]
        
        job_lower = job_description.lower()
        found_skills = set()
        
        for skill in skill_keywords:
            if skill.lower() in job_lower:
                found_skills.add(skill.lower())
        
        return found_skills
    
    def _calculate_semantic_similarity(self, resume_data: Dict, job_embedding: np.ndarray) -> float:
        """Calculate semantic similarity using embeddings (0-100)"""
        resume_text = resume_data.get('full_text', '')
        
        if not resume_text:
            return 0.0
        
        # Generate embedding for resume
        resume_embedding = self.generate_embedding(resume_text)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(
            job_embedding.reshape(1, -1),
            resume_embedding.reshape(1, -1)
        )[0][0]
        
        # Scale to 0-100
        score = similarity * 100
        
        return max(0, min(score, 100))
    
    def _calculate_experience_match(self, resume_data: Dict, job_description: str) -> float:
        """Calculate experience relevance score (0-100)"""
        experiences = resume_data.get('experience', [])
        
        if not experiences:
            return 0.0
        
        # Extract keywords from job description
        job_keywords = self._extract_keywords_from_text(job_description)
        
        if not job_keywords:
            return 50.0  # Default score if no keywords found
        
        # Calculate match for each experience entry
        total_match = 0
        for exp in experiences:
            exp_text = exp.get('text', '').lower()
            exp_keywords = exp.get('keywords', [])
            
            # Count matching keywords
            matches = sum(1 for keyword in job_keywords if keyword in exp_text or keyword in exp_keywords)
            match_ratio = matches / len(job_keywords) if job_keywords else 0
            total_match += match_ratio
        
        # Average match across all experiences
        avg_match = total_match / len(experiences) if experiences else 0
        
        # Scale to 0-100
        score = avg_match * 100
        
        return max(0, min(score, 100))
    
    def _calculate_education_projects_score(self, resume_data: Dict, job_description: str) -> float:
        """Calculate education and projects score (0-100)"""
        education = resume_data.get('education', [])
        projects = resume_data.get('projects', [])
        
        job_keywords = self._extract_keywords_from_text(job_description)
        
        if not job_keywords:
            return 50.0
        
        scores = []
        
        # Score education
        for edu in education:
            edu_text = edu.get('text', '').lower()
            matches = sum(1 for keyword in job_keywords if keyword in edu_text)
            match_ratio = matches / len(job_keywords) if job_keywords else 0
            scores.append(match_ratio)
        
        # Score projects
        for proj in projects:
            proj_text = proj.get('text', '').lower()
            proj_keywords = proj.get('keywords', [])
            matches = sum(1 for keyword in job_keywords if keyword in proj_text or keyword in proj_keywords)
            match_ratio = matches / len(job_keywords) if job_keywords else 0
            scores.append(match_ratio)
        
        if not scores:
            return 0.0
        
        # Average score
        avg_score = sum(scores) / len(scores)
        
        # Scale to 0-100
        score = avg_score * 100
        
        return max(0, min(score, 100))
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Common technical and professional keywords
        keywords = []
        text_lower = text.lower()
        
        # Technical terms
        tech_terms = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'database',
            'api', 'microservices', 'cloud', 'aws', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data science', 'agile', 'scrum'
        ]
        
        for term in tech_terms:
            if term in text_lower:
                keywords.append(term)
        
        # Years of experience patterns
        years_pattern = r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)'
        if re.search(years_pattern, text_lower):
            keywords.append('experience')
        
        return keywords[:15]  # Limit to 15 keywords
    
    def get_strengths(self, resume_data: Dict, job_description: str) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        
        # Check skill matches
        resume_skills = set([s.lower() for s in resume_data.get('skills', [])])
        job_skills = self._extract_skills_from_job_description(job_description)
        matched_skills = resume_skills.intersection(job_skills)
        
        if matched_skills:
            strengths.append(f"Strong match in skills: {', '.join(list(matched_skills)[:5])}")
        
        # Check experience
        if resume_data.get('experience'):
            strengths.append(f"Has {len(resume_data.get('experience', []))} relevant experience entries")
        
        # Check projects
        if resume_data.get('projects'):
            strengths.append(f"Has {len(resume_data.get('projects', []))} project(s) listed")
        
        # Check education
        if resume_data.get('education'):
            strengths.append("Education background provided")
        
        if not strengths:
            strengths.append("Resume contains relevant information")
        
        return strengths[:5]  # Limit to 5 strengths
    
    def get_weaknesses(self, resume_data: Dict, job_description: str) -> List[str]:
        """Identify candidate weaknesses"""
        weaknesses = []
        
        # Check missing skills
        resume_skills = set([s.lower() for s in resume_data.get('skills', [])])
        job_skills = self._extract_skills_from_job_description(job_description)
        missing_skills = job_skills - resume_skills
        
        if missing_skills:
            weaknesses.append(f"Missing key skills: {', '.join(list(missing_skills)[:5])}")
        
        # Check experience
        if not resume_data.get('experience'):
            weaknesses.append("No work experience found in resume")
        elif len(resume_data.get('experience', [])) < 2:
            weaknesses.append("Limited work experience")
        
        # Check projects
        if not resume_data.get('projects'):
            weaknesses.append("No projects listed")
        
        # Check education
        if not resume_data.get('education'):
            weaknesses.append("Education information not clearly stated")
        
        if not weaknesses:
            weaknesses.append("No major weaknesses identified")
        
        return weaknesses[:5]  # Limit to 5 weaknesses
    
    def generate_summary(self, resume_data: Dict, scores: Dict) -> str:
        """Generate a summary for the candidate"""
        total_score = scores.get('total_score', 0)
        
        if total_score >= 80:
            rating = "Excellent match"
        elif total_score >= 60:
            rating = "Good match"
        elif total_score >= 40:
            rating = "Moderate match"
        else:
            rating = "Weak match"
        
        summary = f"This candidate has a {rating} (score: {total_score}%) for this position. "
        
        # Add details based on scores
        if scores.get('skill_match', 0) >= 70:
            summary += "Strong skill alignment with job requirements. "
        elif scores.get('skill_match', 0) < 40:
            summary += "Some key skills may be missing. "
        
        if scores.get('semantic_similarity', 0) >= 70:
            summary += "Resume content is highly relevant to the job description. "
        
        if scores.get('experience_match', 0) >= 70:
            summary += "Work experience aligns well with position requirements. "
        
        num_skills = len(resume_data.get('skills', []))
        if num_skills > 0:
            summary += f"Candidate has {num_skills} identified skills. "
        
        return summary.strip()

