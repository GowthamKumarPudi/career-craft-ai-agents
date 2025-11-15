"""
Skill Extractor Tool
Extracts and categorizes skills from text, resumes, and job descriptions
"""

from typing import Dict, List, Tuple


class SkillExtractor:
    """Extracts and analyzes skills from various text sources"""
    
    def __init__(self):
        self.name = "Skill Extractor"
        self.skills_database = self._create_skills_database()
    
    def _create_skills_database(self) -> Dict[str, List[str]]:
        """Create comprehensive skills database"""
        
        skills = {
            "programming_languages": [
                "python", "java", "javascript", "c++", "c#", "go", "rust", "kotlin",
                "swift", "php", "ruby", "scala", "r", "matlab", "vb.net", "perl",
                "typescript", "groovy", "dart", "lua"
            ],
            "frontend": [
                "react", "angular", "vue", "svelte", "html", "css", "bootstrap",
                "tailwind", "material design", "webpack", "babel", "responsive design",
                "jquery", "next.js", "gatsby", "nuxt", "flutter web", "flutter"
            ],
            "backend": [
                "django", "flask", "fastapi", "nodejs", "express", "spring", "spring boot",
                "laravel", "ruby on rails", "asp.net", "asp.net core", "nest.js",
                "graphql", "rest api", "microservices", "monolithic"
            ],
            "databases": [
                "sql", "mysql", "postgresql", "mongodb", "cassandra", "redis",
                "elasticsearch", "dynamodb", "firebase", "neo4j", "oracle",
                "sqlite", "mariadb", "couchdb", "influxdb"
            ],
            "cloud_platforms": [
                "aws", "azure", "google cloud", "gcp", "heroku", "digital ocean",
                "alibaba cloud", "ibm cloud", "oracle cloud", "kubernetes", "docker",
                "docker swarm", "openstack"
            ],
            "devops": [
                "docker", "kubernetes", "jenkins", "gitlab ci", "github actions",
                "circleci", "travis ci", "terraform", "ansible", "puppet", "chef",
                "prometheus", "grafana", "elk stack", "datadog", "newrelic"
            ],
            "machine_learning": [
                "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
                "lightgbm", "catboost", "hugging face", "transformers", "nlp",
                "computer vision", "deep learning", "neural networks", "lstm", "cnn",
                "rnn", "gan", "reinforcement learning", "supervised learning",
                "unsupervised learning", "nlp", "cv"
            ],
            "data_science": [
                "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
                "tableau", "power bi", "excel", "jupyter", "r", "spss", "sas",
                "data analysis", "data visualization", "data mining", "statistical analysis"
            ],
            "web_technologies": [
                "rest", "graphql", "soap", "http", "https", "json", "xml",
                "oauth", "jwt", "ssl/tls", "cors", "websockets", "progressive web app",
                "pwa"
            ],
            "version_control": [
                "git", "github", "gitlab", "bitbucket", "svn", "mercurial",
                "perforce", "version control", "branching", "merging"
            ],
            "soft_skills": [
                "communication", "leadership", "problem-solving", "teamwork",
                "project management", "agile", "scrum", "kanban", "time management",
                "critical thinking", "creativity", "adaptability", "collaboration",
                "presentation", "negotiation", "conflict resolution", "mentoring"
            ],
            "certifications": [
                "aws certified", "google cloud certified", "azure certified",
                "pmp", "cissp", "ccna", "ccie", "linux+", "security+",
                "scrum master", "certified kubernetes", "terraform associate"
            ],
            "methodologies": [
                "agile", "scrum", "kanban", "waterfall", "devops", "continuous integration",
                "continuous deployment", "test-driven development", "bdd", "pair programming",
                "extreme programming"
            ],
            "other_tools": [
                "jira", "confluence", "slack", "teams", "asana", "trello",
                "notion", "figma", "adobe xd", "postman", "insomnia", "swagger",
                "vs code", "intellij", "pycharm", "sublime", "vim"
            ]
        }
        
        return skills
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from text"""
        
        text_lower = text.lower()
        found_skills = {
            "programming_languages": [],
            "frontend": [],
            "backend": [],
            "databases": [],
            "cloud_platforms": [],
            "devops": [],
            "machine_learning": [],
            "data_science": [],
            "web_technologies": [],
            "version_control": [],
            "soft_skills": [],
            "certifications": [],
            "methodologies": [],
            "other_tools": []
        }
        
        # Search for each skill in the database
        for category, skills_list in self.skills_database.items():
            for skill in skills_list:
                # Use word boundary matching for more accurate results
                if f" {skill} " in f" {text_lower} " or text_lower.endswith(skill):
                    if skill not in found_skills[category]:
                        found_skills[category].append(skill.title())
        
        return found_skills
    
    def categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize given skills"""
        
        categorized = {
            "programming_languages": [],
            "frontend": [],
            "backend": [],
            "databases": [],
            "cloud_platforms": [],
            "devops": [],
            "machine_learning": [],
            "data_science": [],
            "web_technologies": [],
            "version_control": [],
            "soft_skills": [],
            "certifications": [],
            "methodologies": [],
            "other_tools": []
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            
            for category, skills_list in self.skills_database.items():
                if skill_lower in skills_list:
                    categorized[category].append(skill.title())
                    break
        
        return categorized
    
    def find_skill_gaps(self, user_skills: List[str], 
                       required_skills: List[str]) -> Dict:
        """Find gaps between user skills and required skills"""
        
        user_skills_lower = [s.lower() for s in user_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        gaps = {
            "have_skills": [],
            "missing_skills": [],
            "match_percentage": 0,
            "priority_skills": []
        }
        
        # Find what user has
        for req_skill in required_skills_lower:
            if req_skill in user_skills_lower:
                gaps["have_skills"].append(req_skill.title())
            else:
                gaps["missing_skills"].append(req_skill.title())
        
        # Calculate match percentage
        if required_skills_lower:
            gaps["match_percentage"] = (len(gaps["have_skills"]) / len(required_skills_lower)) * 100
        
        # Priority is missing skills that are critical
        critical_keywords = ["python", "java", "javascript", "sql", "aws", "docker", "kubernetes"]
        gaps["priority_skills"] = [
            skill for skill in gaps["missing_skills"] 
            if any(kw in skill.lower() for kw in critical_keywords)
        ]
        
        return gaps
    
    def rank_skills(self, skills: List[str]) -> List[Tuple[str, float]]:
        """Rank skills by relevance and demand (simulated)"""
        
        # Simulated skill demand scores (0-100)
        demand_scores = {
            "python": 95,
            "javascript": 93,
            "java": 92,
            "react": 90,
            "aws": 88,
            "docker": 87,
            "kubernetes": 86,
            "machine learning": 85,
            "sql": 84,
            "nodejs": 82,
            "angular": 75,
            "c++": 70,
            "golang": 72,
            "rust": 68,
            "scala": 60,
            "php": 65,
            "ruby": 55,
            "r": 70,
            "tensorflow": 80,
            "pytorch": 78,
        }
        
        ranked = []
        for skill in skills:
            skill_lower = skill.lower()
            score = demand_scores.get(skill_lower, 50)  # Default score if not found
            ranked.append((skill, score))
        
        # Sort by score descending
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        return ranked
    
    def suggest_skills(self, current_skills: List[str], 
                      career_goal: str = "") -> List[str]:
        """Suggest skills to learn based on current skills and goal"""
        
        # Define skill progression paths
        progression_paths = {
            "frontend": ["HTML", "CSS", "JavaScript", "React", "TypeScript", "Next.js"],
            "backend": ["Python", "Django", "PostgreSQL", "REST API", "Docker", "AWS"],
            "data science": ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL"],
            "devops": ["Linux", "Docker", "Kubernetes", "AWS", "Terraform", "Jenkins"],
            "machine learning": ["Python", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "MLOps"]
        }
        
        current_skills_lower = [s.lower() for s in current_skills]
        suggestions = []
        
        # Match career goal to progression path
        goal_lower = career_goal.lower() if career_goal else ""
        path = None
        
        for key, skills in progression_paths.items():
            if key in goal_lower or goal_lower in key:
                path = skills
                break
        
        if path:
            for skill in path:
                if skill.lower() not in current_skills_lower:
                    suggestions.append(skill)
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def format_extracted_skills(self, skills_dict: Dict[str, List[str]]) -> str:
        """Format extracted skills for display"""
        
        formatted = f"\n{'='*70}\n"
        formatted += f"🛠️ EXTRACTED SKILLS\n"
        formatted += f"{'='*70}\n\n"
        
        total_skills = 0
        for category, skills in skills_dict.items():
            if skills:
                category_name = category.replace('_', ' ').title()
                formatted += f"📌 {category_name}:\n"
                formatted += f"   {', '.join(skills)}\n\n"
                total_skills += len(skills)
        
        formatted += f"{'='*70}\n"
        formatted += f"Total Skills Found: {total_skills}\n"
        formatted += f"{'='*70}\n"
        
        return formatted
    
    def format_skill_gaps(self, gaps: Dict) -> str:
        """Format skill gaps for display"""
        
        formatted = f"\n{'='*70}\n"
        formatted += f"📊 SKILL GAP ANALYSIS\n"
        formatted += f"{'='*70}\n\n"
        
        formatted += f"✅ Skills You Have ({len(gaps['have_skills'])}):\n"
        if gaps['have_skills']:
            formatted += f"   {', '.join(gaps['have_skills'])}\n\n"
        else:
            formatted += f"   None found\n\n"
        
        formatted += f"❌ Skills You Need ({len(gaps['missing_skills'])}):\n"
        if gaps['missing_skills']:
            formatted += f"   {', '.join(gaps['missing_skills'])}\n\n"
        else:
            formatted += f"   Perfect match!\n\n"
        
        if gaps['priority_skills']:
            formatted += f"🔥 Priority Skills to Learn:\n"
            formatted += f"   {', '.join(gaps['priority_skills'])}\n\n"
        
        formatted += f"📈 Match Percentage: {gaps['match_percentage']:.1f}%\n"
        formatted += f"{'='*70}\n"
        
        return formatted
    
    def format_ranked_skills(self, ranked_skills: List[Tuple[str, float]]) -> str:
        """Format ranked skills for display"""
        
        formatted = f"\n{'='*70}\n"
        formatted += f"⭐ SKILLS BY DEMAND\n"
        formatted += f"{'='*70}\n\n"
        
        for i, (skill, score) in enumerate(ranked_skills, 1):
            bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
            formatted += f"{i}. {skill:<20} {bar} {score:.0f}%\n"
        
        formatted += f"{'='*70}\n"
        
        return formatted


def main():
    """Test skill extractor"""
    
    print("="*70)
    print("SKILL EXTRACTOR - TEST")
    print("="*70)
    
    extractor = SkillExtractor()
    
    # Sample resume text
    sample_text = """
I am a software engineer with expertise in Python, JavaScript, and React.
I have worked with Docker, Kubernetes, and AWS cloud platforms.
My database experience includes PostgreSQL, MongoDB, and Redis.
I'm proficient in machine learning with TensorFlow and scikit-learn.
I practice agile development and have experience with Git and GitHub.
Strong communication and leadership skills with 5 years of experience.
Certified Scrum Master and AWS Solutions Architect Associate.
"""
    
    # Test 1: Extract skills
    print("\n--- EXTRACT SKILLS ---")
    extracted = extractor.extract_skills(sample_text)
    print(extractor.format_extracted_skills(extracted))
    
    # Test 2: Find skill gaps
    print("\n--- SKILL GAPS ---")
    user_skills = ["Python", "React", "Docker"]
    required_skills = ["Python", "Java", "React", "Kubernetes", "AWS"]
    gaps = extractor.find_skill_gaps(user_skills, required_skills)
    print(extractor.format_skill_gaps(gaps))
    
    # Test 3: Rank skills
    print("\n--- RANKED SKILLS ---")
    skills_to_rank = ["Python", "JavaScript", "Go", "Rust", "PHP"]
    ranked = extractor.rank_skills(skills_to_rank)
    print(extractor.format_ranked_skills(ranked))
    
    # Test 4: Suggest skills
    print("\n--- SKILL SUGGESTIONS ---")
    current = ["Python", "SQL", "Git"]
    goal = "Data Science"
    suggestions = extractor.suggest_skills(current, goal)
    print(f"\nBased on your goal ({goal}), here are suggested skills:")
    for i, skill in enumerate(suggestions, 1):
        print(f"   {i}. {skill}")


if __name__ == "__main__":
    main()
