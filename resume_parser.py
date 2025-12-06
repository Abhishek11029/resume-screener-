import os
import re
import PyPDF2
import docx2txt
from typing import Dict, List


class ResumeParser:
    """
    Parses resumes from PDF, DOCX, and TXT files
    Extracts: skills, experience, education, projects
    """
    
    def __init__(self):
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
            'postgresql', 'aws', 'docker', 'kubernetes', 'git', 'linux', 'agile',
            'scrum', 'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch',
            'html', 'css', 'typescript', 'angular', 'vue', 'django', 'flask', 'fastapi',
            'rest api', 'graphql', 'microservices', 'ci/cd', 'jenkins', 'terraform',
            'cloud computing', 'azure', 'gcp', 'redis', 'elasticsearch', 'kafka'
        ]
    
    def parse(self, file_path: str) -> Dict:
        """
        Parse resume file and extract structured data
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Extract text based on file type
        if file_ext == '.pdf':
            text = self._extract_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            text = self._extract_from_docx(file_path)
        elif file_ext == '.txt':
            text = self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Parse structured data
        parsed_data = {
            'raw_text': text,
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'projects': self._extract_projects(text),
            'full_text': text
        }
        
        return parsed_data
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            text = docx2txt.process(file_path)
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Also look for common skill patterns
        skill_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:developer|engineer|specialist|expert|proficient)',
            r'proficient in\s+([^,\n]+)',
            r'skills?[:\-]\s*([^\n]+)',
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                skills = [s.strip() for s in re.split(r'[,;|]', match)]
                found_skills.extend(skills)
        
        # Remove duplicates and normalize
        unique_skills = list(set([s.strip().lower() for s in found_skills if s.strip()]))
        return unique_skills[:20]  # Limit to top 20 skills
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience from resume"""
        experience = []
        
        # Look for experience section
        experience_patterns = [
            r'(?:experience|work history|employment)[:\-]?\s*(.*?)(?=\n\s*(?:education|projects|skills|$))',
            r'(\d{4}[\s\-–]+\d{4}|present|current).*?(?:developer|engineer|manager|analyst|specialist).*?\n(.*?)(?=\n\s*(?:\d{4}|education|projects|$))',
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match.strip():
                    experience.append({
                        'text': match.strip()[:500],  # Limit length
                        'keywords': self._extract_keywords(match)
                    })
        
        # If no structured experience found, extract sentences with job-related keywords
        if not experience:
            sentences = re.split(r'[.!?]\s+', text)
            job_keywords = ['developer', 'engineer', 'manager', 'analyst', 'worked', 'responsible', 'developed']
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in job_keywords):
                    if len(sentence) > 20:
                        experience.append({
                            'text': sentence.strip()[:200],
                            'keywords': self._extract_keywords(sentence)
                        })
        
        return experience[:5]  # Limit to 5 experiences
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        
        education_patterns = [
            r'(?:education|academic|qualification)[:\-]?\s*(.*?)(?=\n\s*(?:experience|projects|skills|$))',
            r'(bachelor|master|phd|doctorate|degree|diploma|certificate).*?\n(.*?)(?=\n\s*(?:bachelor|master|phd|experience|projects|$))',
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match.strip():
                    education.append({
                        'text': match.strip()[:300],
                        'keywords': self._extract_keywords(match)
                    })
        
        return education[:3]  # Limit to 3 education entries
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract projects from resume"""
        projects = []
        
        project_patterns = [
            r'(?:projects?|portfolio)[:\-]?\s*(.*?)(?=\n\s*(?:education|experience|skills|$))',
            r'project[:\-]?\s*(.*?)(?=\n\s*(?:project|education|experience|skills|$))',
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match.strip():
                    projects.append({
                        'text': match.strip()[:400],
                        'keywords': self._extract_keywords(match)
                    })
        
        return projects[:5]  # Limit to 5 projects
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        keywords = []
        text_lower = text.lower()
        
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                keywords.append(skill)
        
        return keywords[:10]  # Limit to 10 keywords

