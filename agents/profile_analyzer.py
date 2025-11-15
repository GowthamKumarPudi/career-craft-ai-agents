"""
Profile Analyzer Agent
Analyzes user profiles and resumes to extract key information
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


class ProfileAnalyzerAgent:
    """Analyzes user profiles and resumes"""
    
    def __init__(self):
        self.model = 'gemini-2.0-flash'
        self.name = "Profile Analyzer"
        self.instruction = """
You are a Profile Analysis Specialist. Your expertise includes:
- Resume analysis and optimization
- Skill identification and categorization
- Experience level assessment
- Career timeline analysis
- Professional strengths identification

When analyzing profiles:
1. Extract key information (skills, experience, education)
2. Identify strengths and weaknesses
3. Assess career level (entry, junior, mid, senior)
4. Provide actionable improvement suggestions
5. Highlight unique value propositions
"""

    def parse_resume(self, resume_text):
        """Parse and analyze resume text"""
        
        prompt = f"""
Analyze this resume/profile and extract key information:

RESUME/PROFILE:
{resume_text}

Provide a structured analysis with:
1. **Skills**: Technical and soft skills identified
2. **Experience**: Years of experience and roles
3. **Education**: Qualifications and certifications
4. **Career Level**: Entry/Junior/Mid/Senior
5. **Strengths**: Top 3 professional strengths
6. **Improvements**: Top 3 areas for improvement
7. **Summary**: Brief professional summary

Format as clear sections with bullet points.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def extract_skills(self, resume_text):
        """Extract technical and soft skills"""
        
        prompt = f"""
Extract all skills from this resume:

RESUME:
{resume_text}

Categorize and list:
1. **Technical Skills**: Programming languages, tools, frameworks
2. **Soft Skills**: Communication, leadership, problem-solving
3. **Domain Knowledge**: Industry expertise, specialized knowledge
4. **Certifications**: Professional certifications

Format as lists with importance level (High/Medium/Low)
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def assess_experience(self, resume_text):
        """Assess experience level and progression"""
        
        prompt = f"""
Analyze the career progression and experience level:

RESUME:
{resume_text}

Provide:
1. **Total Experience**: Years and months
2. **Career Level**: Entry-level / Junior / Mid-level / Senior / Lead
3. **Career Path**: Progression analysis
4. **Key Achievements**: Most impressive accomplishments
5. **Growth Trajectory**: Recommendations for advancement

Be specific and data-driven.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def generate_summary(self, resume_text):
        """Generate professional summary"""
        
        prompt = f"""
Create a compelling professional summary based on this resume:

RESUME:
{resume_text}

Write:
1. **Executive Summary**: 2-3 sentences capturing main strengths
2. **Value Proposition**: Why you're valuable to employers
3. **Key Highlights**: 3-5 bullet points of achievements
4. **Career Objective**: Direction for next 2-3 years

Make it compelling and concise.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def process_profile(self, resume_text, analysis_type="full"):
        """Process profile with different analysis types"""
        
        print(f"\n{'='*70}")
        print(f"{self.name}: Analyzing profile...")
        print(f"{'='*70}\n")
        
        if analysis_type == "full":
            print("Full Profile Analysis:\n")
            result = self.parse_resume(resume_text)
        elif analysis_type == "skills":
            print("Skills Extraction:\n")
            result = self.extract_skills(resume_text)
        elif analysis_type == "experience":
            print("Experience Assessment:\n")
            result = self.assess_experience(resume_text)
        elif analysis_type == "summary":
            print("Professional Summary:\n")
            result = self.generate_summary(resume_text)
        else:
            result = self.parse_resume(resume_text)
        
        print(result)
        print(f"\n{'='*70}\n")
        
        return result


def main():
    """Test the Profile Analyzer"""
    
    print("="*70)
    print("PROFILE ANALYZER AGENT - TEST")
    print("="*70)
    
    analyzer = ProfileAnalyzerAgent()
    
    # Sample resume for testing
    sample_resume = """
NAME: Gowtham Kumar Pudi
EMAIL: gowtham@example.com
PHONE: +91-XXXXXXXXXX

SUMMARY:
Final-year BTech student in Computer Science with strong interest in AI/ML. 
Experienced in Python, web development, and data analysis.

EDUCATION:
BTech in Computer Science (Final Year)
CGPA: 8.2/10

EXPERIENCE:
Intern - AI/ML Developer (3 months)
- Worked on machine learning projects
- Built recommendation systems using Python
- Analyzed datasets and created visualizations with Pandas

SKILLS:
Technical: Python, JavaScript, HTML/CSS, React, SQL, Git
AI/ML: TensorFlow, scikit-learn, Pandas, NumPy
Soft: Problem-solving, Communication, Team collaboration

PROJECTS:
- Career Guidance AI System (Ongoing capstone project)
- Data visualization dashboard with Power BI
- Web scraping and data analysis tool
"""
    
    # Test different analysis types
    analysis_types = ["full", "skills", "experience", "summary"]
    
    for analysis_type in analysis_types:
        print(f"\n--- {analysis_type.upper()} ANALYSIS ---")
        analyzer.process_profile(sample_resume, analysis_type)
        
        if analysis_type != analysis_types[-1]:
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
