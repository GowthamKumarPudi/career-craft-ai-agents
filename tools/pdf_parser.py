"""
PDF/Resume Parser Tool
Extracts text from resumes in various formats
"""

import os
import re
from typing import Dict, List


class ResumeParser:
    """Parses resume text and extracts structured information"""
    
    def __init__(self):
        self.name = "Resume Parser"
    
    def parse_text_resume(self, resume_text: str) -> Dict:
        """Parse resume from plain text"""
        
        result = {
            "name": self._extract_name(resume_text),
            "email": self._extract_email(resume_text),
            "phone": self._extract_phone(resume_text),
            "skills": self._extract_skills(resume_text),
            "experience": self._extract_experience(resume_text),
            "education": self._extract_education(resume_text),
            "certifications": self._extract_certifications(resume_text),
            "projects": self._extract_projects(resume_text)
        }
        
        return result
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume"""
        lines = text.split('\n')
        # Usually name is in first few lines
        for line in lines[:5]:
            if line.strip() and len(line.strip().split()) <= 4:
                # Check if it looks like a name (not email/phone)
                if '@' not in line and not re.search(r'\d{10}', line):
                    return line.strip()
        return "Not found"
    
    def _extract_email(self, text: str) -> str:
        """Extract email from resume"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else "Not found"
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from resume"""
        phone_pattern = r'(\+\d{1,3})?[-.\s]?\d{10}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else "Not found"
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume"""
        skills_keywords = [
            'python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust',
            'react', 'angular', 'vue', 'nodejs', 'django', 'flask',
            'sql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'github', 'gitlab', 'jenkins',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'data analysis', 'pandas', 'numpy', 'scipy',
            'html', 'css', 'rest api', 'graphql',
            'agile', 'scrum', 'jira', 'confluence',
            'communication', 'leadership', 'teamwork', 'problem-solving'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience from resume"""
        
        experience = []
        
        # Look for common experience indicators
        exp_section = text.lower().find('experience')
        if exp_section == -1:
            exp_section = text.lower().find('work experience')
        
        if exp_section != -1:
            # Extract next 1000 characters after "experience"
            exp_text = text[exp_section:exp_section+2000]
            
            # Look for job titles and companies
            lines = exp_text.split('\n')
            
            for i, line in enumerate(lines[1:6]):  # Check next 5 lines
                if line.strip():
                    experience.append({
                        "role": line.strip(),
                        "description": lines[i+2].strip() if i+2 < len(lines) else ""
                    })
        
        if not experience:
            experience.append({
                "role": "Experience section found but details unclear",
                "description": ""
            })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education from resume"""
        
        education = []
        edu_keywords = ['btech', 'b.tech', 'bachelor', 'master', 'mtech', 'm.tech', 
                       'diploma', 'degree', 'certification', 'course']
        
        text_lower = text.lower()
        edu_section = -1
        
        for keyword in edu_keywords:
            if keyword in text_lower:
                idx = text_lower.find(keyword)
                if idx != -1:
                    # Extract lines around education keyword
                    start = max(0, idx - 100)
                    end = min(len(text), idx + 200)
                    edu_section = text[start:end]
                    
                    education.append({
                        "degree": keyword.upper(),
                        "details": edu_section.strip()
                    })
        
        if not education:
            education.append({
                "degree": "Not specified",
                "details": ""
            })
        
        return education
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications from resume"""
        
        certifications = []
        cert_keywords = [
            'aws certified', 'google cloud', 'azure certified',
            'pmp', 'cissp', 'ccna', 'ccie',
            'scrum master', 'agile', 'comptia',
            'python certification', 'java certification'
        ]
        
        text_lower = text.lower()
        
        for cert in cert_keywords:
            if cert in text_lower:
                certifications.append(cert.title())
        
        return certifications
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract projects from resume"""
        
        projects = []
        projects_section = text.lower().find('projects')
        
        if projects_section != -1:
            # Extract next 1000 characters
            proj_text = text[projects_section:projects_section+1000]
            
            # Split by common separators
            lines = proj_text.split('\n')
            
            for line in lines[1:6]:
                if line.strip() and line.strip() != 'projects':
                    projects.append(line.strip())
        
        return projects
    
    def format_parsed_data(self, parsed_data: Dict) -> str:
        """Format parsed data into readable string"""
        
        formatted = f"""
╔════════════════════════════════════════════════════════╗
║              PARSED RESUME INFORMATION                 ║
╚════════════════════════════════════════════════════════╝

👤 NAME: {parsed_data.get('name', 'Not found')}
📧 EMAIL: {parsed_data.get('email', 'Not found')}
📱 PHONE: {parsed_data.get('phone', 'Not found')}

🛠️ SKILLS ({len(parsed_data.get('skills', []))})
{chr(10).join('   • ' + skill for skill in parsed_data.get('skills', []))}

💼 EXPERIENCE ({len(parsed_data.get('experience', []))})
"""
        for i, exp in enumerate(parsed_data.get('experience', []), 1):
            formatted += f"   {i}. {exp.get('role', 'Not specified')}\n"
        
        formatted += f"\n🎓 EDUCATION ({len(parsed_data.get('education', []))})\n"
        for edu in parsed_data.get('education', []):
            formatted += f"   • {edu.get('degree', 'Not specified')}\n"
        
        if parsed_data.get('certifications'):
            formatted += f"\n📜 CERTIFICATIONS ({len(parsed_data.get('certifications', []))})\n"
            for cert in parsed_data.get('certifications', []):
                formatted += f"   • {cert}\n"
        
        if parsed_data.get('projects'):
            formatted += f"\n📌 PROJECTS ({len(parsed_data.get('projects', []))})\n"
            for proj in parsed_data.get('projects', [])[:3]:
                formatted += f"   • {proj}\n"
        
        return formatted


def main():
    """Test resume parser"""
    
    print("="*60)
    print("RESUME PARSER - TEST")
    print("="*60)
    
    parser = ResumeParser()
    
    sample_resume = """
Gowtham Kumar Pudi
Email: gowtham@example.com
Phone: +91-9876543210

PROFESSIONAL SUMMARY:
Final year BTech student with expertise in AI/ML and Web Development

SKILLS:
Technical: Python, JavaScript, React, SQL, HTML, CSS, Git
AI/ML: TensorFlow, PyTorch, scikit-learn, Pandas, NumPy
Cloud: AWS, Google Cloud
Soft Skills: Problem-solving, Communication, Leadership

EXPERIENCE:
AI/ML Intern - TechCorp (3 months)
Developed machine learning models for recommendation systems
Analyzed datasets and created visualizations

Junior Developer - StartupXYZ (6 months)
Built React components for web application
Implemented REST APIs using Python Django

EDUCATION:
BTech in Computer Science, CGPA: 8.2/10
Relevant Coursework: Data Structures, Algorithms, Machine Learning, Web Development

CERTIFICATIONS:
AWS Certified Cloud Practitioner
Google Cloud Associate Cloud Engineer

PROJECTS:
1. Career Guidance AI System - Multi-agent system using Gemini API
2. Stock Price Prediction - ML model using LSTM networks
3. E-commerce Platform - Full-stack web application
"""
    
    print("\n📄 Parsing resume...\n")
    
    parsed_data = parser.parse_text_resume(sample_resume)
    
    formatted_output = parser.format_parsed_data(parsed_data)
    print(formatted_output)
    
    print("\n📊 Raw Parsed Data (JSON):")
    import json
    print(json.dumps(parsed_data, indent=2))


if __name__ == "__main__":
    main()
