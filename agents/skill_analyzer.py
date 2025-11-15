"""
Skill Analyzer Agent
Identifies skill gaps and recommends learning paths
"""

import os
from dotenv import load_dotenv
from google import genai
from tools.skill_extractor import SkillExtractor
from tools.learning_resources import LearningResourcesFinder

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


class SkillAnalyzerAgent:
    """Analyzes skills and identifies gaps"""
    
    def __init__(self):
        self.model = 'gemini-2.0-flash'
        self.name = "Skill Analyzer"
        self.skill_extractor = SkillExtractor()
        self.learning_finder = LearningResourcesFinder()
        self.instruction = """
You are a Skill Gap Analysis Specialist. Your expertise includes:
- Skill assessment and evaluation
- Gap identification
- Learning path planning
- Industry skill trends
- Certification recommendations

When analyzing skills:
1. Assess current skill levels
2. Identify required skills for target role
3. Calculate skill gaps
4. Recommend learning resources
5. Create structured learning plans
"""

    def extract_and_analyze_skills(self, resume_or_profile_text: str):
        """Extract skills from text and provide analysis"""
        
        print(f"\n{'='*70}")
        print("Analyzing skills from your profile...")
        print(f"{'='*70}\n")
        
        # Extract skills
        extracted = self.skill_extractor.extract_skills(resume_or_profile_text)
        print(self.skill_extractor.format_extracted_skills(extracted))
        
        # Rank skills by demand
        all_skills = [skill for skills_list in extracted.values() for skill in skills_list]
        if all_skills:
            ranked = self.skill_extractor.rank_skills(all_skills)
            print(self.skill_extractor.format_ranked_skills(ranked))
        
        return extracted

    def compare_skills(self, user_skills: list, required_skills: list):
        """Compare user skills with required skills"""
        
        print(f"\n{'='*70}")
        print("Comparing skills...")
        print(f"{'='*70}\n")
        
        gaps = self.skill_extractor.find_skill_gaps(user_skills, required_skills)
        
        print(self.skill_extractor.format_skill_gaps(gaps))
        
        return gaps

    def identify_gaps(self, current_skills, target_role):
        """Identify skill gaps for target role"""
        
        prompt = f"""
Identify skill gaps between current skills and target role:

CURRENT SKILLS:
{current_skills}

TARGET ROLE: {target_role}

Provide:
1. **Have**: Skills user already has
2. **Need**: Critical skills required for role
3. **Gaps**: Skills to develop
4. **Nice-to-Have**: Optional skills
5. **Priority**: Which gaps to address first

Rate each skill as Critical/Important/Nice-to-Have
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def create_learning_path(self, skill_name, current_level="Beginner"):
        """Create a learning path for a specific skill"""
        
        prompt = f"""
Create a detailed learning path for this skill:

SKILL: {skill_name}
CURRENT LEVEL: {current_level}

Provide:
1. **Phase 1 - Foundations**: Basic concepts (1-2 weeks)
2. **Phase 2 - Intermediate**: Practical skills (2-3 weeks)
3. **Phase 3 - Advanced**: Expert level (3-4 weeks)
4. **Resources**: Courses, books, projects
5. **Timeline**: Expected time to reach proficiency

Include:
- Specific learning resources
- Hands-on projects
- Practice exercises
- Success metrics

Be detailed and realistic.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def create_learning_path_with_resources(self, skills_to_learn: list):
        """Create learning path with actual course resources"""
        
        print(f"\n{'='*70}")
        print("Creating personalized learning path...")
        print(f"{'='*70}\n")
        
        path = self.learning_finder.create_learning_path(skills_to_learn)
        formatted = self.learning_finder.format_learning_path(path)
        
        print(formatted)
        
        return path

    def recommend_certifications(self, user_profile, target_role):
        """Recommend relevant certifications"""
        
        prompt = f"""
Recommend certifications for career development:

USER PROFILE:
{user_profile}

TARGET ROLE: {target_role}

Recommend:
1. **Relevant Certifications**: Top 3-5 certifications
2. **Priority**: Which to pursue first
3. **Cost**: Approximate cost in INR
4. **Time Required**: Duration of each
5. **ROI**: Career benefit and salary impact
6. **Preparation**: How to prepare

Focus on certifications that are valuable in India.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def analyze_industry_trends(self, industry):
        """Analyze skills in demand for an industry"""
        
        prompt = f"""
Analyze top in-demand skills for this industry in 2025:

INDUSTRY: {industry}

Provide:
1. **Top Skills**: Top 5-10 skills in demand
2. **Emerging Skills**: New skills gaining importance
3. **Declining Skills**: Skills losing relevance
4. **Salary Impact**: How skills affect salary
5. **Learning Resources**: Where to learn these skills

