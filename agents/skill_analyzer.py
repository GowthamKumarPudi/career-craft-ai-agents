"""
Skill Analyzer Agent
Identifies skill gaps and recommends learning paths
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


class SkillAnalyzerAgent:
    """Analyzes skills and identifies gaps"""
    
    def __init__(self):
        self.model = 'gemini-2.0-flash'
        self.name = "Skill Analyzer"
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
        elif query_type == "certifications":
            profile = kwargs.get('profile', '')
            role = kwargs.get('target_role', '')
            result = self.recommend_certifications(profile, role)
        elif query_type == "trends":
            industry = kwargs.get('industry', 'Software Development')
            result = self.analyze_industry_trends(industry)
        else:
            result = "Query type not recognized"
        
        print(result)
        print(f"\n{'='*70}\n")
        
        return result


def main():
    """Test the Skill Analyzer"""
    
    print("="*70)
    print("SKILL ANALYZER AGENT - TEST")
    print("="*70)
    
    analyzer = SkillAnalyzerAgent()
    
    print("\n--- IDENTIFY SKILL GAPS ---")
    analyzer.process_analysis("gaps",
                             current_skills="Python, JavaScript, HTML/CSS, SQL",
                             target_role="Data Scientist")
    
    print("\n--- CREATE LEARNING PATH ---")
    analyzer.process_analysis("learning",
                             skill="Machine Learning",
                             level="Beginner")
    
    print("\n--- RECOMMEND CERTIFICATIONS ---")
    analyzer.process_analysis("certifications",
                             profile="BTech Student, Python skills",
                             target_role="AI/ML Engineer")
    
    print("\n--- INDUSTRY TRENDS ---")
    analyzer.process_analysis("trends",
                             industry="Artificial Intelligence & Machine Learning")


if __name__ == "__main__":
    main()
