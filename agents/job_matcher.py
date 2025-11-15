"""
Job Matcher Agent
Finds relevant job opportunities based on user profile
"""

import os
from dotenv import load_dotenv
from google import genai
from tools.job_api import JobSearchAPI


load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


class JobMatcherAgent:
    """Matches users with relevant job opportunities"""
    
    def __init__(self):
        self.model = 'gemini-2.0-flash'
        self.name = "Job Matcher"
        self.instruction = """
You are a Job Matching Specialist. Your expertise includes:
- Job market analysis
- Role matching based on skills and experience
- Career path recommendations
- Industry insights
- Salary and growth potential analysis

When matching jobs:
1. Analyze user skills and experience
2. Identify suitable roles and companies
3. Assess fit and growth potential
4. Provide search strategies
5. Highlight market opportunities
"""

    def match_jobs(self, user_profile, preferences=None):
        """Match user with suitable jobs"""
        
        preferences_text = preferences if preferences else "No specific preferences provided"
        
        prompt = f"""
Based on this user profile, recommend suitable job roles:

USER PROFILE:
{user_profile}

USER PREFERENCES:
{preferences_text}

Provide:
1. **Recommended Roles**: Top 5 job titles that match
2. **Industries**: Best industries to target
3. **Companies**: Types of companies (startups, enterprises, etc.)
4. **Growth Potential**: Expected salary growth and opportunities
5. **Action Plan**: Steps to land these roles

Be specific and actionable.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def find_opportunities(self, role_title, location="Remote"):
        """Find specific job opportunities using real API"""
        
        api = JobSearchAPI()
        jobs = api.search_jobs(keywords=role_title, location=location)
        
        formatted = api.format_job_listings(jobs)
        
        print(formatted)
        return formatted

        
        prompt = f"""
Help find job opportunities for this role:

ROLE: {role_title}
LOCATION: {location}

Provide:
1. **Job Search Strategy**: Where and how to search
2. **Target Companies**: Companies that hire for this role
3. **Salary Range**: Expected salary in India
4. **Growth Path**: Career progression in this role
5. **Resources**: Job boards and networking tips

Focus on practical, actionable advice.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def analyze_job_fit(self, user_profile, job_description):
        """Analyze how well user fits a specific job"""
        
        prompt = f"""
Analyze the fit between user profile and job description:

USER PROFILE:
{user_profile}

JOB DESCRIPTION:
{job_description}

Provide:
1. **Match Score**: 0-100 percentage
2. **Strengths**: How user matches the role
3. **Gaps**: Missing skills or experience
4. **Fit Assessment**: Is this role suitable?
5. **Development Plan**: How to bridge gaps

Be honest and constructive.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def explore_career_paths(self, current_role):
        """Explore different career paths from current role"""
        
        prompt = f"""
What are the possible career paths from this role:

CURRENT ROLE: {current_role}

Provide:
1. **Horizontal Moves**: Similar roles in different companies/industries
2. **Vertical Growth**: Advancement within the field
3. **Lateral Moves**: Switch to different domains
4. **Timeline**: Expected career progression
5. **Skills Development**: What to learn for each path

Be comprehensive and inspiring.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def process_matching(self, user_profile, query_type="match", **kwargs):
        """Process job matching requests"""
        
        print(f"\n{'='*70}")
        print(f"{self.name}: Processing job matching request...")
        print(f"{'='*70}\n")
        
        if query_type == "match":
            preferences = kwargs.get('preferences', None)
            result = self.match_jobs(user_profile, preferences)
        elif query_type == "find":
            role = kwargs.get('role', 'Software Engineer')
            location = kwargs.get('location', 'Remote')
            result = self.find_opportunities(role, location)
        elif query_type == "fit":
            job_desc = kwargs.get('job_description', '')
            result = self.analyze_job_fit(user_profile, job_desc)
        elif query_type == "paths":
            current_role = kwargs.get('current_role', 'Junior Developer')
            result = self.explore_career_paths(current_role)
        else:
            result = self.match_jobs(user_profile)
        
        print(result)
        print(f"\n{'='*70}\n")
        
        return result


def main():
    """Test the Job Matcher"""
    
    print("="*70)
    print("JOB MATCHER AGENT - TEST")
    print("="*70)
    
    matcher = JobMatcherAgent()
    
    sample_profile = """
Skills: Python, JavaScript, React, SQL, Machine Learning basics
Experience: 2 years as Junior Developer
Education: BTech in Computer Science
Interests: AI/ML, Web Development, Startups
"""
    
    print("\n--- MATCHING JOBS ---")
    matcher.process_matching(sample_profile, "match", 
                            preferences="Remote, startup environment, AI focus")
    
    print("\n--- FINDING OPPORTUNITIES ---")
    matcher.process_matching(sample_profile, "find", 
                            role="Python Developer", location="Bangalore")
    
    print("\n--- EXPLORING CAREER PATHS ---")
    matcher.process_matching(sample_profile, "paths", 
                            current_role="Junior Full Stack Developer")


if __name__ == "__main__":
    main()