Focus on the Indian market trends.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def suggest_next_skills(self, current_skills: list, career_goal: str = ""):
        """Suggest next skills to learn based on current skills and goal"""
        
        suggestions = self.skill_extractor.suggest_skills(current_skills, career_goal)
        
        print(f"\n{'='*70}")
        print(f"📚 SUGGESTED SKILLS FOR: {career_goal}")
        print(f"{'='*70}\n")
        
        if suggestions:
            print("Based on your current skills and career goal, consider learning:\n")
            for i, skill in enumerate(suggestions, 1):
                print(f"   {i}. {skill}")
            
            # Find resources for suggested skills
            print(f"\n{'='*70}")
            print("Learning Resources:\n")
            for skill in suggestions[:3]:
                resources = self.learning_finder.find_resources(skill)
                if resources:
                    best = max(resources, key=lambda x: x['rating'])
                    print(f"   {skill}: {best['name']} ({best['platform']})")
                    print(f"              Duration: {best['duration_hours']} hours | Cost: ₹{best['cost_inr']}")
        else:
            print("No suggestions available. Please provide more information.")
        
        return suggestions

    def analyze_resume_skills(self, resume_text: str):
        """Complete analysis of skills from resume"""
        
        print(f"\n{'='*70}")
        print("📄 COMPREHENSIVE SKILL ANALYSIS")
        print(f"{'='*70}\n")
        
        # Extract skills
        extracted = self.skill_extractor.extract_skills(resume_text)
        print(self.skill_extractor.format_extracted_skills(extracted))
        
        # Get all skills
        all_skills = [skill for skills_list in extracted.values() for skill in skills_list]
        
        if all_skills:
            # Rank by demand
            ranked = self.skill_extractor.rank_skills(all_skills)
            print("\n📊 SKILLS RANKED BY DEMAND:")
            print(self.skill_extractor.format_ranked_skills(ranked))
            
            return {
                "extracted_skills": extracted,
                "all_skills": all_skills,
                "ranked_skills": ranked
            }
        
        return {"extracted_skills": extracted, "all_skills": [], "ranked_skills": []}

    def process_analysis(self, query_type, **kwargs):
        """Process skill analysis requests"""
        
        print(f"\n{'='*70}")
        print(f"{self.name}: Analyzing skills...")
        print(f"{'='*70}\n")
        
        if query_type == "gaps":
            current = kwargs.get('current_skills', '')
            target = kwargs.get('target_role', '')
            result = self.identify_gaps(current, target)
        elif query_type == "learning":
            skill = kwargs.get('skill', 'Python')
            level = kwargs.get('level', 'Beginner')
            result = self.create_learning_path(skill, level)
        elif query_type == "learning_with_resources":
            skills = kwargs.get('skills', [])
            result = self.create_learning_path_with_resources(skills)
        elif query_type == "certifications":
            profile = kwargs.get('profile', '')
            role = kwargs.get('target_role', '')
            result = self.recommend_certifications(profile, role)
        elif query_type == "trends":
            industry = kwargs.get('industry', 'Software Development')
            result = self.analyze_industry_trends(industry)
        elif query_type == "extract":
            resume = kwargs.get('resume_text', '')
            result = self.extract_and_analyze_skills(resume)
        elif query_type == "compare":
            user_skills = kwargs.get('user_skills', [])
            required_skills = kwargs.get('required_skills', [])
            result = self.compare_skills(user_skills, required_skills)
        elif query_type == "suggest":
            current_skills = kwargs.get('current_skills', [])
            goal = kwargs.get('career_goal', '')
            result = self.suggest_next_skills(current_skills, goal)
        elif query_type == "resume_analysis":
            resume_text = kwargs.get('resume_text', '')
            result = self.analyze_resume_skills(resume_text)
        else:
            result = "Query type not recognized"
        
        if isinstance(result, dict) and query_type not in ['learning_with_resources', 'compare', 'resume_analysis']:
            print(result)
        elif isinstance(result, str):
            print(result)
        
        print(f"\n{'='*70}\n")
        
        return result


def main():
    """Test the Skill Analyzer"""
    
    print("="*70)
    print("SKILL ANALYZER AGENT - TEST")
    print("="*70)
    
    analyzer = SkillAnalyzerAgent()
    
    # Sample resume for testing
    sample_resume = """
Gowtham Kumar Pudi
Final year BTech Student - Computer Science

SKILLS:
Technical: Python, JavaScript, React, SQL, HTML, CSS, Git
AI/ML: TensorFlow, scikit-learn, Pandas, NumPy
Cloud: AWS, Google Cloud
Soft Skills: Problem-solving, Communication, Teamwork

EXPERIENCE:
AI/ML Intern - 3 months
Developed machine learning models using Python
Analyzed datasets with Pandas and visualized with Matplotlib

EDUCATION:
BTech in Computer Science, CGPA: 8.2/10
"""
    
    print("\n--- EXTRACT AND ANALYZE SKILLS ---")
    analyzer.process_analysis("extract", resume_text=sample_resume)
    
    print("\n--- IDENTIFY SKILL GAPS ---")
    analyzer.process_analysis("gaps",
                             current_skills="Python, JavaScript, HTML/CSS, SQL",
                             target_role="Data Scientist")
    
    print("\n--- CREATE LEARNING PATH WITH RESOURCES ---")
    analyzer.process_analysis("learning_with_resources",
                             skills=["Machine Learning", "Python", "SQL"])
    
    print("\n--- COMPARE SKILLS ---")
    analyzer.process_analysis("compare",
                             user_skills=["Python", "JavaScript", "React"],
                             required_skills=["Python", "Data Analysis", "SQL", "Machine Learning"])
    
    print("\n--- SUGGEST NEXT SKILLS ---")
    analyzer.process_analysis("suggest",
                             current_skills=["Python", "SQL", "Git"],
                             career_goal="Data Science")
    
    print("\n--- RECOMMEND CERTIFICATIONS ---")
    analyzer.process_analysis("certifications",
                             profile="BTech Student, Python skills",
                             target_role="AI/ML Engineer")
    
    print("\n--- INDUSTRY TRENDS ---")
    analyzer.process_analysis("trends",
                             industry="Artificial Intelligence & Machine Learning")


if __name__ == "__main__":
    main()
