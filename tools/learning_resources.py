"""
Learning Resources Tool
Provides courses and learning paths for skill development
"""

from typing import List, Dict


class LearningResourcesFinder:
    """Finds learning resources for skill development"""
    
    def __init__(self):
        self.name = "Learning Resources Finder"
        self.resources_database = self._create_resources_database()
    
    def _create_resources_database(self) -> Dict[str, List[Dict]]:
        """Create learning resources database"""
        
        resources = {
            "python": [
                {
                    "name": "Python for Everybody (Coursera)",
                    "platform": "Coursera",
                    "level": "Beginner",
                    "duration_hours": 40,
                    "cost_inr": 0,
                    "rating": 4.8,
                    "url": "https://www.coursera.org/specializations/python"
                },
                {
                    "name": "Complete Python Bootcamp (Udemy)",
                    "platform": "Udemy",
                    "level": "Beginner to Intermediate",
                    "duration_hours": 22,
                    "cost_inr": 499,
                    "rating": 4.6,
                    "url": "https://www.udemy.com/course/complete-python-bootcamp/"
                },
                {
                    "name": "Advanced Python Programming (Udemy)",
                    "platform": "Udemy",
                    "level": "Advanced",
                    "duration_hours": 15,
                    "cost_inr": 599,
                    "rating": 4.7,
                    "url": "https://www.udemy.com/course/advanced-python-programming/"
                }
            ],
            "machine learning": [
                {
                    "name": "Machine Learning by Andrew Ng (Coursera)",
                    "platform": "Coursera",
                    "level": "Intermediate",
                    "duration_hours": 60,
                    "cost_inr": 2000,
                    "rating": 4.9,
                    "url": "https://www.coursera.org/learn/machine-learning"
                },
                {
                    "name": "Deep Learning Specialization (Coursera)",
                    "platform": "Coursera",
                    "level": "Intermediate to Advanced",
                    "duration_hours": 100,
                    "cost_inr": 4000,
                    "rating": 4.8,
                    "url": "https://www.coursera.org/specializations/deep-learning"
                },
                {
                    "name": "ML with TensorFlow (Google Cloud)",
                    "platform": "Google Cloud",
                    "level": "Intermediate",
                    "duration_hours": 30,
                    "cost_inr": 0,
                    "rating": 4.7,
                    "url": "https://www.cloudskillsboost.google/paths/40"
                }
            ],
            "javascript": [
                {
                    "name": "The Complete JavaScript Course (Udemy)",
                    "platform": "Udemy",
                    "level": "Beginner",
                    "duration_hours": 69,
                    "cost_inr": 499,
                    "rating": 4.8,
                    "url": "https://www.udemy.com/course/the-complete-javascript-course/"
                },
                {
                    "name": "JavaScript Algorithms (Freecodecamp)",
                    "platform": "Freecodecamp",
                    "level": "Intermediate",
                    "duration_hours": 40,
                    "cost_inr": 0,
                    "rating": 4.7,
                    "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"
                }
            ],
            "react": [
                {
                    "name": "React - The Complete Guide (Udemy)",
                    "platform": "Udemy",
                    "level": "Intermediate",
                    "duration_hours": 49,
                    "cost_inr": 599,
                    "rating": 4.8,
                    "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"
                },
                {
                    "name": "React Official Tutorial",
                    "platform": "React.dev",
                    "level": "Beginner",
                    "duration_hours": 20,
                    "cost_inr": 0,
                    "rating": 4.9,
                    "url": "https://react.dev/learn"
                }
            ],
            "data science": [
                {
                    "name": "Data Science with Python (Coursera)",
                    "platform": "Coursera",
                    "level": "Intermediate",
                    "duration_hours": 50,
                    "cost_inr": 2000,
                    "rating": 4.7,
                    "url": "https://www.coursera.org/specializations/data-science-python"
                },
                {
                    "name": "SQL for Data Analysis (Udemy)",
                    "platform": "Udemy",
                    "level": "Beginner",
                    "duration_hours": 10,
                    "cost_inr": 399,
                    "rating": 4.6,
                    "url": "https://www.udemy.com/course/sql-for-data-analysis/"
                }
            ],
            "aws": [
                {
                    "name": "AWS Certified Cloud Practitioner (Udemy)",
                    "platform": "Udemy",
                    "level": "Beginner",
                    "duration_hours": 15,
                    "cost_inr": 499,
                    "rating": 4.7,
                    "url": "https://www.udemy.com/course/aws-certified-cloud-practitioner/"
                },
                {
                    "name": "AWS Free Tier Hands-on (AWS)",
                    "platform": "AWS",
                    "level": "Beginner",
                    "duration_hours": 20,
                    "cost_inr": 0,
                    "rating": 4.8,
                    "url": "https://aws.amazon.com/training/"
                }
            ]
        }
        
        return resources
    
    def find_resources(self, skill: str, level: str = "") -> List[Dict]:
        """Find resources for a skill"""
        
        skill_lower = skill.lower()
        
        # Search for skill in database
        for key in self.resources_database.keys():
            if skill_lower in key or key in skill_lower:
                resources = self.resources_database[key]
                
                # Filter by level if specified
                if level:
                    resources = [r for r in resources if level.lower() in r['level'].lower()]
                
                return resources
        
        return []
    
    def create_learning_path(self, skills: List[str]) -> Dict:
        """Create a learning path for multiple skills"""
        
        learning_path = {
            "skills": skills,
            "total_hours": 0,
            "total_cost": 0,
            "resources": []
        }
        
        for skill in skills:
            resources = self.find_resources(skill)
            
            if resources:
                # Pick the best rated resource
                best_resource = max(resources, key=lambda x: x['rating'])
                
                learning_path["resources"].append({
                    "skill": skill,
                    "course": best_resource['name'],
                    "platform": best_resource['platform'],
                    "duration_hours": best_resource['duration_hours'],
                    "cost_inr": best_resource['cost_inr'],
                    "rating": best_resource['rating']
                })
                
                learning_path["total_hours"] += best_resource['duration_hours']
                learning_path["total_cost"] += best_resource['cost_inr']
        
        return learning_path
    
    def format_resources(self, resources: List[Dict]) -> str:
        """Format resources for display"""
        
        if not resources:
            return "❌ No resources found for this skill"
        
        formatted = f"\n{'='*70}\n"
        formatted += f"📚 LEARNING RESOURCES ({len(resources)} found)\n"
        formatted += f"{'='*70}\n\n"
        
        for i, resource in enumerate(resources, 1):
            formatted += f"{i}. 📖 {resource['name']}\n"
            formatted += f"   Platform: {resource['platform']}\n"
            formatted += f"   Level: {resource['level']}\n"
            formatted += f"   Duration: {resource['duration_hours']} hours\n"
            formatted += f"   Cost: ₹{resource['cost_inr']}\n"
            formatted += f"   Rating: {'⭐' * int(resource['rating'])} ({resource['rating']}/5)\n"
            formatted += f"\n"
        
        return formatted
    
    def format_learning_path(self, learning_path: Dict) -> str:
        """Format learning path for display"""
        
        formatted = f"\n{'='*70}\n"
        formatted += f"🎓 LEARNING PATH - {', '.join(learning_path['skills'])}\n"
        formatted += f"{'='*70}\n\n"
        
        for i, resource in enumerate(learning_path['resources'], 1):
            formatted += f"{i}. Skill: {resource['skill']}\n"
            formatted += f"   Course: {resource['course']}\n"
            formatted += f"   Duration: {resource['duration_hours']} hours\n"
            formatted += f"   Cost: ₹{resource['cost_inr']}\n"
            formatted += f"\n"
        
        formatted += f"{'='*70}\n"
        formatted += f"📊 SUMMARY:\n"
        formatted += f"   Total Duration: {learning_path['total_hours']} hours (~{learning_path['total_hours']//4} weeks at 10 hrs/week)\n"
        formatted += f"   Total Cost: ₹{learning_path['total_cost']}\n"
        formatted += f"{'='*70}\n"
        
        return formatted


def main():
    """Test learning resources finder"""
    
    print("="*70)
    print("LEARNING RESOURCES FINDER - TEST")
    print("="*70)
    
    finder = LearningResourcesFinder()
    
    # Test 1: Find resources for a skill
    print("\n--- FIND RESOURCES ---")
    resources = finder.find_resources("Python", level="Beginner")
    print(finder.format_resources(resources))
    
    # Test 2: Create learning path
    print("\n--- LEARNING PATH ---")
    path = finder.create_learning_path(["Python", "Machine Learning", "React"])
    print(finder.format_learning_path(path))


if __name__ == "__main__":
    main()
