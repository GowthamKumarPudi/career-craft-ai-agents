"""
Job Search API Tool
Simulates job search functionality (can be replaced with real APIs)
"""

from typing import List, Dict
from datetime import datetime, timedelta
import random


class JobSearchAPI:
    """Job search tool using simulated job data"""
    
    def __init__(self):
        self.name = "Job Search Tool"
        self.job_database = self._create_job_database()
    
    def _create_job_database(self) -> List[Dict]:
        """Create sample job database"""
        
        jobs = [
            {
                "id": 1,
                "title": "Senior Python Developer",
                "company": "Google",
                "location": "Bangalore",
                "salary_min": 25,
                "salary_max": 35,
                "currency": "LPA",
                "skills_required": ["Python", "Django", "REST API", "Docker", "AWS"],
                "experience_years": 5,
                "job_type": "Full-time",
                "description": "Build scalable backend services using Python and modern technologies"
            },
            {
                "id": 2,
                "title": "Junior ML Engineer",
                "company": "Flipkart",
                "location": "Bangalore",
                "salary_min": 8,
                "salary_max": 15,
                "currency": "LPA",
                "skills_required": ["Python", "TensorFlow", "Machine Learning", "SQL"],
                "experience_years": 1,
                "job_type": "Full-time",
                "description": "Work on machine learning models for e-commerce recommendations"
            },
            {
                "id": 3,
                "title": "Full Stack Developer",
                "company": "Microsoft",
                "location": "Remote",
                "salary_min": 18,
                "salary_max": 28,
                "currency": "LPA",
                "skills_required": ["JavaScript", "React", "Node.js", "MongoDB", "Azure"],
                "experience_years": 3,
                "job_type": "Full-time",
                "description": "Develop web applications using modern frontend and backend technologies"
            },
            {
                "id": 4,
                "title": "Data Scientist",
                "company": "Amazon",
                "location": "Delhi",
                "salary_min": 20,
                "salary_max": 32,
                "currency": "LPA",
                "skills_required": ["Python", "SQL", "Statistics", "Machine Learning", "Tableau"],
                "experience_years": 2,
                "job_type": "Full-time",
                "description": "Analyze large datasets and build predictive models"
            },
            {
                "id": 5,
                "title": "Frontend Engineer",
                "company": "Uber",
                "location": "Bangalore",
                "salary_min": 15,
                "salary_max": 25,
                "currency": "LPA",
                "skills_required": ["React", "JavaScript", "CSS", "HTML", "Redux"],
                "experience_years": 2,
                "job_type": "Full-time",
                "description": "Build beautiful and responsive user interfaces"
            },
            {
                "id": 6,
                "title": "DevOps Engineer",
                "company": "Infosys",
                "location": "Remote",
                "salary_min": 14,
                "salary_max": 22,
                "currency": "LPA",
                "skills_required": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
                "experience_years": 2,
                "job_type": "Full-time",
                "description": "Manage infrastructure and deployment pipelines"
            }
        ]
        
        return jobs
    
    def search_jobs(self, keywords: str = "", location: str = "", 
                   min_experience: int = 0) -> List[Dict]:
        """Search for jobs matching criteria"""
        
        results = []
        keywords_lower = keywords.lower()
        
        for job in self.job_database:
            # Check keyword match
            keyword_match = (keywords_lower in job['title'].lower() or 
                           any(kw in keywords_lower for kw in job['skills_required']))
            
            # Check location match
            location_match = (location.lower() in job['location'].lower() or 
                            location.lower() == "remote" and job['location'].lower() == "remote")
            
            # Check experience match
            exp_match = job['experience_years'] >= min_experience
            
            if keyword_match and location_match and exp_match:
                results.append(job)
        
        return results
    
    def get_job_details(self, job_id: int) -> Dict:
        """Get detailed information about a job"""
        
        for job in self.job_database:
            if job['id'] == job_id:
                return {
                    **job,
                    "posted_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                    "applicants": random.randint(10, 200),
                    "similar_jobs": len([j for j in self.job_database 
                                        if any(s in j['skills_required'] for s in job['skills_required'])])
                }
        
        return {}
    
    def match_jobs(self, user_skills: List[str], 
                   target_location: str = "") -> List[Dict]:
        """Match jobs based on user skills"""
        
        matched_jobs = []
        user_skills_lower = [s.lower() for s in user_skills]
        
        for job in self.job_database:
            # Calculate skill match percentage
            required_skills = [s.lower() for s in job['skills_required']]
            matches = sum(1 for skill in required_skills if any(us in skill for us in user_skills_lower))
            match_percentage = (matches / len(required_skills)) * 100 if required_skills else 0
            
            # Filter by location if specified
            if target_location and target_location.lower() not in job['location'].lower():
                continue
            
            if match_percentage >= 50:  # At least 50% match
                matched_jobs.append({
                    **job,
                    "match_percentage": round(match_percentage, 1)
                })
        
        # Sort by match percentage
        matched_jobs.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        return matched_jobs
    
    def format_job_listings(self, jobs: List[Dict]) -> str:
        """Format jobs for display"""
        
        if not jobs:
            return "❌ No jobs found matching your criteria"
        
        formatted = f"\n{'='*70}\n"
        formatted += f"📊 FOUND {len(jobs)} JOB(S)\n"
        formatted += f"{'='*70}\n\n"
        
        for i, job in enumerate(jobs, 1):
            match_info = f" (Match: {job.get('match_percentage', 'N/A')}%)" if 'match_percentage' in job else ""
            
            formatted += f"{i}. 💼 {job['title']} - {job['company']}{match_info}\n"
            formatted += f"   📍 {job['location']} | 💰 ₹{job['salary_min']}-{job['salary_max']} {job['currency']}\n"
            formatted += f"   📌 Experience: {job['experience_years']} years\n"
            formatted += f"   🛠️  Skills: {', '.join(job['skills_required'][:3])}...\n"
            formatted += f"   📝 {job['description']}\n"
            formatted += f"\n"
        
        return formatted


def main():
    """Test job search API"""
    
    print("="*70)
    print("JOB SEARCH API - TEST")
    print("="*70)
    
    api = JobSearchAPI()
    
    # Test 1: Search by keywords
    print("\n--- SEARCH BY KEYWORDS ---")
    jobs = api.search_jobs(keywords="Python", location="Bangalore")
    print(api.format_job_listings(jobs))
    
    # Test 2: Match jobs by skills
    print("\n--- MATCH JOBS BY SKILLS ---")
    user_skills = ["Python", "Machine Learning", "Data Analysis"]
    matched = api.match_jobs(user_skills, target_location="Bangalore")
    print(api.format_job_listings(matched))
    
    # Test 3: Get specific job details
    print("\n--- JOB DETAILS ---")
    details = api.get_job_details(1)
    if details:
        print(f"Job ID: {details['id']}")
        print(f"Title: {details['title']}")
        print(f"Company: {details['company']}")
        print(f"Posted: {details.get('posted_date', 'N/A')}")
        print(f"Applicants: {details.get('applicants', 'N/A')}")
        print(f"Similar Jobs: {details.get('similar_jobs', 'N/A')}")


if __name__ == "__main__":
    main()
